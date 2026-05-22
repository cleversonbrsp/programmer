package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	oidc "github.com/coreos/go-oidc/v3/oidc"
	"golang.org/x/oauth2"
)

// ClientID e ClientSecret são as credenciais que você cadastrou no Keycloak
// para a aplicação "app". Sem elas o Keycloak não sabe qual app está pedindo login
// e não libera a troca do código de autorização por tokens.
var (
	ClientID     = "app"
	ClientSecret = "..."
)

func main() {
	// O contexto carrega cancelamento/timeout para chamadas HTTP.
	// Usamos Background() aqui porque o programa inteiro depende dessas requisições
	// e não há um request HTTP "pai" ainda — o main é o ponto de partida.
	ctx := context.Background()

	// Antes de redirecionar o usuário, precisamos descobrir onde o Keycloak expõe
	// login (auth) e troca de token (token). O NewProvider lê o .well-known do realm
	// e monta isso automaticamente, em vez de você copiar URLs na mão e quebrar
	// quando mudar versão ou path. Keycloak 17+ usa /realms/...; versões antigas usavam /auth/realms/...
	provider, err := oidc.NewProvider(ctx, "http://localhost:8080/realms/demo")
	if err != nil {
		log.Fatal(err)
	}

	// Aqui descrevemos "quem somos" no OAuth2: qual app, para onde voltar após login
	// e quais dados pedimos (openid, perfil, e-mail, roles). O Endpoint vem do provider
	// porque o Keycloak já publicou as URLs corretas na descoberta OIDC acima.
	config := oauth2.Config{
		ClientID:     ClientID,
		ClientSecret: ClientSecret,
		Endpoint:     provider.Endpoint(),
		RedirectURL:  "http://localhost:8081/auth/callback",
		Scopes:       []string{oidc.ScopeOpenID, "profile", "email", "roles"},
	}

	// O state é um valor que nós geramos e o Keycloak devolve no callback.
	// Quando o usuário volta, comparamos: se for diferente, alguém pode estar
	// forjando o redirect (ataque CSRF). Neste exemplo é fixo ("exemplo"); em produção
	// você geraria um valor aleatório por sessão e guardaria (cookie/memória).
	state := "exemplo"

	// Quando o usuário acessa http://localhost:8081/ no navegador, ainda não está
	// logado nesta app. Por isso não mostramos uma página local: montamos a URL de
	// autorização do Keycloak (AuthCodeURL) e redirecionamos (302). O usuário passa
	// a ver a tela de login do IdP; depois de autenticar, o Keycloak o manda de volta
	// para /auth/callback com ?code=...&state=...
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, config.AuthCodeURL(state), http.StatusFound)
	})

	// Esta rota só é chamada depois que o usuário logou no Keycloak. O navegador chega
	// com code (autorização temporária) e state na query string.
	http.HandleFunc("/auth/callback", func(w http.ResponseWriter, r *http.Request) {
		// Primeiro conferimos o state: tem que ser o mesmo que enviamos no "/".
		// Se não bater, ignoramos a requisição porque não confiamos na origem do redirect.
		if r.URL.Query().Get("state") != state {
			http.Error(w, "State doesnt match", http.StatusBadRequest)
			return
		}

		// O code sozinho não autentica nada — é só um ticket de uso único. Trocamos
		// ele por access_token (e refresh, se houver) fazendo POST no endpoint de token
		// do Keycloak, usando ClientID/Secret e RedirectURL cadastrados.
		oauth2Token, err := config.Exchange(ctx, r.URL.Query().Get("code"))
		if err != nil {
			http.Error(w, "problema ao trocar token", http.StatusInternalServerError)
			return
		}

		// No fluxo OpenID Connect, além do access token vem o id_token (JWT com claims
		// do usuário). A biblioteca oauth2 guarda isso em Extra("id_token"); aqui só
		// extraímos a string para exibir no JSON de resposta deste exemplo.
		idToken, ok := oauth2Token.Extra("id_token").(string)
		if !ok {
			http.Error(w, "problema ao pegar id token", http.StatusInternalServerError)
			return
		}

		// Montamos um JSON legível com os tokens para você inspecionar no browser
		// (aula/demo). Em produção você validaria o id_token, criaria sessão, etc.
		res := struct {
			OAuth2Token *oauth2.Token
			IDToken     string
		}{
			oauth2Token, idToken,
		}

		data, _ := json.MarshalIndent(res, "", "  ")
		w.Write(data)
	})

	// Escutamos na porta 8081 porque o RedirectURL e o client no Keycloak apontam
	// para http://localhost:8081/auth/callback — tem que ser a mesma origem.
	log.Fatal(http.ListenAndServe(":8081", nil))
}

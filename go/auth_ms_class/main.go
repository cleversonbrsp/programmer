// Package main define o ponto de entrada da aplicação.
// Esta é uma aplicação de exemplo que integra autenticação OAuth2/OpenID Connect
// com o Keycloak, usando redirecionamento para login e callback de código de autorização.
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"

    "golang.org/x/oauth2"
)

// Credenciais da aplicação que foram registradas no Keycloak.
// Em produção, estes valores devem vir de variáveis de ambiente ou de um cofre secreto.
var (
    clientID     = "app"
    clientSecret = "..."
)

func main() {
    // Contexto base para chamadas de rede com o Keycloak.
    ctx := context.Background()

    // Configura o fluxo OAuth2 para esta aplicação.
    // Usamos here os endpoints padrão do Keycloak para OpenID Connect.
    // O RedirectURL deve corresponder exatamente ao callback cadastrado no Keycloak.
    config := oauth2.Config{
        ClientID:     clientID,
        ClientSecret: clientSecret,
        Endpoint: oauth2.Endpoint{
            AuthURL:  "http://localhost:8080/realms/demo/protocol/openid-connect/auth",
            TokenURL: "http://localhost:8080/realms/demo/protocol/openid-connect/token",
        },
        RedirectURL: "http://localhost:8081/auth/callback",
        Scopes:      []string{"openid", "profile", "email", "roles"},
    }

    // Valor estático de exemplo para proteger o fluxo contra CSRF.
    // Em uma aplicação real, esse valor deve ser gerado dinamicamente por usuário/sessão.
    state := "exemplo"

    // Define a rota raiz "/".
    // Quando um usuário acessa esta rota, ele é redirecionado para o Keycloak
    // para iniciar o fluxo de login via OpenID Connect.
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        authCodeURL := config.AuthCodeURL(state)
        http.Redirect(w, r, authCodeURL, http.StatusFound)
    })

    // Define o callback que o Keycloak deve chamar após o login do usuário.
    // Este caminho deve ser exatamente igual ao RedirectURL configurado acima.
    http.HandleFunc("/auth/callback", func(w http.ResponseWriter, r *http.Request) {
        if err := r.ParseForm(); err != nil {
            http.Error(w, "falha ao ler parâmetros de callback", http.StatusBadRequest)
            return
        }

        // Verifica se o state retornado pelo Keycloak é o mesmo que mandamos.
        // Isso protege contra requisições falsas ou redirecionamentos maliciosos.
        if r.Form.Get("state") != state {
            http.Error(w, "state não corresponde", http.StatusBadRequest)
            return
        }

        // Recebe o código de autorização enviado pelo Keycloak.
        code := r.Form.Get("code")
        if code == "" {
            http.Error(w, "código de autorização ausente", http.StatusBadRequest)
            return
        }

        // Troca o código de autorização por um token de acesso/ID token.
        // O pacote oauth2 já faz a requisição correta ao endpoint de token.
        token, err := config.Exchange(ctx, code)
        if err != nil {
            http.Error(w, "erro ao trocar código pelo token", http.StatusInternalServerError)
            return
        }

        // Aqui, poderia ser feito o parse do ID token e verificação adicional,
        // mas para este exemplo apenas mostramos que a troca foi bem-sucedida.
        fmt.Fprintf(w, "Login bem-sucedido! Token de acesso: %s", token.AccessToken)
    })

    // Inicia o servidor HTTP na porta 8081.
    // Se o servidor não iniciar, a aplicação será encerrada com erro.
    log.Fatal(http.ListenAndServe(":8081", nil))
}

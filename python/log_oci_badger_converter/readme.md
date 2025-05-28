
Essas duas variáveis de ambiente PYTHONDONTWRITEBYTECODE=1 e PYTHONUNBUFFERED=1 no Dockerfile, são **boas práticas comuns em aplicações Python containerizadas**, especialmente em ambientes como Docker. Vamos entender cada uma:

---

## 🧠 Explicação simples

### `PYTHONDONTWRITEBYTECODE=1`

> Impede o Python de gerar arquivos `.pyc` (bytecode) no diretório do projeto.

* Normalmente, ao executar um script Python, o interpretador cria arquivos `.pyc` para acelerar execuções futuras.
* Em ambientes Docker, isso **não é necessário** e pode até **poluir o container** com arquivos desnecessários.
* Deixar desativado (com `=1`) evita isso.

📌 **Analogia:** Imagine que o Python quer guardar "atalhos" (os `.pyc`), mas no container você quer que ele apenas execute e vá embora sem deixar rastros.

---

### `PYTHONUNBUFFERED=1`

> Faz o Python **não armazenar (bufferizar)** a saída padrão (`stdout`) e a saída de erros (`stderr`).

* Isso garante que logs sejam **imediatamente visíveis** no terminal ou no sistema de log do Docker/Kubernetes.
* Sem isso, o log pode **demorar a aparecer**, pois o Python tenta otimizar gravando em lote (buffer).

📌 **Analogia:** É como se o Python estivesse anotando logs em um caderno para mostrar depois. Com `PYTHONUNBUFFERED=1`, ele mostra em tempo real.

---

## ✅ Quando usar?

Essas variáveis são **recomendadas em quase todos os Dockerfiles de aplicações Python**, especialmente quando:

* Você está rodando **scripts pontuais**, como o seu.
* Quer que os logs apareçam **imediatamente** no terminal do `docker logs` ou nos logs do Kubernetes.
* Não quer deixar "lixo" de `.pyc` em camadas do container.

---

# Estágio de Build (usando Maven e OpenJDK)
FROM maven:3.8.4-openjdk-17-slim AS build

# Definir o diretório de trabalho
WORKDIR /workspace

# Copiar o código da aplicação para o contêiner
COPY . /workspace

# Rodar o Maven para compilar e empacotar a aplicação
RUN mvn clean package -DskipTests -Pnative

# Estágio Final (usando imagem distroless para execução)
FROM quay.io/quarkus/quarkus-distroless-image:2.0

# Definir o diretório de trabalho para o estágio final
WORKDIR /work

# Copiar a aplicação compilada do estágio anterior
COPY --from=build /workspace/target/*-runner /work/application

# Definir o comando para rodar a aplicação
CMD ["/work/application"]

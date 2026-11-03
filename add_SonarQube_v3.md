# 🚀 Multi-Container Web App with Nginx, Flask, PostgreSQL, Observability & SonarQube

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

Projeto prático de infraestrutura containerizada desenvolvendo um ambiente web resiliente em arquitetura de microsserviços e instrumentado com uma stack completa de **Observabilidade, Monitoramento e Governança de Código (DevSecOps)**.

O ambiente simula uma aplicação pronta para produção utilizando proxy reverso Nginx, backend Flask em Python, banco de dados relacional PostgreSQL, **Prometheus**, **Grafana** e **cAdvisor** para telemetria em tempo real, além de um servidor **SonarQube** dedicado para análise estática de código e identificação de vulnerabilidades.

---

## 📌 Arquitetura da Solução

A aplicação é composta por 8 serviços orquestrados via **Docker Compose** operando na mesma rede bridge virtual (`lab-net`):

```text
                                [ Cliente / Navegador ]
                                           │
         ┌───────────────────┬─────────────┼───────────────────┬───────────────────┐
         │ (Porta 8080)      │ (Porta 9000)│ (Porta 9090)      │ (Porta 3000)      │ (Porta 8081)
         ▼                   ▼             ▼                   ▼                   ▼
┌───────────────────┐ ┌─────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│   Nginx Proxy     │ │  SonarQube  │ │    Prometheus     │◄┤      Grafana      │ │     cAdvisor      │
└─────────┬─────────┘ └──────┬──────┘ └─────────▲─────────┘ └───────────────────┘ └─────────┬─────────┘
          │ (Interna)        │ (Interna)        │ (Scrape)                                  │
          ▼                  ▼                  │                                           │
┌───────────────────┐ ┌─────────────┐           │                                           │
│   Flask Web App   │ │  Sonar-DB   │           ├───────────────────────────────────────────┘
└─────────┬─────────┘ └─────────────┘           │
          │ (Interna: 5432)                     │
          ▼                                     │
┌───────────────────┐                           │
│   PostgreSQL DB   ├───────────────────────────┘
└───────────────────┘
```

---

## ⚙️ Tecnologias e Ferramentas

- **Orquestração & Containerização:** Docker, Docker Compose
- **Proxy Reverso & Servidor Web:** Nginx
- **Linguagem & Framework:** Python 3.10, Flask, Psycopg2, `prometheus-flask-exporter`
- **Bancos de Dados:** PostgreSQL 16 (Aplicação) e PostgreSQL 15 (SonarQube)
- **Observabilidade & Telemetria:** Prometheus, Grafana, cAdvisor
- **Qualidade & Segurança de Código:** SonarQube LTS Community, Sonar Scanner CLI
- **Persistência de Dados:** Named Volumes (`pgdata`, `sonar_db_data`, `sonarqube_data`, `sonarqube_extensions`, `sonarqube_logs`)
- **Sistema Operacional Host:** Ubuntu Linux / WSL2

---

## 🌐 Mapeamento de Portas & Serviços

| Serviço | Container | Porta Externa | Função / Descrição |
| :--- | :--- | :---: | :--- |
| **Nginx** | `nginx_proxy` | `8080` | Proxy Reverso e Ponto de Entrada Web |
| **Flask** | `flask_web_app` | `5000` | Backend Python (Rede Interna) |
| **PostgreSQL DB** | `postgres_db` | `5432` | Banco de Dados Relacional da Aplicação |
| **Prometheus** | `prometheus_server` | `9090` | Servidor de Coleta de Métricas |
| **Grafana** | `grafana_dashboard` | `3000` | Interface Visual para Dashboards |
| **cAdvisor** | `cadvisor_metrics` | `8081` | Monitoramento de Recursos dos Containers |
| **SonarQube** | `sonarqube_server` | `9000` | Servidor de Análise Estática de Código |
| **Sonar DB** | `sonars_db` | `5432` (Interna) | Banco de Dados Exclusivo do SonarQube |

---

## ⚙️ Pré-requisitos e Configuração do Host (WSL2 / Linux)

O motor interno de busca do SonarQube (Elasticsearch) requer um limite maior de mapeamento de memória virtual no kernel do Linux.

### Configurar o parâmetro do kernel:
```bash
# Aplicação temporária
sudo sysctl -w vm.max_map_count=524288
```

Para tornar permanente, insira a linha `vm.max_map_count=524288` dentro do arquivo `/etc/sysctl.conf` e execute `sudo sysctl -p`.

---

## 🛠️ Como Executar o Laboratório

1. **Subir a stack completa de aplicação, observabilidade e qualidade:**
   ```bash
   docker compose up -d --build
   ```

2. **Verificar a execução dos containers:**
   ```bash
   docker ps
   ```

3. **Acessar as interfaces web:**
   - **Aplicação Web:** [http://localhost:8080](http://localhost:8080)
   - **Prometheus Metrics:** [http://localhost:9090](http://localhost:9090)
   - **Grafana Dashboards:** [http://localhost:3000](http://localhost:3000) *(Credenciais: `admin` / `admin`)*
   - **SonarQube:** [http://localhost:9000](http://localhost:9000) *(Credenciais iniciais: `admin` / `admin`)*

--- 

## 🔍 Análise de Código Estática com SonarQube (Atividade Realizada)

Para realizar auditorias de segurança e qualidade de código localmente sem depender de pipelines de CI na nuvem:

### 1. Download e Instalação do Sonar Scanner CLI via `wget`
No terminal do WSL2, dentro da pasta do projeto, faça o download do scanner oficial:

```bash
# Baixar o pacote zip da CLI
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip

# Descompactar o arquivo
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
```

### 2. Configurar o Projeto e Token no SonarQube
1. Acesse `http://localhost:9000`.
2. Altere a senha padrão do usuário `admin`.
3. Selecione a opção **Create a project manually** e defina a chave do projeto (ex: `Lab-Web-DB-Flask`).
4. Gere um **Token de Acesso** para o projeto.

### 3. Executar o Scanner no Código Local
Execute o binário do Sonar Scanner indicando a raiz do código fonte e o token gerado:

```bash
./sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner \
  -Dsonar.projectKey=Lab-Web-DB-Flask \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=SEU_TOKEN_AQUI
```

### 4. Resultados da Análise de Hoje
A varredura foi concluída com sucesso no código do projeto, trazendo visibilidade direta sobre **Security Hotspots** (como avisos de cópia recursiva no `Dockerfile` e validações de rotas CSRF no Flask), permitindo a revisão contínua das melhores práticas de segurança antes da publicação do código.

---

## 🧹 Finalizando e Resetando o Ambiente

- **Parar os containers:**
  ```bash
  docker compose stop
  ```

- **Remover containers mantendo os dados salvos:**
  ```bash
  docker compose down
  ```

- **Reset completo (removendo volumes e bancos):**
  ```bash
  docker compose down -v
  ```

---
*Projeto desenvolvido por [Silvio Luiz](https://github.com/silvio69luiz) como parte dos laboratórios práticos para consolidação de carreira em DevOps, Cloud Engineering e SRE.*
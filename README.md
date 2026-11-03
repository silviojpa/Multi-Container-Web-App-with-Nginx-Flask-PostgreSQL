# 🚀 Multi-Container Web App with Nginx, Flask, PostgreSQL & Observability Stack

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

Projeto prático de infraestrutura containerizada desenvolvendo um ambiente web resiliente em arquitetura de microsserviços e instrumentado com uma stack completa de **Observabilidade e Monitoramento**. 

O ambiente simula uma aplicação pronta para produção utilizando proxy reverso Nginx, backend Flask em Python, banco de dados relacional PostgreSQL, além de **Prometheus**, **Grafana** e **cAdvisor** para telemetria de métricas de aplicação e recursos de infraestrutura em tempo real.

---

## 📌 Arquitetura da Solução

A aplicação é composta por 6 serviços orquestrados via **Docker Compose** operando na mesma rede bridge virtual (`lab-net`):

```text
                                [ Cliente / Navegador ]
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │ (Porta 8080)                    │ (Porta 9090)                    │ (Porta 3000)
         ▼                                 ▼                                 ▼
┌───────────────────┐             ┌───────────────────┐             ┌───────────────────┐
│   Nginx Proxy     │             │    Prometheus     │◄────────────┤      Grafana      │
└─────────┬─────────┘             └─────────▲─────────┘             └───────────────────┘
          │ (Rede Interna: 5000)            │ (Scrape de Métricas)
          ▼                                 │
┌───────────────────┐                       │
│   Flask Web App   ├───────────────────────┼───► Metrics (/metrics via prometheus-flask-exporter)
└─────────┬─────────┘                       │
          │ (Rede Interna: 5432)            │
          ▼                                 │
┌───────────────────┐                       │
│   PostgreSQL DB   │                       │
└───────────────────┘                       │
                                            │
┌───────────────────┐                       │
│     cAdvisor      ├───────────────────────┘
└───────────────────┘ (Métricas de CPU, Memória e Rede dos Containers)
```

---

## ⚙️ Tecnologias e Ferramentas

- **Orquestração & Containerização:** Docker, Docker Compose
- **Proxy Reverso & Servidor Web:** Nginx
- **Linguagem & Framework:** Python 3.10, Flask, Psycopg2, `prometheus-flask-exporter`
- **Banco de Dados:** PostgreSQL 16
- **Observabilidade & Telemetria:** Prometheus, Grafana, cAdvisor
- **Persistência de Dados:** Named Volume (`pgdata`)
- **Sistema Operacional Host:** Ubuntu Linux / WSL2

---

## 📊 Stack de Observabilidade & Monitoramento

A camada de observabilidade foi implementada para fornecer visibilidade total sobre a saúde da aplicação e da infraestrutura:

1. **Instrumentação da Aplicação (Flask Metrics):**
   - Exposição automática de métricas na rota `/metrics` utilizando a biblioteca `prometheus-flask-exporter`.
   - Monitoramento de volume de requisições HTTP, taxas de erro por código de status, latência e duração das requisições.
2. **Telemetria de Infraestrutura (cAdvisor):**
   - Coleta contínua do uso de recursos (CPU, memória RAM, I/O de disco e tráfego de rede) de cada container individual da stack.
3. **Coleta & Armazenamento (Prometheus):**
   - Agente centralizador realizando *scraping* periódico de métricas nos alvos configurados (`web-app:5000` e `cadvisor:8080`).
4. **Visualização em Dashboards (Grafana):**
   - Painéis gráficos para análise em tempo real da performance das APIs e do consumo da infraestrutura host.

---

## 🌐 Mapeamento de Portas & Serviços

| Serviço | Container | Porta Externa | Função / Descrição |
| :--- | :--- | :---: | :--- |
| **Nginx** | `nginx_proxy` | `8080` | Proxy Reverso e Ponto de Entrada Web |
| **Flask** | `flask_web_app` | `5000` | Backend Python (Rede Interna / Debug) |
| **PostgreSQL** | `postgres_db` | `5432` | Banco de Dados Relacional |
| **Prometheus** | `prometheus_server` | `9090` | Servidor de Coleta e Consultas PromQL |
| **Grafana** | `grafana_dashboard` | `3000` | Interface Visual para Dashboards |
| **cAdvisor** | `cadvisor_metrics` | `8080` / `8081` | Monitoramento de Recursos dos Containers |

---

## 🛠️ Como Executar o Laboratório

### Pré-requisitos
- Docker Engine e Docker Compose instalados.
- Git.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/lab-web-db.git
   cd lab-web-db
   ```

2. **Subir toda a stack de aplicação e monitoramento:**
   ```bash
   docker compose up -d --build
   ```

3. **Acessar as interfaces do ambiente:**
   - **Aplicação Web:** [http://localhost:8080](http://localhost:8080)
   - **Prometheus Metrics:** [http://localhost:9090](http://localhost:9090)
   - **Grafana Dashboards:** [http://localhost:3000](http://localhost:3000) *(Credenciais padrão: `admin` / `admin`)*

4. **Verificar o status dos containers:**
   ```bash
   docker ps
   ```

---

## 🔍 Consultando o Banco de Dados via CLI

Para inspecionar as tabelas diretamente no container PostgreSQL:

```bash
docker exec -it postgres_db psql -U postgres -d usuarios_db
```

Comandos SQL úteis:
```sql
-- Listar tabelas
\dt

-- Consultar cadastros
SELECT * FROM usuarios;

-- Sair
\q
```

---

## 🧹 Finalizando o Ambiente

Para parar todos os serviços mantendo a persistência dos dados:
```bash
docker compose stop
```

Para remover os containers mantendo os volumes de banco e métricas:
```bash
docker compose down
```

Para resetar completamente o ambiente (removendo containers, redes e volumes):
```bash
docker compose down -v
```

---
*Projeto desenvolvido por [Silvio Luiz](https://github.com/silvio69luiz) como parte dos laboratórios práticos para a consolidação de carreira em DevOps, Cloud Engineering e SRE.*

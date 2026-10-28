# 🚀 Multi-Container Web App with Nginx, Flask & PostgreSQL

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

Projeto prático de infraestrutura containerizada desenvolvendo um ambiente web resiliente em arquitetura de microsserviços. O ambiente simula uma aplicação pronta para produção utilizando um proxy reverso Nginx, backend Flask em Python e banco de dados relacional PostgreSQL com persistência de dados.

---

## 📌 Arquitetura da Solução

A aplicação é composta por 3 serviços orquestrados via **Docker Compose** operando na mesma rede bridge virtual (`app-net`):

```text
[ Cliente / Browser ]
          │
          │ (Porta 8080)
          ▼
┌───────────────────┐
│   Nginx Proxy     │ (Reverse Proxy & Frontend Gateway)
└─────────┬─────────┘
          │ (Rede Interna: 5000)
          ▼
┌───────────────────┐
│   Flask Web App   │ (Backend Python - Lógica & Renderização)
└─────────┬─────────┘
          │ (Rede Interna: 5432)
          ▼
┌───────────────────┐
│   PostgreSQL DB   │ (Banco de Dados Relacional + Volume Persistente)
└───────────────────┘
```

---

## ⚙️ Tecnologias e Ferramentas

- **Orquestração & Containerização:** Docker, Docker Compose
- **Proxy Reverso & Servidor Web:** Nginx
- **Linguagem & Framework:** Python 3.10, Flask, Psycopg2
- **Banco de Dados:** PostgreSQL 16
- **Persistência de Dados:** Named Volume (`pgdata`)
- **Sistema Operacional de Host:** Ubuntu Linux / WSL2

---

## 🎯 Destaques do Projeto & Resolução de Desafios DevOps

Durante a implementação do laboratório, foram aplicados conceitos avançados de engenharia de confiabilidade e infraestrutura:

1. **Tratamento de *Race Conditions* (Resiliência):**
   - Implementação de *retry logic* no backend Python para aguardar a completa inicialização e prontidão do PostgreSQL antes de tentar executar migrações de tabela (`init_db`), prevenindo erros no *cold start*.
2. **Proxy Reverso Nginx:**
   - Isolamento e segurança da aplicação Flask, expondo publicamente apenas a porta `8080` do Nginx enquanto a comunicação interna entre os containers ocorre de forma privada.
3. **Persistência & Migração de Dados (Database Migrations):**
   - Configuração de volume persistente para manter a integridade dos cadastros mesmo durante reinicializações.
   - Aplicação prática de alterações de schema via `ALTER TABLE` sem indisponibilidade ou perda dos dados existentes.

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

2. **Subir a pilha de containers:**
   ```bash
   docker compose up -d --build
   ```

3. **Acessar a aplicação:**
   Abra o navegador e acesse:
   ```text
   http://localhost:8080
   ```

4. **Verificar os logs dos serviços:**
   ```bash
   docker compose logs -f
   ```

---

## 🔍 Consultando o Banco de Dados diretamente via CLI

Para inspecionar as tabelas diretamente no container PostgreSQL:

```bash
docker exec -it postgres_db psql -U postgres -d usuarios_db
```

Comandos SQL úteis:
```sql
-- Listar tabelas
\dt

-- Consultar dados
SELECT * FROM usuarios;

-- Sair do terminal psql
\q
```

---

## 🧹 Finalizando o Ambiente

Para parar os serviços mantendo os dados gravados:
```bash
docker compose stop
```

Para remover os containers mantendo os dados:
```bash
docker compose down
```

Para resetar completamente o ambiente (removendo containers e volumes):
```bash
docker compose down -v
```

---
*Projeto desenvolvido por [Silvio Luiz](https://github.com/silvio69luiz) como parte dos laboratórios práticos para a consolidação de carreira em DevOps, Cloud Engineering e SRE.*
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
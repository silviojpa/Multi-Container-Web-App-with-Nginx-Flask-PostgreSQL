## Passo 1: Adicionar o cAdvisor no docker-compose.yml
- Abra o seu arquivo docker-compose.yml e adicione o serviço do cadvisor logo abaixo dos serviços de monitoramento que já temos:

````YAML
# NOVO: cAdvisor para métricas de recursos dos containers (CPU, Memória, Rede)
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.47.2
    container_name: cadvisor_metrics
    ports:
      - "8080:8080" # Atenção: se a porta 8080 já estiver usada pelo Nginx, ajuste aqui para "8081:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - lab-net
````
* (Nota: Se o seu Nginx já estiver usando a porta 8080 para expor o Flask, mude a porta externa do cAdvisor para "8081:8080" para evitar conflito de portas no host).

## Passo 2: Atualizar o arquivo prometheus/prometheus.yml
- Para que o Prometheus comece a puxar essas novas métricas de recursos, adicione um novo job no seu arquivo de configuração do Prometheus:

````YAML
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask-app-metrics'
    static_configs:
      - targets: ['web-app:5000']

  # NOVO: Job para coletar métricas dos containers via cAdvisor
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
````

## Passo 3: Subir a nova stack atualizada
- Salve os arquivos alterados e execute o comando no terminal para recriar e subir os serviços:

````Bash
docker compose up -d --build
````

## Passo 4: Visualizar no Grafana
1. Volte ao seu painel do Grafana (http://localhost:3000).
2. Crie um New panel.
3. Selecione a fonte de dados do Prometheus.
* Teste uma query de uso de memória dos containers usando o cAdvisor, por exemplo:

````Snippet de código
container_memory_usage_bytes{container_label_com_docker_compose_service!=""}
````
Salve o painel e você terá o monitoramento completo de infraestrutura e aplicação lado a lado!

# 🛰️ iFood Demand Sentinel
### 🗺️ Plataforma de Inteligência Geospacial & Mapeamento de Demanda

<p align="center">
  <img src="https://img.shields.io/badge/Java_17-Spring_Boot-ED8B00?style=for-the-badge&logo=java&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-PostGIS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Uber_H3-000000?style=for-the-badge&logo=uber&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

---

## 📌 Visão Geral
O **iFood Demand Sentinel** é uma solução fim a fim de engenharia e análise de dados desenvolvida para identificar oportunidades de expansão de mercado e áreas com alta demanda não atendida. 

A arquitetura combina um módulo em **Java** para simulação de eventos de busca de clientes em alta escala, web scraping em **Python (Firecrawl)** para mapeamento da oferta de restaurantes locais, streaming via **Apache Kafka**, indexação geospacial hexagonal **Uber H3**, geração de relatórios analíticos via **Gemini API** e um painel executivo interativo em **Streamlit**.

---

## 📐 Arquitetura da Solução

```text
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│   1. ORIGEM DOS DADOS   │ ───► │  2. INGESTÃO DE DADOS   │ ───► │  3. PROCESSAMENTO & H3  │
│ (Java Producer/Firecrawl)│     │  (Kafka + Zookeeper)    │      │  (Python + Uber H3)     │
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                               │
                                                                               ▼
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│      5. DASHBOARD       │ ◄─── │  5. IA & RELATÓRIOS     │ ◄─── │    4. ARMAZENAMENTO     │
│   (Streamlit + Folium)  │      │   (Gemini API Agent)    │      │  (PostgreSQL / PostGIS) │
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
Origem dos Dados: Simulação de buscas de usuários implementada em Java (ingestor-java) enviando payloads ao Kafka, combinada à raspagem de ofertas ativas de restaurantes via scraper_firecrawl.py.Ingestão: Cluster de mensageria gerenciado via Docker com Apache Kafka e Zookeeper para mensageria assíncrona de alta disponibilidade.Processamento Espacial: Consumidor Python (kafka_consumer.py) que processa mensagens em tempo real e calcula os índices hexagonais Uber H3 (h3_analytics.py).Armazenamento Analítico: Banco PostgreSQL com PostGIS estruturado em modelo Star Schema para suporte a consultas geospaciais avançadas (spatial_queries.sql).Inteligência & Dashboard: Agente automatizado (maestro_agent.py) integrado à API do Google Gemini para síntese de relatórios em linguagem natural e interface de visualização construída com Streamlit e mapas interativos Folium.💻 Tecnologias e MódulosCamadaTecnologias / BibliotecasIngestão JavaJava 17, Maven, Spring Boot, Kafka Producer ClientPipeline PythonPython 3.10+, Firecrawl, Kafka-Python, Uber H3, Pandas, psycopg2InfraestruturaDocker, Docker Compose, Apache Kafka, ZookeeperBanco de DadosPostgreSQL, PostGIS, SQL DDL (Star Schema)Inteligência ArtificialGoogle Gemini API (Agente Maestro)Interface VisualStreamlit, Folium (Leaflet maps)📁 Estrutura do RepositórioPlaintextifood-demand-sentinel/
├── docker-compose.yml          # Serviços containerizados (Kafka, Zookeeper, PostgreSQL)
├── README.md                   # Documentação técnica do projeto
│
├── ingestor-java/              # Módulo Java (Simulação e Engenharia de Software)
│   ├── pom.xml                 # Gerenciador de dependências Maven
│   └── src/main/java/com/ifood/
│       ├── DemandProducer.java # Producer Kafka que dispara eventos de busca
│       └── model/SearchEvent.java # Modelo de dados dos eventos
│
├── pipeline-python/            # Módulo Python (Engenharia de Dados & IA)
│   ├── requirements.txt        # Dependências Python (pandas, psycopg2, h3, etc.)
│   ├── scraper_firecrawl.py    # Coleta automatizada de ofertas de restaurantes
│   ├── kafka_consumer.py       # Consumidor Kafka e persistência no PostgreSQL
│   ├── h3_analytics.py         # Módulo de processamento espacial Uber H3
│   └── maestro_agent.py        # Integração com Gemini API para relatórios executivos
│
├── database/                   # Módulo de Banco de Dados
│   ├── schema.sql              # DDL de criação do banco e tabelas (Star Schema)
│   └── spatial_queries.sql     # Consultas analíticas geospaciais otimizadas
│
└── dashboard/                  # Módulo de Visualização
    └── app.py                  # Painel interativo em Streamlit com mapas Folium
⚡ Instruções de ExecuçãoPré-requisitosDocker e Docker ComposeJDK 17+ e MavenPython 3.10+Instância/Credenciais do PostgreSQL e Google Gemini API Key1. Infraestrutura DockerNa raiz do repositório, suba o cluster contendo Kafka, Zookeeper e PostgreSQL:Bashdocker-compose up -d
2. Banco de DadosConecte-se ao PostgreSQL criado pelo Docker e execute os scripts SQL na ordem abaixo:Bashpsql -h localhost -U postgres -d ifood_sentinel -f database/schema.sql
psql -h localhost -U postgres -d ifood_sentinel -f database/spatial_queries.sql
3. Módulo Ingestor (Java)Acesse a pasta do projeto Java, compile com Maven e inicie o gerador de eventos:Bashcd ingestor-java
mvn clean install
mvn exec:java -Dexec.mainClass="com.ifood.DemandProducer"
4. Pipeline de Dados (Python)Em outro terminal, crie um ambiente virtual na pasta do pipeline, instale as dependências e inicie a ingestão/processamento:Bashcd pipeline-python
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Executar a coleta de oferta via scraping (opcional):Bashpython scraper_firecrawl.py
Iniciar o consumidor Kafka para processar e indexar via Uber H3:Bashpython kafka_consumer.py
5. Aplicação Dashboard (Streamlit)Em um novo terminal com o ambiente virtual ativado, inicie o painel executivo:Bashcd dashboard
streamlit run app.py

# 🛰️ iFood Demand Sentinel
### 🗺️ Plataforma de Inteligência Geospacial & Mapeamento de Demanda

<p align="center">
  <img src="https://img.shields.io/badge/Java_21-Spring_Boot-ED8B00?style=for-the-badge&logo=java&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Maven-C71A36?style=for-the-badge&logo=apache-maven&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-PostGIS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Uber_H3-000000?style=for-the-badge&logo=uber&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

---

## 📌 Visão Geral
O **iFood Demand Sentinel** é uma solução fim a fim de engenharia e análise de dados desenvolvida para identificar oportunidades de expansão de mercado e áreas com alta demanda não atendidas.
<img width="1915" height="929" alt="Captura de tela de 2026-09-08 23-57-55" src="https://github.com/user-attachments/assets/ea5d8052-e92e-41f4-b2a1-8b1e59e22fff" />

A arquitetura combina um módulo em **Java** para simulação de eventos de busca de clientes em alta escala, streaming via **Apache Kafka**, indexação geospacial hexagonal **Uber H3** e um painel executivo interativo em **Streamlit**.

---

## 📐 Arquitetura da Solução

```text
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│   1. ORIGEM DOS DADOS   │ ───► │  2. INGESTÃO DE DADOS   │ ───► │  3. PROCESSAMENTO & H3  │
│     (Java Producer)     │      │  (Kafka + Zookeeper)    │      │  (Python + Uber H3)     │
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                               │
                                                                               ▼
┌─────────────────────────┐                                       ┌─────────────────────────┐
│      5. DASHBOARD       │ ◄──────────────────────────────────── │    4. ARMAZENAMENTO     │
│   (Streamlit + Folium)  │                                       │  (PostgreSQL / PostGIS) │
└─────────────────────────┘                                       └─────────────────────────┘
Origem dos Dados: Simulação de buscas de usuários implementada em Java (ingestor-java) enviando payloads ao Kafka.Ingestão: Cluster de mensageria gerenciado via Docker com Apache Kafka e Zookeeper para mensageria assíncrona.Processamento Espacial: Consumidor Python (consumidor.py) que processa mensagens e calcula os índices hexagonais Uber H3.Armazenamento Analítico: Banco PostgreSQL com extensão PostGIS (schema.sql).Dashboard: Interface de visualização em Streamlit com mapas interativos em Folium.💻 Tecnologias e MódulosCamadaTecnologias / BibliotecasIngestão JavaJava 21, Apache Maven, Spring Boot, Kafka Producer ClientPipeline PythonPython 3.10+, Kafka-Python, Uber H3, Pandas, psycopg2InfraestruturaDocker, Docker Compose, Apache Kafka, ZookeeperBanco de DadosPostgreSQL, PostGISInterface VisualStreamlit, Folium📁 Estrutura do RepositórioPlaintextifood-demand-sentinel/
├── docker-compose.yml          # Serviços containerizados (Kafka, Zookeeper, PostgreSQL)
├── README.md                   # Documentação técnica do projeto
│
├── consumer-python/            # Módulo de consumo e processamento
│   ├── consumidor.py           # Consumidor Kafka e conversão Uber H3
│   └── requirements.txt        # Dependências Python
│
├── dashboard/                  # Módulo de visualização
│   └── app.py                  # Painel interativo em Streamlit
│
├── database-schema/            # Estrutura de banco de dados
│   └── schema.sql              # DDL de criação do banco e tabelas
│
└── ingestor-java/              # Módulo gerador de eventos
    ├── pom.xml                 # Gerenciador de dependências Maven
    └── src/main/java/com/ifood/
        ├── DemandProducer.java # Producer Kafka
        └── searchEvent.java    # Modelo do evento de busca
⚡ Instruções de ExecuçãoPré-requisitosDocker e Docker ComposeJDK 21+ e Apache MavenPython 3.10+PostgreSQL1. Infraestrutura DockerNa raiz do repositório, suba o cluster contendo Kafka, Zookeeper e PostgreSQL:Bashdocker-compose up -d
2. Banco de DadosConecte-se ao PostgreSQL criado pelo Docker e execute o script SQL:Bashpsql -h localhost -U postgres -d ifood_sentinel -f database-schema/schema.sql
3. Módulo Ingestor (Java)Acesse a pasta do projeto Java, compile com Maven e inicie o gerador de eventos:Bashcd ingestor-java
mvn clean install
mvn exec:java -Dexec.mainClass="com.ifood.DemandProducer"
4. Pipeline de Dados (Python)Em outro terminal, acesse a pasta do consumidor Python, instale as dependências e execute:Bashcd consumer-python
pip install -r requirements.txt
python consumidor.py
5. Aplicação Dashboard (Streamlit)Em um novo terminal, inicie a interface visual:Bashcd dashboard
streamlit run app.py

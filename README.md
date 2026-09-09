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

A arquitetura combina um módulo em **Java** para simulação de eventos de busca de clientes em alta escala, streaming via **Apache Kafka**, indexação geospacial hexagonal **Uber H3** e um painel executivo interativo em **Streamlit**.

---

## 📊 Painel Executivo & Mapeamento Geoespacial

<p align="center">
  <img src="URL_DA_SUA_IMAGEM_AQUI.png" alt="iFood Demand Sentinel Dashboard" width="100%">
</p>

* **Métricas em Tempo Real:** Monitoramento do volume de buscas, usuários ativos, item mais buscado e hexágonos atingidos.
* **Inteligência Espacial:** Indexação hexagonal via **Uber H3** sobreposta em mapa interativo com Folium.
* **Rank de Demandas:** Agregação de pesquisas por categoria de produto (ex: pastel, açaí, pizza) para identificação estratégica de "desertos de oferta".

---

## 📐 Arquitetura da Solução

```text
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│   1. ORIGEM DOS DADOS   │ ───► │  2. INGESTÃO DE DADOS   │ ───► │  3. PROCESSAMENTO & H3  │
│      (Java Producer)    │      │  (Kafka + Zookeeper)    │      │  (Python + Uber H3)     │
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                               │
                                                                               ▼
┌─────────────────────────┐                                       ┌─────────────────────────┐
│      5. DASHBOARD       │ ◄──────────────────────────────────── │    4. ARMAZENAMENTO     │
│   (Streamlit + Folium)  │                                       │  (PostgreSQL / PostGIS) │
└─────────────────────────┘                                       └─────────────────────────┘

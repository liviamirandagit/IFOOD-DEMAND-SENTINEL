# 🛰️ iFood Demand Sentinel
###-> Plataforma de Inteligência Geospacial & Mapeamento de Demanda

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
## || Visão Geral ||
O **iFood Demand Sentinel** é uma pipeline "End-to-end" de engenharia e análise de dados desenvolvida para identificar oportunidades de expansão de mercado e áreas com alta demanda não atendidas.
<img width="1915" height="929" alt="Captura de tela de 2026-09-08 23-57-55" src="https://github.com/user-attachments/assets/ea5d8052-e92e-41f4-b2a1-8b1e59e22fff" />
---
## || Arquitetura ||

O projeto simula um fluxo de dados de ponta a ponta: as buscas são geradas e coletadas, passam pela ingestão em tempo real, são processadas e indexadas com H3, armazenadas no PostgreSQL/PostGIS e, por fim, utilizadas na visualização e análise dos dados.

<p align="center">
  <img width="619" height="741" alt="Captura de tela de 2026-09-09 00-13-21" src="https://github.com/user-attachments/assets/9fbefa3f-51e5-4ea7-883f-28d8db7910a1" />
</p>
---
## || PostgreSQL/PostGIS — análise dos registros ||
Os registros armazenam os eventos de busca realizados pelos usuários, incluindo informações como o termo pesquisado, o usuário, o momento da busca e o índice H3 correspondente à localização. A partir desses dados, as consultas SQL permitem identificar regiões com maior volume de buscas, os tipos de comida mais pesquisados e a quantidade de usuários únicos em cada área.

<img width="1809" height="845" alt="Captura de tela de 2026-09-08 23-22-23" src="https://github.com/user-attachments/assets/f002eb6d-cd4f-46d5-805d-248115caadb0" />


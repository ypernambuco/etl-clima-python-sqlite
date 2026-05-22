# etl-clima-python-sqlite

Projeto simples de ETL para consumir dados de clima de uma API pública, transformar os dados com pandas e salvar o resultado em SQLite.

A ideia é praticar um fluxo comum em dados:

```text
API -> pandas -> SQLite -> métricas simples
```

O projeto ainda está em evolução e foi pensado para ser pequeno, organizado e fácil de explicar.

## Objetivo

- consumir dados diários de clima pela API Open-Meteo;
- organizar os dados em formato tabular com pandas;
- salvar os dados tratados em um banco SQLite local;
- gerar métricas simples por cidade.

## Estrutura

```text
etl-clima-python-sqlite/
|-- data/
|   |-- raw/
|   |-- processed/
|-- database/
|-- logs/
|-- sql/
|-- src/
|-- README.md
|-- requirements.txt
```

## Status

Projeto em construção.

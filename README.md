# etl-clima-python-sqlite

Projeto simples de ETL para consumir dados de clima de uma API pública, transformar os dados com pandas, salvar em SQLite e gerar métricas básicas por cidade.

A ideia é praticar um fluxo comum em dados:

```text
API -> pandas -> SQLite -> métricas simples
```

A ideia é manter o projeto pequeno, organizado e fácil de explicar em entrevista. Ele não tenta parecer um sistema de produção.

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
|   |-- metricas_clima.sql
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- extract.py
|   |-- load.py
|   |-- logger.py
|   |-- main.py
|   |-- metrics.py
|   |-- transform.py
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## Fonte Dos Dados

Os dados são consumidos da API pública da Open-Meteo:

https://open-meteo.com/en/docs

Neste projeto, a consulta usa previsão diária para algumas capitais brasileiras:

- São Paulo
- Rio de Janeiro
- Belo Horizonte
- Brasília
- Curitiba
- Recife

## Como Rodar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o pipeline:

```bash
python -m src.main
```

Também é possível escolher a quantidade de dias de previsão:

```bash
python -m src.main --forecast-days 3
```

## O Que O Pipeline Faz

1. Consulta a API da Open-Meteo para cada cidade configurada.
2. Salva uma cópia do JSON bruto em `data/raw`.
3. Transforma os dados diários com pandas.
4. Salva um CSV tratado em `data/processed`.
5. Carrega os dados em SQLite na tabela `clima_diario`.
6. Calcula métricas simples por cidade.
7. Salva as métricas em `data/processed/metricas_clima.csv`.

Os arquivos gerados são ignorados pelo Git para manter o repositório limpo.

## Métricas Geradas

As métricas principais são:

- dias analisados;
- temperatura média;
- maior temperatura;
- menor temperatura;
- precipitação acumulada;
- quantidade de dias com chuva.

A consulta SQL usada para gerar essas métricas está em `sql/metricas_clima.sql`.

## Projeto Relacionado

Os dados tratados deste ETL também são usados em um dashboard simples feito com Streamlit:

https://github.com/ypernambuco/dashboard-clima-streamlit

## Aprendizados

Neste projeto, pratiquei a leitura de dados vindos de uma API, a transformação de JSON em tabela com pandas e a carga em um banco SQLite local.

Também foi útil separar o código em etapas simples: extração, transformação, carga e métricas. A separação deixa o projeto mais fácil de testar e explicar, sem precisar usar ferramentas mais complexas.

## Limitações

Este projeto ainda tem algumas limitações:

- usa poucas cidades;
- consulta apenas dados de previsão diária;
- usa SQLite local, sem banco em servidor;
- não tem agendamento automático;
- a visualização em dashboard fica em um repositório separado;
- não possui testes automatizados ainda;
- depende da disponibilidade da API no momento da execução.

Essas limitações são intencionais para manter o escopo simples e adequado a um projeto júnior.

## Próximos Passos

- Adicionar testes para as transformações principais.
- Permitir configurar cidades por arquivo CSV.
- Criar mais algumas consultas SQL de análise.
- Gerar um pequeno relatório em CSV com os principais indicadores.

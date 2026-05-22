# etl-clima-python-sqlite

Projeto simples de ETL para consumir dados de clima de uma API pública, transformar os dados com pandas, salvar em SQLite e gerar métricas básicas por cidade.

O pipeline busca os últimos 7 dias de dados recentes e mantém a previsão futura, usando a Forecast API da Open-Meteo com o parâmetro `past_days=7`.

A ideia é praticar um fluxo comum em dados:

```text
API -> pandas -> SQLite -> métricas simples
```

O objetivo foi manter o projeto pequeno, organizado e fácil de explicar em entrevista.

## Objetivo

- consumir dados diários de clima pela API Open-Meteo;
- buscar dados recentes dos últimos 7 dias;
- manter dados de previsão futura;
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
|-- assets/
|   |-- screenshots/
|   |   |-- terminal-etl.png
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

Neste projeto, a consulta usa dados diários para algumas capitais brasileiras, juntando histórico recente e previsão em uma única base.

A Forecast API da Open-Meteo aceita o parâmetro `past_days`, com valores de `0` a `92`. Por isso, o projeto usa `past_days=7` no mesmo endpoint de previsão, sem precisar chamar a Archive API para este escopo.

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

Também dá para escolher quantos dias de previsão consultar:

```bash
python -m src.main --forecast-days 3
```

Também é possível ajustar a quantidade de dias recentes buscados:

```bash
python -m src.main --past-days 7
```

## Screenshot

### ETL rodando no terminal

![Execução do ETL de clima no terminal](assets/screenshots/terminal-etl.png)

O print fica logo depois do comando de execução para mostrar o pipeline funcionando na prática, antes da explicação etapa por etapa.

## O Que O Pipeline Faz

1. Consulta a API da Open-Meteo para cada cidade configurada.
2. Salva uma cópia do JSON bruto em `data/raw`.
3. Transforma os dados diários com pandas.
4. Salva um CSV tratado em `data/processed`.
5. Carrega os dados em SQLite na tabela `clima_diario`.
6. Calcula métricas simples por cidade.
7. Salva as métricas em `data/processed/metricas_clima.csv`.

O CSV e a tabela SQLite incluem a coluna `tipo_dado`, com os valores:

- `historico`: datas anteriores ao dia da coleta;
- `previsao`: o dia da coleta e os próximos dias.

Os arquivos gerados são ignorados pelo Git para manter o repositório mais limpo.

## Métricas Geradas

As métricas principais são:

- dias analisados;
- temperatura média;
- maior temperatura;
- menor temperatura;
- precipitação acumulada;
- quantidade de dias com chuva.

A consulta SQL usada para gerar essas métricas está em `sql/metricas_clima.sql`.

Exemplo de saída das métricas:

| cidade | dias_analisados | temperatura_media_c | precipitacao_total_mm |
| --- | ---: | ---: | ---: |
| Recife | 3 | 25.53 | 21.6 |
| Brasília | 3 | 21.00 | 0.9 |
| Curitiba | 3 | 12.73 | 14.2 |

## Projeto Relacionado

Os dados tratados deste ETL também são usados em um dashboard simples feito com Streamlit:

https://github.com/ypernambuco/dashboard-clima-streamlit

## Aprendizados

Neste projeto, pratiquei:
- leitura de dados vindos de API;
- transformação de JSON em tabela com pandas;
- carga de dados em SQLite;
- organização de um pipeline ETL simples;
- separação do código em etapas menores.

A divisão entre extração, transformação, carga e métricas ajudou a deixar o projeto mais organizado e fácil de entender.

## Limitações

O projeto ainda tem algumas limitações:

- usa poucas cidades;
- consulta apenas dados diários, sem granularidade por hora;
- as chamadas da API são feitas de forma sequencial;
- usa SQLite local;
- não possui agendamento automático;
- o dashboard fica em um repositório separado;
- ainda não possui testes automatizados;
- depende da disponibilidade da API no momento da execução.

## Próximos Passos

- adicionar testes para as transformações principais;
- permitir configurar cidades por CSV;
- criar mais consultas SQL de análise;
- gerar relatórios simples em CSV.

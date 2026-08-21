# SP500 Stock Returns Analysis

Análise exploratória e estatística dos retornos diários de uma ação do índice **S&P 500**, a partir de uma série histórica de preços. O script baixa a base, filtra por ticker e janela de datas, calcula os retornos e produz gráficos e um relatório em Markdown.

## Problema resolvido

Transforma uma série histórica de preços em uma leitura estatística objetiva sobre o risco e o comportamento dos retornos de um ativo.

## O que o script entrega

- download automatizado da base histórica (via `kagglehub`);
- filtragem por ticker e por janela de datas;
- cálculo do retorno diário (`pct_change`);
- testes de normalidade (Shapiro-Wilk e Kolmogorov-Smirnov);
- estimativa da probabilidade de retorno negativo;
- gráficos de preço/volume e distribuição de retornos.

## Stack

- Python 3.10+
- pandas
- numpy
- scipy
- matplotlib
- seaborn
- kagglehub

## Estrutura

```text
sp500-stock-returns-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── external/        # reservado (os dados vêm do cache do kagglehub)
├── outputs/
│   └── figures/         # gráficos gerados
└── src/
    └── sp500_returns_analysis.py
```

## Dados

Usa o dataset **S&P 500 stock data** (Kaggle, `camnugent/sandp500`):
<https://www.kaggle.com/datasets/camnugent/sandp500>

O download é feito automaticamente pelo `kagglehub` na primeira execução, então é
necessário ter credenciais do Kaggle configuradas na máquina. Opções:

- coloque o arquivo `kaggle.json` (obtido em *Kaggle → Account → Create New API Token*)
  em `~/.kaggle/kaggle.json` (Linux/macOS) ou `%USERPROFILE%\.kaggle\kaggle.json` (Windows); ou
- defina as variáveis de ambiente `KAGGLE_USERNAME` e `KAGGLE_KEY`.

O `kagglehub` guarda a base em um cache local (`~/.cache/kagglehub`), não dentro do projeto.

## Como executar

```bash
# 1. crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

# 2. instale as dependências
pip install -r requirements.txt

# 3. rode a análise (a partir da raiz do projeto)
python src/sp500_returns_analysis.py --ticker AAPL
```

Parâmetros opcionais:

```bash
python src/sp500_returns_analysis.py --ticker MSFT --start-date 2014-01-01 --end-date 2018-12-31
```

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--ticker` | `AAPL` | símbolo da ação a analisar |
| `--start-date` | `2014-01-01` | início da janela (YYYY-MM-DD) |
| `--end-date` | `2018-12-31` | fim da janela (YYYY-MM-DD) |

## Resultado esperado

Arquivos gerados em `outputs/` (o relatório também é impresso no terminal):

- `<ticker>_report.md` — resumo dos retornos, testes de normalidade e probabilidade de retorno negativo;
- `figures/<ticker>_price_volume.png` — preço de fechamento e volume;
- `figures/<ticker>_returns_distribution.png` — histograma dos retornos diários.

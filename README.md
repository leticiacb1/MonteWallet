
## 🚀 MonteWallet

Este projeto tem como objetivo encontrar a configuração ótima de uma carteira de investimentos,
por meio da simulação massiva de diferentes combinações de ativos e pesos.

Os preços dos ativos no período são baixados com o pacote `yfinance`.

Para isso realizam-se milhares de simulações de carteiras utilizando subconjuntos de ativos financeiros, retirados do index Dow Jones,
avaliando cada configuração com base em métricas clássicas de desempenho, como:

- Retorno anualizado
- Desvio padrão anual (risco)
- Índice de Sharpe (relação risco/retorno)

###  Contexto

#### Carteira

Uma carteira é uma lista de tuplas de ativo e percentual alocado naquele ativo ($w$, $w_i$).

* $w_i$: percentual do total alocado no ativo $i$

Com a restrição:

* $\sum_{i=1}^{n} w_i = 1$

Sendo que, para esse projeto, foi usado condições de contorno:

* $0 \leq w_i \leq 0.2$


####  Sharpe Ratio

Uma medida que captura retorno alto e volatilidade baixa:

$$
SR = \frac{R_p - R_f}{\sigma_p}
$$

Onde:

* $SR$: Sharpe Ratio anualizado
* $R_p$: retorno anualizado da carteira
* $R_f$: taxa livre de risco anual 
* $\sigma_p$: volatilidade anualizada da carteira

Sendo que, para esse projeto, foi usado condição:

* $R_f = 0$

#### Retorno diário

$$
r_t = \frac{P_t}{P_{t-1}} - 1
$$

Onde:

* $r_t$: retorno no dia $t$
* $P_t$: preço no dia $t$
* $P_{t-1}$: preço no dia anterior

Esse retorno é chamado de **retorno discreto**.


#### Retorno da carteira (vetor de retornos diários)

$$
\vec{r}_{\text{carteira}} = R \cdot w
$$

Onde:

* $\vec{r}_{\text{carteira}}$: vetor de retornos diários da carteira
* $R$: matriz de retornos diários (dias × ações)
* $w$: vetor de pesos

O **retorno médio anualizado** da carteira é:

$$
\mu_{\text{anual}} = \text{média}(\vec{r}_{\text{carteira}}) \times 252
$$

Sendo 252 o número de dias considerados úteis (trading days).

#### Volatilidade da carteira

$$
\sigma = \sqrt{w^T \Sigma w}
$$

Onde:

* $\sigma$: desvio padrão da carteira no período
* $\Sigma$: matriz de covariância dos retornos
* $w$: vetor de pesos

A **volatilidade anualizada** é:

$$
\sigma_{\text{anual}} = \sigma \times \sqrt{252}
$$


#### Problema de otimização

Como $R_f$ é fixo, o problema vira maximizar:

$$
\max_w \frac{R_p}{\sigma_p}
$$

Sujeito às restrições:

* Carteira com 25 ações das 30 disponíveis
* Nenhum ativo pode ter mais de 20%

### 📌 Como utilizar

#### Dependencias

1. Poetry
```bash 
# Install Pipx (Ubuntu)
$ sudo apt install pipx
$ pipx ensurepath
$ pipx install poetry
```
Saiba mais, [aqui](https://python-poetry.org/docs/)

2. Instalando bibliotecas
```bash 
$ poetry install  
```

#### Rodando

Argumentos obrigatórios:

  * `--index`     :    Nome do índice de ativos a ser utilizado (deve existir no dicionário indexes em `src/indexes.py`)

  * `--data_path` :    Caminho para salvar os resultados de todas as carteiras computadas

  * `--start_date`:    Data de início da análise no formato YYYY-MM-DD

  * `--end_date`:      Data de fim da análise no formato YYYY-MM-DD

Argumentos opcionais:

* `--n_assets`  :    Número de ativos por carteira (padrão: 25)
* `--n_wallets` :    Número de conjuntos de pesos de carteiras a serem gerados (padrão: 1000)


```bash
$ cd src/
$ python main.py \
    --index "DOW JONES" \
    --data_path path/to/data \
    --start_date "2024-07-01" \
    --end_date "2024-12-31" \
    --n_assets 25 \
    --n_wallets 1000
```
##### Saída

Todas as simulações realizadas são exportadas para um arquvio arquivo csv escrito no caminho especificado.

##### Evidências

```
$ python3 main.py --index "DOW JONES" \
                  --start_date "2024-07-01" \
                  --end_date "2024-12-31" \
                  --data_path "/home/leticiacb/Documents/FuncionalProgramming/MonteWallet/data" \
                  --n_assets 29 \
                  --n_wallets 1000 
```

* Verificação de multiprocessing ocorrendo no código `media/evidence.png`

* Exemplo de Logs exibidos no arquivo `media/evidence.log`

* Carteiras calculadas pelo exemplo no arquivo `data/wallets.csv`

<br>

<div align="center">
  
**@2024, Insper**. 10° Semester, Computer Engineering.

_Funcional Programming Discipline_
  
</div>

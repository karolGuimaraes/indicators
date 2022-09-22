# Indicadores

### - Python: 3.7.10

### Instalação do projeto

Para executar o projeto com docker:

 `$ docker build -t indicators .`

 

Para executar o projeto sem docker:

 - Criar uma virtualenv:
 
    `$ python -m venv env`

 - Iniciar avirtualenv:

    `$ source env/bin/activate`

 - Instalar as dependências:

   `$ pip install -r requirements.txt`


### Executar do projeto

Para executar com docker:

`$ docker run indicators python app.py [OPTIONS]`

Para excutar sem docker:

`$ python app.py [OPTIONS]`

OPTIONS

| parâmetro | Formato | Default | Descrição |
|---|---|---|---|
| `--start_date`  | yyyy-mm-dd | 2021-03-01 | Data de início. |
| `--end_date`  | yyyy-mm-dd | 2021-03-31 | Data fim. |
| `--days`  | dd | 5 | Dias para o cálculo da Média Móvel Exponencial. |
| `--help` | | | Ajuda. |

### Arquivo

O CSV gera os indicadores na seguinte ordem:

   - indicador-0 - Média Móvel Exponencial
   - indicador-1 - Índice de Força Relativa
   - indicador-2 - Banda de Bollinger Superior
   - indicador-3 - Banda de Bollinger Inferior


### Testes

Para executa os testes com docker:

`$ docker run indicators pytest`

Para executa os testes sem docker:

`$ pytest`
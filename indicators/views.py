import click
import pandas as pd
from datetime import datetime
import itertools
import numpy as np 
import time
import sys

DAYS_RSI = 14
DAYS_BOL = 20
COLUMN_NAMES = ['timestamp', 'indicador-0', 'indicador-1', 'indicador-2', 'indicador-3']

@click.command()
@click.option('--start_date', default='2021-03-01', help='Início do período de análise. Default 2021-03-01')
@click.option('--end_date', default='2021-03-31', help='Fim do período de análise. Default 2021-03-31')
@click.option('--days', default=5, help='Dias para a Média Móvel Exponencial. Default 5')
def main(start_date, end_date, days):

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    timestamp_start_date = int(start_date.timestamp())
    timestamp_end_date = int(end_date.timestamp())

    dataset = pd.read_csv('static/dataset/bitstamp.csv')

    filter = (dataset['Timestamp'] >= timestamp_start_date) & (dataset['Timestamp'] <= timestamp_end_date)
    dataset = dataset[filter]

    ema = 0
    last_close_price = 0
    gains, losses, quotes = {}, {}, {}
    data = []  

    for index, row in dataset.iterrows():

        variation, rsi, bolu, bold = 0, 0, 0, 0
        close_price = row['Close']
        timestamp = int(row['Timestamp'])

        ema = exponential_moving_average(close_price, days, ema)


        variation = close_price - last_close_price
        if variation > 0:
            gains[index] = variation
            losses[index] = 0
        else:
            losses[index] = abs(variation)
            gains[index] = 0

        if (index+1) >= DAYS_RSI:
            rsi = relative_strength_index(gains, losses)


        quotes[index] = close_price

        if (index+1) >= DAYS_BOL:
            bolu, bold = bollinger_bands(quotes)
  

        last_close_price = row['Close']
        data.append([timestamp, ema, rsi, bolu, bold])

    if data:
        indicadors = pd.DataFrame(data)
        indicadors.to_csv(f"tmp/indicadors_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", 
                                                            index=False, header=COLUMN_NAMES)
        click.echo(indicadors)
        sys.exit(0)

    sys.exit(1)
    

def exponential_moving_average(current_price, days, last_ema):
    '''
        Média Móvel Exponencial

        MME (ema) = [preço atual - MME(anterior)] x (2/dias+1) + MME(anterior)
    '''

    ema = (current_price - last_ema) * (2/(days+1)) + last_ema

    return ema


def relative_strength_index(gains, losses):
    '''
        Índice de Força Relativa

        IRF (rsi) = 100 - ( 100 / ( 1 + ( ( gain/N ) / ( loss/N ) )))

        gain = Média das cotações dos últimos N dias em que a cotação da ação subiu.
        loss = Média das cotações dos últimos N dias em que a cotação da ação caiu.
        N = O número de dias mais utilizado pelo mercado.
    '''

    total_gain, total_loss = 0, 0

    gain_period = dict(itertools.islice(sorted(gains.items(), reverse=True), DAYS_RSI))
    for value in gain_period.values():
        total_gain += value
    
    avg_gain = total_gain / DAYS_RSI

    loss_period = dict(itertools.islice(sorted(losses.items(), reverse=True), DAYS_RSI))
    for value in loss_period.values():
        total_loss += value
    
    avg_loss = total_loss / DAYS_RSI

    rsi = 100 - (100 / (1 + (avg_gain/avg_loss)))

    return rsi
    

def bollinger_bands(quotes):
    '''
        Bandas de Bollinger

        Superior (bolu) = Média Móvel Simples (20 dias) + (2 x Desvio Padrão de 20 dias).
        Inferior (bold) = Média Móvel Simples (20 dias) – (2 x Desvio Padrão de 20 dias).
    '''

    quotes_period = dict(itertools.islice(sorted(quotes.items(), reverse=True), DAYS_BOL))
    values = list(quotes_period.values())

    simple_moving_average = np.average(values)

    standard_deviation = np.std(values)

    bolu = simple_moving_average + ( 2 * standard_deviation )
    bold = simple_moving_average - ( 2 * standard_deviation )

    return bolu, bold
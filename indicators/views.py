from audioop import reverse
import click
import pandas as pd
from datetime import datetime
import itertools
import numpy as np 
import time

N = 14
M = 20
COLUMN_NAMES = ['timestamp', 'indicador-0', 'indicador-1', 'indicador-2', 'indicador-3']

@click.command()
@click.option('--start', help='--start_date=2022-09-01')
@click.option('--end', help='--end_date=2022-09-30')
def main(start, end):

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    timestamp_start_date = int(start_date.timestamp())
    timestamp_end_date = int(end_date.timestamp())

    period = (end_date - start_date).days

    dataset = pd.read_csv('static/dataset/bitstamp.csv')

    filter = (dataset['Timestamp'] >= timestamp_start_date) & (dataset['Timestamp'] <= timestamp_end_date)
    dataset = dataset[filter]

    ema, rsi, sma = 0, 0, 0
    variation = 0
    last_close_price = 0
    quotes = {}
    gain = {}
    loss = {}
    data = []  

    for index, row in dataset.iterrows():
        print("------ ", index, row['Timestamp'], datetime.fromtimestamp(row['Timestamp']))
        close_price = row['Close']
        ema = exponential_moving_average(close_price, period, ema)
        
        variation = close_price - last_close_price
        if variation > 0:
            gain[index] = variation
            loss[index] = 0
        else:
            loss[index] = variation
            gain[index] = 0

        quotes[index] = close_price

        total_gain = 0
        total_loss = 0
        bolu, bold = 0, 0

        if (index+1) >= N:
            # Pega as 14 últimas variações p/ calcular a média
            lista = dict(itertools.islice(sorted(gain.items(), reverse=True), N))
            for value in lista.values():
                total_gain += value
            
            avg_gain = total_gain / N

            lista = dict(itertools.islice(sorted(loss.items(), reverse=True), N))
            for value in lista.values():
                total_loss += value
            
            avg_loss = total_loss / N
            rsi = relative_strength_index(avg_gain, avg_loss)

        
        if (index+1) >= M:

            lista = dict(itertools.islice(sorted(quotes.items(), reverse=True), N))
            values = list(lista.values())
            simple_moving_average = np.average(values)

            standard_deviation = np.std(values)

            bolu = simple_moving_average + ( 2 * standard_deviation )
            bold = simple_moving_average - ( 2 * standard_deviation )
            
  
        last_close_price = row['Close']
        data.append([row['Timestamp'], ema, rsi, bolu, bold])

    
    indicadors = pd.DataFrame(data)
    indicadors.to_csv(f"tmp/indicadors_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", 
                                                        index=False, header=COLUMN_NAMES)
    
    return 



def exponential_moving_average(close_price, period, last_ema=0):
    '''
        MME = [price - MME(last)] x (2/period+1) + MME(last)
    '''
    return (close_price - last_ema) * (2/period+1) + last_ema


def relative_strength_index(avg_gain, avg_loss):
    '''
        IRF = 100 - (100/(1+( (gain/N) / (loss/N) )))

        n = 14
    '''

    return 100 - (100 / (1 + (avg_gain/avg_loss)))
    




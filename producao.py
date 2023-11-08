import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from time import sleep


def dados(csv, aparelho,i,serie):
    global contagem
    contagem = pd.read_csv('Contagem.csv')
    csv.loc[i, aparelho] = serie
    contagem.loc[0, aparelho] = len(csv)
    contagem.to_csv('Contagem.csv',index=False)
    
    return contagem

def producao():
    while True:
        sleep(4)
        sheets = pd.read_csv('https://docs.google.com/spreadsheets/d/14I3lOStF5udUsfIREUpuH8bR_9JwDJK7kktEznhWc-E/export?format=csv')
        onu = pd.read_csv('ONU.csv')
        roteador = pd.read_csv('ROTEADOR.csv')
        contagem = pd.read_csv('Contagem.csv')
        for i,sheet in enumerate(sheets['Série']):
            if sheet.startswith('FHTT') and sheet not in onu['ONU']:
                dados(onu,'ONU',i,sheet)
                onu.to_csv('ONU.csv', index=False)
            elif sheet.startswith('32') or sheet.startswith('33') or sheet.startswith('22')and sheet not in roteador['ROTEADOR']:    
                dados(roteador,'ROTEADOR',i,sheet) 
                roteador.to_csv('ROTEADOR.csv', index=False)
            i += 1


        valor = [int(contagem['ONU'].values),int(contagem['ROTEADOR'].values)]


        aparelhos = ['ONU','ROTEADOR']
        onu_producao = [len(onu), 180]
        roteador_producao = [len(roteador), 180]
        mosaico = 'AA;BC'
        fig = plt.figure(figsize=(8,5))
        axs = fig.subplot_mosaic(mosaico)
        color = ['#01c4e7','#2ef8a0']

        axs['A'].bar(aparelhos,valor,color=color)
        axs['B'].pie(onu_producao, colors=color)
        axs['C'].pie(roteador_producao,colors=color)
        plt.show()

producao()
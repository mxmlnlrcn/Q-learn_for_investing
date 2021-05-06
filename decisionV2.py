from ambienteV3 import enviroment
import numpy as np
from estrategias import estrategias
import pandas as pd


class qlearn:
    def __init__(self, inversion, objetivo = 20, data_name = 'Data/MiniEURUSD(100k).csv'):
        self.inversion = inversion
        self.data_name = data_name
        self.objetivo = objetivo
        csv = pd.read_csv('Data/actions.csv')
        self.actions = pd.DataFrame(csv)

    def entrenar(self, games= 50):
        env = enviroment(inversion = self.inversion, data_name = self.data_name, objetivo = self.objetivo)
        registro = []
        for i in range(games):
            print(f"Episode: {i}")
            historial = []
            balance = self.inversion
            done = False
            t = 1262290
            a = 0
            observation = env.reset() # preguntar estado inicial
            while not done:
                t +=1
                action = self.actions['actions'][a]
                observation_, reward, done, info = env.step(action, t) #extraer los resultados de la accion
                observation = observation_ #cambiar estado actual
                balance += reward
                historial.append(balance)
                a+=1
            
            if done:
                env.if_done()
                registro.append([])
                registro[i].append(historial)

        
        return registro


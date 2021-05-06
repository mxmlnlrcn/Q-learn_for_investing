import pandas as pd
import ta
from estrategias import estrategias



class enviroment:

    def __init__(self, inversion, objetivo, data_name, pip_value = 10000, spread = 5, riesgo = 0.1):
        self.inversion = inversion
        self.balance = 0
        self.data = data_name
        self.posiciones = 0
        self.precio_apertura = 0
        self.tipo = "buy" 
        self.profit = 0
        self.pip = pip_value
        self.spread = spread/self.pip
        self.buenas = 0
        self.malas = 0
        self.Open = []
        self.High = []
        self.Low = []
        self.Close = []
        self.ValorFuturo = []
        self.indicador = []
        self.largo = 0
        self.objetivo = objetivo/self.pip
        self.est = estrategias(data=self.data)
        self.riesgo = riesgo

    def GetData(self):
        csv = pd.read_csv(self.data)
        data = pd.DataFrame(csv)
        for i in range(0,len(data)):
            self.Open.append(data['open'][i])
            self.High.append(data['high'][i])
            self.Low.append(data['low'][i])
            self.Close.append(data['close'][i])

    def reset(self):
        self.GetData()
        self.largo = len(self.Close)
        balance_i = self.inversion
        patrimonio_i = self.inversion
        self.posiciones = 0

        return balance_i, patrimonio_i, self.posiciones

    def GetPrice (self, t):
        p = float(self.Close[t])
        p = round(p,5)
        return(p)

    def GetState (self, t): # precio actual, balance, patrimonio, n° posiciones
        self.balance = self.inversion + self.profit
        if self.posiciones==1: #calcular patrimonio
            if self.tipo == "buy":
                ganancia_actual = round(round(self.GetPrice(t)-self.precio_apertura-self.spread,5)*self.pip,1)
                patrimonio = round(self.balance + ganancia_actual,1)
            elif self.tipo == "sell":
                ganancia_actual = round(round(self.precio_apertura-self.GetPrice(t)-self.spread,5)*self.pip,1)
                patrimonio = round(self.balance + ganancia_actual,1)    
        else:
            patrimonio = self.balance

        respuesta = [self.balance, patrimonio, self.posiciones]

        return respuesta
        
    def step(self, action, t):

        reward = 0
        if action == 1: #buy
            if self.posiciones==0:
                self.tipo = "buy"
                self.posiciones += 1
                self.precio_apertura = self.GetPrice(t)
            elif self.posiciones>0:
                reward = -0.01

        if action == 2: #sell
            if self.posiciones==0:
                self.tipo = "sell"
                self.posiciones += 1
                self.precio_apertura = self.GetPrice(t)
            elif self.posiciones>0 and self.tipo == "sell":
                reward = -0.01

        if self.posiciones > 0: #cerrar
            if self.tipo == "buy":
                if  self.objetivo < self.High[t]-self.precio_apertura:
                    reward = self.balance*0.02
                    self.profit += reward
                    self.buenas +=1
                    self.posiciones = 0
                if -self.objetivo > self.Low[t]-self.precio_apertura:
                    reward = -self.balance*0.02
                    self.profit += reward
                    self.malas += 1
                    self.posiciones = 0
            else:
                if  self.objetivo < self.High[t]-self.precio_apertura:
                    reward = -self.balance*self.riesgo
                    self.profit += reward
                    self.malas +=1
                    self.posiciones = 0
                if -self.objetivo > self.Low[t]-self.precio_apertura:
                    reward = self.balance*self.riesgo
                    self.profit += reward
                    self.buenas += 1
                    self.posiciones = 0
                

        done = t==self.largo-1
        profit = self.profit
        info = {'profit': profit}
        return self.GetState(t), reward, done, info

    def if_done(self):
        if self.profit != 0:
            rent = round(100*self.profit/self.inversion,5)
            acierto = round(self.buenas*100/(self.buenas+self.malas),2)
        else:
            rent = 0
            acierto = 0
        
        print(f"Profit: {self.profit}")
        print(f"Rentabilidad: {rent}%")
        print(f"Buenas: {self.buenas}")
        print(f"Malas: {self.malas}")
        print(f"% de acierto: {acierto}%")
        print("----------------------------------------")

import ta
import pandas as pd

class estrategias:
    def __init__(self, data):
        csv = pd.read_csv(data)
        df = pd.DataFrame(csv)
        self.data = df.filter(['open', 'high', 'low','close'])

        bollinger = ta.volatility.BollingerBands(close = df["close"] ,fillna=True)
        RSI = ta.momentum.RSIIndicator(close= df["close"],fillna=True)
        stochastic = ta.momentum.StochasticOscillator( high=df["high"],low=df["low"],close=df["close"],fillna=True)
        ADX = ta.trend.ADXIndicator(high=df['high'],low=df['low'],close=df['close'],fillna=True)
        MACD = ta.trend.MACD(close=df['close'],fillna=True)

        SMA200 = ta.trend.SMAIndicator(close=df['close'], n=200, fillna=True)
        self.data['SMA200'] = SMA200.sma_indicator()
        SMA100 = ta.trend.SMAIndicator(close=df['close'], n=100,fillna=True)
        self.data['SMA100'] = SMA100.sma_indicator()
        SMA40 = ta.trend.SMAIndicator(close=df['close'], n=40,fillna=True)
        self.data['SMA40'] = SMA40.sma_indicator()
        self.data['SMA20'] = bollinger.bollinger_mavg()
        self.data['bb_h'] = bollinger.bollinger_hband()
        self.data['bb_l'] = bollinger.bollinger_lband()
        self.data['RSI'] = RSI.rsi()
        self.data['stochastic1'] = stochastic.stoch()
        self.data['stochastic2'] = stochastic.stoch_signal()
        self.data['adx'] = ADX.adx()
        self.data['macdD'] = MACD.macd_diff()#histograma
        
        haopen = []
        hahigh = []
        halow = []
        haclose = []
        for i in range(len(self.data)):
            if i == 0:
                haopen.append(df['open'][i])
                ho = df['open'][i]
            else:
                ho = (haopen[i-1]+haclose[i-1])/2
                haopen.append(ho) 
            hc = (df['open'][i]+df['high'][i]+df['low'][i]+df['close'][i])/4
            haclose.append(hc)
            hh = max(df['high'][i],ho)
            hahigh.append(hh)
            hl = min(df['low'][i],ho)
            halow.append(hl)
                
        self.data['HAopen'] = haopen
        self.data['HAhigh'] = hahigh
        self.data['HAlow'] = halow
        self.data['HAclose'] = haclose

    def show_data(self):
        return self.data

    def heikinashi(self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0

        if self.data['macdD'][t] > 0 and self.data['close'][t] > self.data['EMA20'][t] and self.data['HAlow'][t] == self.data['HAopen'][t]:
            decision = 1
        if self.data['macdD'][t] < 0 and self.data['close'][t] < self.data['EMA20'][t] and self.data['HAhigh'][t] == self.data['HAopen'][t]:
            decision = 2

        return decision

    def bband (self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['close'][t] < self.data['bb_l'][t]:
            decision = 1
        if self.data['close'][t] > self.data['bb_h'][t]:
            decision = 2
            
        return decision

    def el_rsi (self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['RSI'][t] < 30:
            decision = 1
        if self.data['RSI'][t] >70:
            decision = 2
            
        return decision

    def medias (self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['SMA200'][t] > self.data['SMA200'][t-1]:
            if self.data['EMA20'][t] > self.data['EMA40'][t]:
                decision = 1 
        if self.data['SMA200'][t] < self.data['SMA200'][t-1]:
            if self.data['EMA20'][t] < self.data['EMA40'][t]:
                decision = 2

        return decision

    def el_adx (self, t): #### sin funcionamiento
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['adx'][t] > 20:
            if self.data['adxP'][t] > self.data['adxN'][t]:
                decision = 1
            if self.data['adxP'][t] < self.data['adxN'][t]:
                decision = 2

        return decision

    def estocastico (self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['stochastic2'][t] > 80:
            if self.data['stochastic2'][t-1] < self.data['stochastic1'][t-1]:
                if self.data['stochastic2'][t] > self.data['stochastic1'][t]:
                    decision = 2
        if self.data['stochastic2'][t] < 20:
            if self.data['stochastic2'][t-1] > self.data['stochastic1'][t-1]:
                if self.data['stochastic2'][t] < self.data['stochastic1'][t]:
                    decision = 1
        return decision

    def trend (self,t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['adx'][t] > 14:
                decision = 1
        return decision

    def ccis(self, t):
        decision = 0
        return 0

    def HA(self, t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        if self.data['close'][t] > self.data['EMA200'][t]:
            if self.data['HAopen'][t] == self.data['HAlow'][t]:
                decision = 1 
        if self.data['close'][t] < self.data['EMA200'][t]:
            if self.data['HAopen'][t] == self.data['HAhigh'][t]:
                decision = 2
        return decision

    def la_strat(self,t):
        decision = 0
        if t>= len(self.data['close']):
            return 0
        
        if self.data['SMA200'][t] > self.data['SMA200'][t-1]:
            if self.data['close'][t] > self.data['SMA200'][t]:
                if self.data['EMA20'][t] > self.data['EMA40'][t]:
                    if self.data['stochastic2'][t] > 80:
                        if self.data['macdD'][t] > 0:
                            decision = 1 

        elif self.data['SMA200'][t] < self.data['SMA200'][t-1]:
            if self.data['close'][t] < self.data['SMA200'][t]:
                if self.data['EMA20'][t] < self.data['EMA40'][t]:
                    if self.data['stochastic2'][t] < 20:
                        if self.data['macdD'][t] > 0:
                            decision = 2 
        else:
            decision = 0

        return decision


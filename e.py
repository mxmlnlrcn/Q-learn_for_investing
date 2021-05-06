from decisionV2 import qlearn

q=qlearn(inversion=10000, data_name='Data/EURUSD5.csv')
q.entrenar(games = 1)

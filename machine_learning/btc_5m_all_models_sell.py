import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
import ta

list_of_equity = [
    "./data/aapl_5m_train.csv",
    "./data/aapl_project_1m_test.csv",
    "./data/aapl_project_1m_train.csv",
    "./data/aapl_project_test.csv",
    "./data/aapl_project_train.csv",
    "./data/btc_project_1m_test.csv",
    "./data/btc_project_1m_train.csv",
    "./data/btc_project_test.csv",
    "./data/btc_project_train.csv"
]


def reading_files(list_of_files: str):
    """
    list of files is going to be a list where all the files need
    to be written as a string
    """

    dict_files = dict()
    for file in list_of_files:
        dict_files[file] = pd.read_csv(file)
    return dict_files


data = pd.read_csv("./data/btc_project_train.csv").dropna()

data_clean = data.loc[:, ["Close"]]
data_clean["Y"] = data_clean.shift(-15)
data_clean["Close_t1"] = data.loc[:, ["Close"]].shift(1)
data_clean["Close_t2"] = data.loc[:, ["Close"]].shift(2)
data_clean["Close_t3"] = data.loc[:, ["Close"]].shift(3)
data_clean["Close_t4"] = data.loc[:, ["Close"]].shift(4)
data_clean["Close_t5"] = data.loc[:, ["Close"]].shift(5)
data_clean["rsi_10"] = ((ta.momentum.RSIIndicator(data["Close"], window=10)).rsi())
data_clean["rsi_20"] = ((ta.momentum.RSIIndicator(data["Close"], window=20)).rsi())
data_clean["rsi_30"] = ((ta.momentum.RSIIndicator(data["Close"], window=30)).rsi())
data_clean["macd_10_24_7"] = ((ta.trend.MACD(close=data["Close"], window_slow=24, window_fast=10, window_sign=7)).macd())
data_clean["macd_12_26_9"] = ((ta.trend.MACD(close=data_clean["Close"], window_slow=26, window_fast=12, window_sign=9)).macd())
data_clean["macd_5_35_5"] = ((ta.trend.MACD(close=data_clean["Close"], window_slow=35, window_fast=5, window_sign=5)).macd())

# Bollinger bands
bollinger_20_2 = ta.volatility.BollingerBands(close=data_clean["Close"], window=20, window_dev=2)
data_clean["bollinger_20_2_hband"] = bollinger_20_2.bollinger_hband()
data_clean["bollinger_20_2_lband"] = bollinger_20_2.bollinger_lband()
data_clean["bollinger_20_2_mavg"] = bollinger_20_2.bollinger_mavg()

bollinger_10_1_5 = ta.volatility.BollingerBands(close=data_clean["Close"], window=10, window_dev=1.5)
data_clean["bollinger_10_1_5_hband"] = bollinger_10_1_5.bollinger_hband()
data_clean["bollinger_10_1_5_lband"] = bollinger_10_1_5.bollinger_lband()
data_clean["bollinger_10_1_5_mavg"] = bollinger_10_1_5.bollinger_mavg()

bollinger_50_2_5 = ta.volatility.BollingerBands(close=data_clean["Close"], window=50, window_dev=2.5)
data_clean["bollinger_50_2_5_hband"] = bollinger_50_2_5.bollinger_hband()
data_clean["bollinger_50_2_5_lband"] = bollinger_50_2_5.bollinger_lband()
data_clean["bollinger_50_2_5_mavg"] = bollinger_50_2_5.bollinger_mavg()
data_clean = data_clean.dropna()

data_clas = data_clean.drop("Y", axis=1).copy()
data_clas["Y"] = data_clas.Close > data_clas.Close.shift(-15)

X_train, X_test, y_train, y_test = train_test_split(data_clas.drop("Y", axis=1),
                                                    data_clas.Y,
                                                    shuffle=False, test_size=0.2)


files = reading_files(list_of_equity)
data = files["./data/btc_project_test.csv"]

data_clean = data.loc[:, ["Close"]]
data_clean["Y"] = data_clean.shift(-15)
data_clean["Close_t1"] = data.loc[:, ["Close"]].shift(1)
data_clean["Close_t2"] = data.loc[:, ["Close"]].shift(2)
data_clean["Close_t3"] = data.loc[:, ["Close"]].shift(3)
data_clean["Close_t4"] = data.loc[:, ["Close"]].shift(4)
data_clean["Close_t5"] = data.loc[:, ["Close"]].shift(5)
data_clean["rsi_10"] = ((ta.momentum.RSIIndicator(data["Close"], window=10)).rsi())
data_clean["rsi_20"] = ((ta.momentum.RSIIndicator(data["Close"], window=20)).rsi())
data_clean["rsi_30"] = ((ta.momentum.RSIIndicator(data["Close"], window=30)).rsi())
data_clean["macd_10_24_7"] = (
    (ta.trend.MACD(close=data["Close"], window_slow=24, window_fast=10, window_sign=7)).macd())
data_clean["macd_12_26_9"] = (
    (ta.trend.MACD(close=data_clean["Close"], window_slow=26, window_fast=12, window_sign=9)).macd())
data_clean["macd_5_35_5"] = (
    (ta.trend.MACD(close=data_clean["Close"], window_slow=35, window_fast=5, window_sign=5)).macd())

### bollinger bands
bollinger_20_2 = ta.volatility.BollingerBands(close=data_clean["Close"], window=20, window_dev=2)
data_clean["bollinger_20_2_hband"] = bollinger_20_2.bollinger_hband()
data_clean["bollinger_20_2_lband"] = bollinger_20_2.bollinger_lband()
data_clean["bollinger_20_2_mavg"] = bollinger_20_2.bollinger_mavg()

bollinger_10_1_5 = ta.volatility.BollingerBands(close=data_clean["Close"], window=10, window_dev=1.5)
data_clean["bollinger_10_1_5_hband"] = bollinger_10_1_5.bollinger_hband()
data_clean["bollinger_10_1_5_lband"] = bollinger_10_1_5.bollinger_lband()
data_clean["bollinger_10_1_5_mavg"] = bollinger_10_1_5.bollinger_mavg()

bollinger_50_2_5 = ta.volatility.BollingerBands(close=data_clean["Close"], window=50, window_dev=2.5)
data_clean["bollinger_50_2_5_hband"] = bollinger_50_2_5.bollinger_hband()
data_clean["bollinger_50_2_5_lband"] = bollinger_50_2_5.bollinger_lband()
data_clean["bollinger_50_2_5_mavg"] = bollinger_50_2_5.bollinger_mavg()
data_clean = data_clean.dropna()

data_clas = data_clean.drop("Y", axis=1).copy()

data_clas["Y"] = data_clas.Close > data_clas.Close.shift(-15)

X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(data_clas.drop("Y", axis=1),
                                                            data_clas.Y,
                                                            shuffle=False, test_size=0.2)

def model_y():
    classification_model = LogisticRegression().fit(X_train, y_train)
    svc = SVC(C=500, max_iter=10_000, probability=True).fit(X_train, y_train)
    xgb = XGBClassifier().fit(X_train, y_train)

    ensemble_model = VotingClassifier(estimators=[
        ('logistic', classification_model),
        ('svc', svc),
        ('xgb', xgb)
    ], voting='soft')

    ensemble_model.fit(X_train, y_train)

    signals = ensemble_model.predict(X_test_t)
    trading_df = X_test_t.copy()
    trading_df['SELL_SIGNAL'] = signals

    return trading_df


x = model_y()
df_sellsignals = x[['Close', 'SELL_SIGNAL']]

print("###############################################")
print("Trading signals:", sum(df_sellsignals['SELL_SIGNAL']))

capital = 1_000_000
n_shares = 15
stop_loss = 0.4
take_profit = 0.4
COM = 0.125 / 100

active_positions = []
portfolio_value = [capital]

for i, row in df_sellsignals.iterrows():
    # Cerrar todas las posiciones que han alcanzado el stop loss o el take profit
    active_pos_copy = active_positions.copy()
    for pos in active_pos_copy:
        if row.Close > pos["stop_loss"]:  # La posición se cierra con pérdida
            capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COM)
            active_positions.remove(pos)
        elif row.Close < pos["take_profit"]:  # La posición se cierra con ganancia
            capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COM)
            active_positions.remove(pos)

    # Verificar si hay señal de venta
    if row.SELL_SIGNAL:
        # Verificar si tenemos suficientes acciones para vender
        if (capital > row.Close * (1 + COM) * n_shares * 1.1) and len(active_positions) < 1000:
            capital -= row.Close * (COM) * n_shares
            active_positions.append({
                "type": "SHORT",
                "sold_at": row.Close,
                "n_shares": n_shares,
                "stop_loss": row.Close * (1 + stop_loss),
                "take_profit": row.Close * (1 - take_profit)
            })
        else:
            print("OUT OF CASH")

    # Valor del portafolio a través del tiempo
    positions_value = sum([(pos["sold_at"] - row.Close) * pos["n_shares"] for pos in active_positions])
    portfolio_value.append(capital + positions_value)

# Cerrar todas las posiciones restantes al final
for pos in active_positions.copy():
    capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COM)
    active_positions.remove(pos)

portfolio_value.append(capital)


# Graficar el valor del portafolio
plt.figure(figsize=(12, 6))
plt.plot(portfolio_value)
plt.xlabel('Período de Tiempo')
plt.ylabel('Valor del Portafolio')
plt.title('Evolución del Valor del Portafolio Basado en Señales de Venta')
plt.legend()
plt.grid(True)

capital_benchmark = 1_000_000
shares_to_buy = capital_benchmark // (df_sellsignals.Close.values[0] * (1 + COM))
capital_benchmark -= shares_to_buy * df_sellsignals.Close.values[0] * (1 + COM)
portfolio_value_benchmark = (shares_to_buy * df_sellsignals.Close) + capital_benchmark
portfolio_value_benchmark_list = portfolio_value_benchmark.tolist()

plt.title(f"Active={(portfolio_value[-1] / 1_000_000 - 1) * 100}%\n" +
          f"Passive={(portfolio_value_benchmark.values[-1] / 1_000_000 - 1) * 100}%")
plt.plot(portfolio_value, label="Active")
plt.plot(portfolio_value_benchmark_list, label="Passive")
plt.legend()
plt.show()
















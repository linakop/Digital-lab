import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title('Preisvorhersage')

df = pd.read_csv('Test.csv', sep=";")
df.tail()


train_size = int(len(df) * 0.8)
df_train, df_test = df[:train_size], df[train_size:len(df)]
train_data = df_train.iloc[:, 1:2].values


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
train_data_scaled = scaler.fit_transform(train_data)


x_train = []
y_train = []

time_window = 7

for i in range(time_window, len(train_data_scaled)):
  x_train.append(train_data_scaled[i-time_window:i, 0])
  y_train.append(train_data_scaled[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))



from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, epochs=25, batch_size=32)



actual_stock_price = df_test.iloc[:, 1:2].values

total_data = pd.concat((df_train['Preis'], df_test['Preis']), axis=0)
test_data = total_data[len(total_data)-len(df_test)-time_window:].values
test_data = test_data.reshape(-1, 1)
test_data = scaler.transform(test_data)



total_dates = pd.concat((df_train['Datum'], df_test['Datum']), axis=0)
test_dates = total_dates[len(total_dates)-len(df_test)-time_window:].values
test_dates = test_dates.reshape(-1, 1)


x_test = []
for i in range(time_window, len(test_data)):
  x_test.append(test_data[i-time_window:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))



predicted_stock_price = model.predict(x_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)



import datetime as dt

plt_test_dates = [dt.datetime.strptime(d, '%d.%m.%Y') for d in test_dates[time_window:, 0]]
plt.plot(plt_test_dates, actual_stock_price[:, 0], color='black', label='Realer Preis')
plt.plot(plt_test_dates, predicted_stock_price[:, 0], color='green', label='Vorhergesagter Preis')
plt.xticks(rotation=90)
plt.title('Preisentwicklung')
plt.xlabel('Datum')
plt.ylabel('Preis in EUR')
plt.legend()
plt.show()



real_data = [test_data[len(test_data)+1-time_window:len(test_data+1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)



st.subheader('Der prognostizierte Preis beträgt morgen:  ')
st.subheader(prediction) 
st.subheader("EURO")
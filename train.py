import matplotlib
matplotlib.use('gtk3agg')  # Utiliser le backend GTK3Agg pour matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def normalize_km(km):
    return (km - km.mean()) / km.std()

df = pd.read_csv('data.csv')
km = np.array(df['km'])
price = np.array(df['price'])

a = 0
b = 0

L = 0.01
epochs = 1000
n = float(len(km))

km = normalize_km(km)
price = normalize_km(price)

plt.ion()  # Activer le mode interactif pour matplotlib
fig, ax = plt.subplots()
ax.scatter(km, price, color='blue', label='Data points')
line, = ax.plot(km, a * km + b, color='red', label='Regression line')
ax.legend()
plt.xlabel('Normalized km')
plt.ylabel('Price')
plt.title('Linear Regression Training')

for i in range(epochs):
    y_pred = a * km + b
    D_a = (-2 / n) * sum(km * (price - y_pred))
    D_b = (-2 / n) * sum(price - y_pred)
    a = a - L * D_a
    b = b - L * D_b

    if i % 10 == 0:  # Mettre à jour la courbe toutes les 10 epochs
        line.set_ydata(a * km + b)
        plt.draw()
        plt.pause(0.01)

plt.ioff()  # Désactiver le mode interactif
plt.show()

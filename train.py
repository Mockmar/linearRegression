import matplotlib
matplotlib.use('gtk3agg')  # Assurez-vous que vous avez les dépendances GTK installées
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

A = 0
B = 0
L = 0.001
EPOCH = 10000
EPOCH_DISPLAY = 100

def normalize(values, mean, std):
    return (values - mean) / std

def R2(y, y_pred):
    return 1 - (sum((y - y_pred) ** 2) / sum((y - y.mean()) ** 2))

def predict(mileage):
    return A * mileage + B

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python train.py <path_data> <path_model>")
        sys.exit(1)

    path_data = sys.argv[1]
    path_model = sys.argv[2]

    try:
        df = pd.read_csv(path_data)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        sys.exit(1)

    if 'km' not in df.columns or 'price' not in df.columns:
        print("Erreur : les colonnes 'km' et 'price' doivent exister dans le fichier.")
        sys.exit(1)

    km = np.array(df['km'])
    price = np.array(df['price'])

    if len(km) == 0 or len(price) == 0:
        print("Erreur : le fichier de données est vide.")
        sys.exit(1)

    km_normalize = [km.mean(), km.std()]
    price_normalize = [price.mean(), price.std()]

    m = float(len(km))

    km_norm = normalize(km, km_normalize[0], km_normalize[1])
    price_norm = normalize(price, price_normalize[0], price_normalize[1])

    plt.ion()
    fig, ax = plt.subplots()
    ax.scatter(km_norm, price_norm, label="Données")
    line, = ax.plot(km_norm, A * km_norm + B, color='red', label="Modèle")
    ax.set_xlabel("Kilométrage normalisé")
    ax.set_ylabel("Prix normalisé")
    ax.legend()
    plt.title("Régression linéaire - Entraînement")

    for i in range(EPOCH):
        y_pred = predict(km_norm)
        tmpB = L * (1 / m) * sum(price_norm - y_pred)
        tmpA = L * (1 / m) * sum((price_norm - y_pred) * km_norm)
        A += tmpA
        B += tmpB

        if i % EPOCH_DISPLAY == 0 or i == EPOCH - 1:
            line.set_ydata(A * km_norm + B)
            ax.set_title(f"Epoch {i+1}/{EPOCH}")
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)

    plt.ioff()
    plt.show()

    y_pred = predict(km_norm)
    r2 = R2(price_norm, y_pred)
    print(f"R2 = {r2:.3f}")

    with open(path_model, 'w') as f:
        f.write(f"{A},{B}\n")
        f.write(f"{km_normalize[0]},{km_normalize[1]}\n")
        f.write(f"{price_normalize[0]},{price_normalize[1]}\n")


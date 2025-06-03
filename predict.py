import sys
import json

def extract_model(path_model):
    try:
        with open(path_model, "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        print(f"Erreur : fichier '{path_model}' introuvable.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

    if not data :
        print("Erreur : fichier vide ou invalide.")
        sys.exit(1)

    data = [line.strip() for line in data if line.strip()]
    thetas = data[0].strip().split(",")
    if len(thetas) != 2:
        print("Erreur : fichier ne contient pas deux valeurs de theta")
        sys.exit(1)

    try:
        thetas = [float(theta) for theta in thetas]
    except ValueError:
        print("Erreur : valeurs de theta non valides")
        sys.exit(1)

    print("Modèle extrait avec succès :")
    print(f"    theta0 = {thetas[0]}")
    print(f"    theta1 = {thetas[1]}")

    return thetas

def predict(mileage, thetas):
    return thetas[0] * mileage + thetas[1]

def normalize(value, normalize):
    if value < 0:
        raise ValueError("Erreur : le kilométrage ne peut pas être négatif.")
    if normalize[1] == 0:
        raise ValueError("Erreur : la valeur de normalisation ne peut pas être nulle.")
    return (value - normalize[0]) / normalize[1]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python predict.py <mileage> <path_model>")
        sys.exit(1)

    try:
        mileage = float(sys.argv[1])
    except ValueError:
        print("Erreur : valeur de mileage non valide.")
        sys.exit(1)

    path_model = sys.argv[2]
    thetas = extract_model(path_model)

    try:
        price = predict(mileage, thetas)
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)

    print(f"Prix prédit : {price:.2f} euros")


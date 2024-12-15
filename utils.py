import csv
import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def list_jobs(n):
    jobs1 = []
    jobs2 = []

    for i in range(0,n//2):
        jobs1.append(i)
    for i in range(n//2,n):
        jobs2.append(i)

    return jobs1,jobs2


def append_results(id, min_max, kalai_smorodinsky, suboptimal, file_name):
    if len(suboptimal) != 11:
        raise ValueError("La lista di valori deve contenere esattamente 11 elementi.")

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([id, min_max, kalai_smorodinsky] + suboptimal)


def reset_csv(file_name):
    header = [
        "ID", "Min Max", "Kalai Smorodinsky",
        "alpha_0.0", "alpha_0.1", "alpha_0.2", "alpha_0.3", "alpha_0.4",
        "alpha_0.5", "alpha_0.6", "alpha_0.7", "alpha_0.8", "alpha_0.9", "alpha_1.0"
    ]

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

def plot_payoff_values(file1, file2, output_dir):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    os.makedirs(output_dir, exist_ok=True)

    alpha_columns = [col for col in df1.columns if col.startswith('alpha')]

    # Genera un grafico per ogni ID
    for index, row in df1.iterrows():
        instance_id = row['ID']
        # Payoff del primo giocatore (ascisse)
        x_values = row[alpha_columns].values
        # Payoff del secondo giocatore (ordinate)
        y_values = df2.loc[index, alpha_columns].values

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, 'o-', label=f"Alpha results")

        kalai_x = row["Kalai Smorodinsky"]
        kalai_y = df2.loc[index, "Kalai Smorodinsky"]
        plt.scatter(kalai_x, kalai_y, color='red', edgecolor='black', s=100, label="Kalai-Smorodinsky")

        min_max_x = row["Min Max"]
        min_max_y = df2.loc[index, "Min Max"]
        plt.scatter(min_max_x, min_max_y, color='black', marker='x', s=100, label="Min Max")

        plt.title(f"Payoff per istanza {int(instance_id)}")
        plt.xlabel("Payoff Primo Giocatore")
        plt.ylabel("Payoff Secondo Giocatore")
        plt.legend()
        plt.grid(True)

        output_path = os.path.join(output_dir, f'instance_{int(instance_id)}.png')
        plt.savefig(output_path)
        plt.close()


def generate_distribution_values(n, low, high, run):
    for i in range(run):
        values = np.random.randint(low, high, n)
        print(f"[{', '.join(map(str, values))}]")






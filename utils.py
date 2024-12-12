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


def append_results(id, min_max, kalai_smorondisky, suboptimal, file_name):
    if len(suboptimal) != 11:
        raise ValueError("La lista di valori deve contenere esattamente 11 elementi.")

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([id, min_max, kalai_smorondisky] + suboptimal)


def reset_csv(file_name):
    header = [
        "ID", "Min Max", "Kalai Smorondisky",
        "alpha_0.0", "alpha_0.1", "alpha_0.2", "alpha_0.3", "alpha_0.4",
        "alpha_0.5", "alpha_0.6", "alpha_0.7", "alpha_0.8", "alpha_0.9", "alpha_1.0"
    ]

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

def plot_scheduling_solutions(data_file, output_dir):
    df = pd.read_csv(data_file)

    os.makedirs(output_dir, exist_ok=True)

    for _, row in df.iterrows():
        instance_id = row['ID']
        min_max = row['Min Max']

        alpha_values = [float(a.split('_')[1]) for a in df.columns if a.startswith('alpha_')]
        suboptimal_solutions = [row[f'alpha_{alpha}'] for alpha in alpha_values]

        plt.figure(figsize=(10, 6))
        plt.plot(alpha_values, suboptimal_solutions, marker='o', label='Soluzioni Subottime')

        if min_max in suboptimal_solutions:
            plt.scatter(
                alpha_values[suboptimal_solutions.index(min_max)],
                min_max,
                color='red',
                label='Min Max (Coincide)',
                zorder=5
            )
        else:
            plt.axhline(y=min_max, color='red', linestyle='--', label='Min Max (Non coincide)')

        plt.title(f'Istanza {int(instance_id)}')
        plt.xlabel('Alpha')
        plt.ylabel('Valore Ottimo')
        plt.legend()
        plt.grid(True)

        output_path = os.path.join(output_dir, f'instance_{int(instance_id)}.png')
        plt.savefig(output_path)
        plt.close()

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
        plt.plot(x_values, y_values, 'o-', label=f"Suboptimal values")

        kalai_x = row["Kalai Smorondisky"]
        kalai_y = df2.loc[index, "Kalai Smorondisky"]
        plt.scatter(kalai_x, kalai_y, color='red', edgecolor='black', s=100, label="Kalai-Smorondinsky")

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






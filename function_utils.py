import csv
import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_file(file_name):
    # Leggere il file JSON
    with open(file_name, 'r') as file:
        # Caricare il contenuto come una lista di dizionari
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
        raise ValueError("La lista di valori deve contenere esattamente 10 elementi.")

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Scrivi la riga
        writer.writerow([id, min_max, kalai_smorondisky] + suboptimal)

def reset_csv(file_name):
    header = [
        "ID", "Min Max", "Kalai Smorondisky",
        "alpha_0.0", "alpha_0.1", "alpha_0.2", "alpha_0.3", "alpha_0.4",
        "alpha_0.5", "alpha_0.6", "alpha_0.7", "alpha_0.8", "alpha_0.9", "alpha_1.0"
    ]

    # Sovrascrivi il file mantenendo solo l'intestazione
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

def plot_scheduling_solutions(data_file, output_dir):
    df = pd.read_csv(data_file)

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

        plt.title(f'Istanza {instance_id}')
        plt.xlabel('Alpha')
        plt.ylabel('Valore Ottimo')
        plt.legend()
        plt.grid(True)

        output_path = os.path.join(output_dir, f'instance_{instance_id}.png')
        plt.savefig(output_path)
        plt.close()


def generate_distribution_values(n, low, high):
    for i in range(2):
        # Generazione dei valori
        values = np.random.randint(low, high, n)
        print(f"[{', '.join(map(str, values))}]")










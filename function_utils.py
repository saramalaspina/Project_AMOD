import json

def read_file():
    # Leggere il file JSON
    with open('istanze/istanze_simmetriche.json', 'r') as file:
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


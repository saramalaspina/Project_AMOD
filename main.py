from function_utils import*
from pli.solution1 import min_max_pli
from pli.solution2 import kalai_smorondisky_pli
from pli.solution3 import subottimo_pli


def get_data(istanza):
    if istanza == 1:
        print("Istanze simmetriche")
        data = read_file('istanze/istanze_simmetriche.json')
        nome = "simmetriche"
    elif istanza == 2:
        print("Istanze con pochi job e bassa varianza")
    elif istanza == 3:
        print("Istanze con molti job e bassa varianza")
    elif istanza == 4:
        print("Istanze con pochi job e alta varianza")
    elif istanza == 5:
        print("Istanze con molti job e alta varianza")
    else:
        raise ValueError()
    return data, nome

def esegui_modello(modello, data, istanza):
    if modello == 1:
        print("Min-Max")
        output_file =  f"outputs/{istanza}/min_max.txt"
        with open(output_file, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            min_max_pli(n, jobs1, jobs2, p, id, output_file)
    elif modello == 2:
        print("Kalai-Smorondisky")
        output_file =  f"outputs/{istanza}/kalai_smorondisky.txt"
        with open(output_file, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            kalai_smorondisky_pli(n, jobs1, jobs2, p, id, output_file)
    elif modello == 3:
        print("Soluzioni Subottime")
        output_file = f"outputs/{istanza}/subottimo.txt"
        with open(output_file, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            for alpha in range(11):
                subottimo_pli(n, jobs1, jobs2, p, alpha/10, id, output_file)
    else:
        raise ValueError()


def main():
    print("Seleziona una tipologia di istanza da eseguire:")
    print("1. Istanze simmetriche")
    print("2. Istanze con pochi job e bassa varianza")
    print("3. Istanze con molti job e bassa varianza")
    print("4. Istanze con pochi job e alta varianza")
    print("5. Istanze con alti job e alta varianza")
    try:
        istanza = int(input("Inserisci il numero corrispondente all'istanza: "))
        data, nome = get_data(istanza)
        print("Min-Max")
        output_file1 = f"outputs/{nome}/min_max.txt"
        with open(output_file1, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            min_max_pli(n, jobs1, jobs2, p, id, output_file1)

        print("Kalai-Smorondisky")
        output_file2 = f"outputs/{nome}/kalai_smorondisky.txt"
        with open(output_file2, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            kalai_smorondisky_pli(n, jobs1, jobs2, p, id, output_file2)

        print("Soluzioni Subottime")
        output_file3 = f"outputs/{nome}/subottimo.txt"
        with open(output_file3, 'w'):
            print("Clear file")
        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            for alpha in range(11):
                subottimo_pli(n, jobs1, jobs2, p, alpha / 10, id, output_file3)
    except ValueError:
        print("Errore: Inserisci un numero valido.")

    print("Seleziona il modello:")
    print("1. Min-Max")
    print("2. Kalai-Smorondisky")
    print("3. Soluzioni Subottime")
    try:
        modello = int(input("Inserisci il numero corrispondente al modello: "))
        #esegui_modello(modello, data, nome)
    except ValueError:
        print("Errore: Inserisci un numero valido.")


main()


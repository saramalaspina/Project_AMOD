from function_utils import*
from pli.solution1 import min_max_pli
from pli.solution2 import kalai_smorondisky_pli
from pli.solution3 import subottimo_pli


def get_data(type):
    if type == 1:
        print("Istanze simmetriche")
        data = read_file('istanze/istanze_simmetriche.json')
        name = "simmetriche"
    elif type == 2:
        print("Istanze con pochi job e bassa varianza")
        data = read_file('istanze/few_low.json')
        name = "few_low"
    elif type == 3:
        print("Istanze con molti job e bassa varianza")
        data = read_file('istanze/many_low.json')
        name = "many_low"
    elif type == 4:
        print("Istanze con pochi job e alta varianza")
        data = read_file('istanze/few_high.json')
        name = "few_high"
    elif type == 5:
        print("Istanze con molti job e alta varianza")
        data = read_file('istanze/many_high.json')
        name = "many_high"
    else:
        raise ValueError()
    return data, name


def main():
    print("Seleziona una tipologia di istanza da eseguire:")
    print("1. Istanze simmetriche")
    print("2. Istanze con pochi job e bassa varianza")
    print("3. Istanze con molti job e bassa varianza")
    print("4. Istanze con pochi job e alta varianza")
    print("5. Istanze con molti job e alta varianza")
    try:
        choice = int(input("Inserisci il numero corrispondente all'istanza: "))
        data, name = get_data(choice)

        output_file1 = f"outputs/{name}/min_max.txt"
        output_file2 = f"outputs/{name}/kalai_smorondisky.txt"
        output_file3 = f"outputs/{name}/subottimo.txt"
        output_file4 = f"outputs/{name}/results.csv"

        with open(output_file1, 'w'):
            print("Clear file 1")
        with open(output_file2, 'w'):
            print("Clear file 2")
        with open(output_file3, 'w'):
            print("Clear file 3")
        with open(output_file4, 'w'):
            reset_csv(output_file4)

        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            result1 = min_max_pli(n, jobs1, jobs2, p, id, output_file1)
            result2 = kalai_smorondisky_pli(n, jobs1, jobs2, p, id, output_file2)
            suboptimal_values = []
            for alpha in range(11):
                result3 = subottimo_pli(n, jobs1, jobs2, p, alpha / 10, id, output_file3)
                suboptimal_values.append(result3)

            append_results(id, result1, result2, suboptimal_values, output_file4)

        plot_scheduling_solutions(f"outputs/{name}/results.csv", f"outputs/{name}/plots")

    except ValueError:
        print("Errore: Inserisci un numero valido.")

main()


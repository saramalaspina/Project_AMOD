from utils import*
from pli.min_max import min_max_pli
from pli.kalai_smorondisky import kalai_smorondisky_pli
from pli.suboptimal import subottimo_pli


def get_data(type):
    if type == 1:
        print("Istanze simmetriche")
        data = read_file('instances/symmetric.json')
        name = "symmetric"
    elif type == 2:
        print("Istanze con pochi job e bassa varianza")
        data = read_file('instances/few_low.json')
        name = "few_low"
    elif type == 3:
        print("Istanze con molti job e bassa varianza")
        data = read_file('instances/many_low.json')
        name = "many_low"
    elif type == 4:
        print("Istanze con pochi job e alta varianza")
        data = read_file('instances/few_high.json')
        name = "few_high"
    elif type == 5:
        print("Istanze con molti job e alta varianza")
        data = read_file('instances/many_high.json')
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
        output_file3 = f"outputs/{name}/suboptimal.txt"
        output_file4 = f"outputs/{name}/results.csv"
        output_file5 = f"outputs/{name}/payoff1.csv"
        output_file6 = f"outputs/{name}/payoff2.csv"

        with open(output_file1, 'w'):
            print("Clear file 1")
        with open(output_file2, 'w'):
            print("Clear file 2")
        with open(output_file3, 'w'):
            print("Clear file 3")
        with open(output_file4, 'w'):
            reset_csv(output_file4)
        with open(output_file5, 'w'):
            reset_csv(output_file5)
        with open(output_file6, 'w'):
            reset_csv(output_file6)

        for instance in data:
            id = instance["id"]
            p = instance["p"]
            n = instance["n"]
            jobs1, jobs2 = list_jobs(n)
            result_mm, sum_mm_1, sum_mm_2 = min_max_pli(n, jobs1, jobs2, p, id, output_file1)
            result_ks, sum_ks_1, sum_ks_2 = kalai_smorondisky_pli(n, jobs1, jobs2, p, id, output_file2)
            suboptimal_values = []
            sum1_alpha = []
            sum2_alpha = []
            for alpha in range(11):
                result, sum1, sum2 = subottimo_pli(n, jobs1, jobs2, p, alpha / 10, id, output_file3)
                suboptimal_values.append(result)
                sum1_alpha.append(sum1)
                sum2_alpha.append(sum2)

            append_results(id, result_mm, result_ks, suboptimal_values, output_file4)
            append_results(id, sum_mm_1, sum_ks_1, sum1_alpha, output_file5)
            append_results(id, sum_mm_2, sum_ks_2, sum2_alpha, output_file6)

        plot_scheduling_solutions(output_file4, f"outputs/{name}/plots/min_max_suboptimal")
        plot_payoff_values(output_file5, output_file6,f"outputs/{name}/plots/kalai_smorondisky_suboptimal")

    except ValueError:
        print("Errore: Inserisci un numero valido.")

main()


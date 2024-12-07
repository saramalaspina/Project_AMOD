import gurobipy as gp
from gurobipy import GRB

def best_value(sorted_p):
    c = [0] * len(sorted_p)
    c[0] = sorted_p[0]
    best = c[0]
    for i in range(1, len(sorted_p)):
        c[i] = sorted_p[i] + c[i - 1]
        best += c[i]
    return best, c

def worst_value(sorted_p, c_other):
    c_worst = [0] * len(sorted_p)
    c_worst[0] = sorted_p[0] + c_other[-1]
    worst = c_worst[0]
    for i in range(1, len(sorted_p)):
        c_worst[i] = sorted_p[i] + c_worst[i - 1]
        worst += c_worst[i]
    return worst

def kalai_smorondisky_pli(n, jobs1, jobs2, p, id, output_file):
    # Creazione del modello
    model = gp.Model("Solution2")

    M = sum(p)  # Big M (valore molto grande)

    p1 = [0] * len(jobs1)  # Vettore delle durate dei job assegnati al giocatore 1
    p2 = [0] * len(jobs2)  # Vettore delle durate dei job assegnati al giocatore 2

    j = 0
    for i in jobs1:
        p1[j] = p[i]
        j += 1

    j = 0
    for i in jobs2:
        p2[j] = p[i]
        j += 1

    # Ordinamento delle durate dei job di ciascun giocatore secondo l'ordine SPT
    sorted_p1 = sorted(p1)
    sorted_p2 = sorted(p2)

    best1, c1 = best_value(sorted_p1)
    best2, c2 = best_value(sorted_p2)
    worst1 = worst_value(sorted_p1, c2)
    worst2 = worst_value(sorted_p2, c1)

    # Variabili di inizio e completamento per ogni job
    s = model.addVars(n, vtype=GRB.CONTINUOUS, name="s")  # Tempo di inizio
    c = model.addVars(n, vtype=GRB.CONTINUOUS, name="c")  # Tempo di completamento

    # Creazione delle variabili di precedenza binarie x[i,j] (x[i,j] = 1 --> job i precede job j)
    x = model.addVars([(i, j) for i in range(n) for j in range(i+1, n)],vtype=GRB.BINARY,name='x')

    # Variabile z per il tempo di completamento massimo
    z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

    # Funzione obiettivo: minimizzare z
    model.setObjective(z, GRB.MINIMIZE)

    # Vincoli sul tempo di completamento
    for i in range(n):
        model.addConstr(c[i] == s[i] + p[i], f"completion_{i}")

    # Vincoli per garantire che z sia maggiore o uguale alla somma dei tempi di completamento per entrambi i giocatori
    model.addConstr(z >= (gp.quicksum(c[i] for i in jobs1)) / (worst1 - best1), "sum_giocatore1")
    model.addConstr(z >= (gp.quicksum(c[i] for i in jobs2)) / (worst2 - best2), "sum_giocatore2")

    # Vincoli di precedenza
    for i in range(n):
        for j in range(i+1, n):
            # Caso 1: i precede j (x[i,j] = 1), allora s[j] >= c[i] - M * (1-x[i,j])
            model.addConstr(s[j] >= c[i] - M * ( 1 - x[i, j]), f"precedenza_{i}_su_{j}")
            # Caso 2: j precede i (x[i,j] = 0), allora s[i] >= c[j] - M * x[i,j]
            model.addConstr(s[i] >= c[j] - M * x[i, j], f"precedenza_{j}_su_{i}")

    # Ottimizzazione del modello
    model.optimize()

    with open(output_file, 'a') as file:  # Usa 'a' per modalità append
        # Scrivi una linea vuota per separare le esecuzioni precedenti
        file.write("\n" + "=" * 50 + "\n")  # Separatore opzionale per leggibilità

        # Stampa dei risultati
        if model.status == GRB.OPTIMAL:
            print(f"Istanza n° {id}:", file=file)
            print("Soluzione ottima trovata:", file= file)
            print(f"Valore di z: {z.x}", file= file)
            for i in range(n):
                print(f"Job {i}: inizio = {s[i].x}, completamento = {c[i].x}", file= file)
            for i in range(n):
                for j in range(i+1, n):
                        print(f"x_{i}_{j} = {x[i, j].x}", file= file)

            scheduling = sorted(range(n), key=lambda i: s[i].x)
            print("\nScheduling trovato:", file= file)
            for idx, job in enumerate(scheduling):
                print(f"Posizione {idx+1}: Job {job}", file= file)

            return round(z.x, 1)
        else:
            print("Non è stata trovata una soluzione ottima.", file= file)
            return 0


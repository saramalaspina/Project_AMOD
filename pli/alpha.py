import gurobipy as gp
from gurobipy import GRB

def alpha_pli(n, jobs1, jobs2, p, alpha, id, output_file):
    # Creazione del modello
    model = gp.Model("Solution3")
    M = sum(p) # Big M (valore molto grande)

    # Variabili di inizio e completamento per ogni job
    s = model.addVars(n, vtype=GRB.CONTINUOUS, name="s")  # Tempo di inizio
    c = model.addVars(n, vtype=GRB.CONTINUOUS, name="c")  # Tempo di completamento

    sum1 = 0
    sum2 = 0

    # Creazione delle variabili di precedenza binarie x[i,j] (x[i,j] = 1 --> job i precede job j)
    x = model.addVars([(i, j) for i in range(n) for j in range(i+1, n)],vtype=GRB.BINARY,name='x')

    obj = (alpha * gp.quicksum(c[i] for i in jobs1) + (1 - alpha) * gp.quicksum(c[i] for i in jobs2))

    # Funzione obiettivo: minimizzare la somma pesata dei tempi di completamento dei due giocatori
    model.setObjective(obj, GRB.MINIMIZE)

    # Vincoli sul tempo di completamento
    for i in range(n):
        model.addConstr(c[i] == s[i] + p[i], f"completion_{i}")

    # Vincoli di precedenza
    for i in range(n):
        for j in range(i+1, n):
            # Caso 1: i precede j (x[i,j] = 1), allora s[j] >= c[i] - M * (1-x[i,j])
            model.addConstr(s[j] >= c[i] - M * ( 1 - x[i, j]), f"precedenza_{i}_su_{j}")
            # Caso 2: j precede i (x[i,j] = 0), allora s[i] >= c[j] - M * x[i,j]
            model.addConstr(s[i] >= c[j] - M * x[i, j], f"precedenza_{j}_su_{i}")

    # Ottimizzazione del modello
    model.optimize()

    with open(output_file, 'a') as file:
        file.write("\n" + "=" * 50 + "\n")

        # Stampa dei risultati
        if model.status == GRB.OPTIMAL:
            print(f"Istanza n° {id}:", file=file)
            print("Soluzione ottima trovata:", file=file)
            print(f"Valore di obj: {round(model.objVal, 1)} per alpha {alpha}", file=file)
            for i in range(n):
                print(f"Job {i}: inizio = {round(s[i].x, 1)}, completamento = {round(c[i].x, 1)}", file=file)
            for i in range(n):
                for j in range(i+1, n):
                        print(f"x_{i}_{j} = {x[i, j].x}", file=file)

            scheduling = sorted(range(n), key=lambda i: s[i].x)
            print("\nScheduling trovato:", file=file)
            for idx, job in enumerate(scheduling):
                print(f"Posizione {idx+1}: Job {job}", file=file)

            for i in jobs1:
                sum1 += c[i].x

            for i in jobs2:
                sum2 += c[i].x

            print(f"\nPayoff giocatore 1: {round(sum1, 1)}\nPayoff giocatore 2: {round(sum2, 1)}", file=file)

            return round(model.objVal,1), round(sum1, 1), round(sum2, 1)
        else:
            print("Non è stata trovata una soluzione ottima.", file=file)
            return 0



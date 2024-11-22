import gurobipy as gp
from gurobipy import GRB

def subottimo_R(n, jobs1, jobs2, p, alpha):
    # Creazione del modello
    model = gp.Model("Solution3")
    M = sum(p)
    # Variabili di inizio e completamento per ogni job
    s = model.addVars(n, vtype=GRB.CONTINUOUS, name="s")  # Tempo di inizio
    c = model.addVars(n, vtype=GRB.CONTINUOUS, name="c")  # Tempo di completamento

    # Creazione delle variabili di precedenza continue x[i,j] (x[i,j] ∈ [0, 1])
    x = model.addVars([(i, j) for i in range(n) for j in range(i + 1, n)], vtype=GRB.CONTINUOUS, name='x')

    # Vincolo per limitare x tra 0 e 1
    for i in range(n):
        for j in range(i + 1, n):
            model.addConstr(x[i, j] >= 0, f"x_lb_{i}_{j}")
            model.addConstr(x[i, j] <= 1, f"x_ub_{i}_{j}")

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

    # Stampa dei risultati
    if model.status == GRB.OPTIMAL:
        print("Soluzione ottima trovata:")
        print(f"Valore di obj: {model.objVal}")
        for i in range(n):
            print(f"Job {i}: inizio = {s[i].x}, completamento = {c[i].x}")
        for i in range(n):
            for j in range(i+1, n):
                    print(f"x_{i}_{j} = {x[i, j].x}")

        scheduling = sorted(range(n), key=lambda i: s[i].x)
        print("\nScheduling trovato:")
        for idx, job in enumerate(scheduling):
            print(f"Posizione {idx+1}: Job {job}")
    else:
        print("Non è stata trovata una soluzione ottima.")

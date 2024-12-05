from function_utils import*
from pli.solution1 import min_max_pli


def start():

    data = read_file()

    # Iterare attraverso ogni istanza
    for instance in data:
        p = instance["p"]
        n = instance["n"]
        jobs1, jobs2 = list_jobs(n)
        min_max_pli(n, jobs1, jobs2, p)

start()



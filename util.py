def flatten(l):
    return [item for sublist in l for item in sublist]

# utility lambda functions
def nxt(k): return (k+1) % n
def conjoin(u, v): return u & v
def disjoin(u, v): return u | v

import logging

def flatten(l):
    return [item for sublist in l for item in sublist]

# utility lambda functions
def nxt(k): return (k+1) % n
def conjoin(u, v): return u & v
def disjoin(u, v): return u | v
def mergecur(x, y): 
  curstate = list(set(x['current_states'] + y['current_states']))
  nextstate = list(set(x['next_states'] + y['next_states']))
  curstate.sort()
  nextstate.sort()
  return { 'current_states': curstate, 'next_states': nextstate }


# Logger configuration
debug = False
if debug:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

# set error and warning colors
logging.addLevelName(
    logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(
    logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(
    logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

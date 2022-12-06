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

def red(msg):
    return "\033[1;31m" + msg + "\033[0m"

def green(msg):
    return "\033[1;32m" + msg + "\033[0m"

def yellow(msg):
    return "\033[1;33m" + msg + "\033[0m"

def blue(msg):
    return "\033[1;34m" + msg + "\033[0m"

def magenta(msg):
    return "\033[1;35m" + msg + "\033[0m"

def cyan(msg):
    return "\033[1;36m" + msg + "\033[0m"

def white(msg):
    return "\033[1;37m" + msg + "\033[0m"

def bold(msg):
    return "\033[1m" + msg + "\033[0m"

def underline(msg):
    return "\033[4m" + msg + "\033[0m"


class Result:
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return red("K does not ⊨ φ\n") if self.status == False else green("K ⊨ φ\n")


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
logging.addLevelName(
    logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))

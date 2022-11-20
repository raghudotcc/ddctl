import json

def read_spec(specfile):
    """Read the specification
    file and get the states,
    initial state, the 
    transition relation and 
    the CTL formula.
    """
    states = []
    init = []
    T = {}
    ap = {}
    ctlf = None

    with open(specfile, 'r') as f:
      spec = json.load(f)
      states = spec['states']
      init = spec['init']
      T = spec['T']
      ap = spec['ap']
      ctlf = spec['ctlf']

    ks = {
      'states': states,
      'init': init,
      'T': T,
      'ap': ap,
    }

    return ks, ctlf




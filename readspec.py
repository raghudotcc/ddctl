import json

def read_spec(specfile):
    """Read the specification
    file and get the states,
    initial state, the 
    transition relation and 
    the CTL formula.
    """
    states = []
    initial_states = []
    transitions = {}
    labels = {}
    ctl_formula = None
    with open(specfile, 'r') as f:
      spec = json.load(f)
      states = spec['states']
      initial_states = spec['initial_states']
      transitions = spec['transitions']
      labels = spec['labels']
      ctl_formula = spec['ctl_formula']
    kripke_structure = {
      'states': states,
      'initial_states': initial_states,
      'transitions': transitions,
      'labels': labels,
    }
    return kripke_structure, ctl_formula




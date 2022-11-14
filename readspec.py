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
    atomic_propositions = {}
    ctl_formula = None
    with open(specfile, 'r') as f:
      spec = json.load(f)
      states = spec['states']
      initial_states = spec['initial_states']
      transitions = spec['transitions']
      atomic_propositions = spec['atomic_propositions']
      ctl_formula = spec['ctl_formula']
    kripke_structure = {
      'states': states,
      'initial_states': initial_states,
      'transitions': transitions,
      'atomic_propositions': atomic_propositions,
    }
    return kripke_structure, ctl_formula




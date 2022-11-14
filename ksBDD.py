from cudd import Cudd

def bdd_transitions(kripke_structure, mgr, x, y):
  T = mgr.bddZero()
  states = kripke_structure['states']
  transitions = kripke_structure['transitions']
  n = len(bin(len(states))[2:])
  for state in states:
      state_index = states.index(state)
      state_bit_vector = bin(state_index)[2:].zfill(n)
      state_bit_vector = state_bit_vector[::-1]
      for next_state in transitions[state]:
          # get the bit vector representation of the states
          next_state_index = states.index(next_state)
          next_state_bit_vector = bin(next_state_index)[2:].zfill(n)
          next_state_bit_vector = next_state_bit_vector[::-1]
          # construct the transition relation
          transition = mgr.bddOne()
          for i in range(n):
              transition &= x[i] if state_bit_vector[i] == '1' else ~x[i]
              transition &= y[i] if next_state_bit_vector[i] == '1' else ~y[i]
          T |= (transition)
  return T


def bdd_initial_states(kripke_structure, mgr, x):
  init = mgr.bddZero()
  states = kripke_structure['states']
  initial_states = kripke_structure['initial_states']
  n = len(bin(len(states))[2:])
  for state in initial_states:
      state_index = states.index(state)
      state_bit_vector = bin(state_index)[2:].zfill(n)
      state_bit_vector = state_bit_vector[::-1]
      initial_state = mgr.bddOne()
      for i in range(n):
          initial_state &= x[i] if state_bit_vector[i] == '1' else ~x[i]
      init |= initial_state
  return init


def bdd_atomic_propositions(kripke_structure, mgr, x):
  ap = {}
  states = kripke_structure['states']
  n = len(bin(len(states))[2:])
  for state in states:
      state_index = states.index(state)
      state_bit_vector = bin(state_index)[2:].zfill(n)
      state_bit_vector = state_bit_vector[::-1]
      # some of the states may not have any atomic propositions
      if state in kripke_structure['atomic_propositions']:
          atomic_propositions = kripke_structure['atomic_propositions'][state]
          for atomic_proposition in atomic_propositions:
              atomic_proposition = atomic_proposition.lower()
              if atomic_proposition not in ap:
                ap[atomic_proposition] = mgr.bddZero()
              atomic_proposition_state = mgr.bddOne()
              for i in range(n):
                  atomic_proposition_state &= x[i] if state_bit_vector[i] == '1' else ~x[i]
              ap[atomic_proposition] |= atomic_proposition_state
  return ap


mgr = Cudd()

def KripkeStructureBDD(kripke_structure):
  states = kripke_structure['states']
  n = len(bin(len(states))[2:])
  x = [mgr.bddVar(2*i,   'x' + str(i)) for i in range(n)]
  y = [mgr.bddVar(2*i+1, 'y' + str(i)) for i in range(n)]
  T = bdd_transitions(kripke_structure, mgr, x, y)
  init = bdd_initial_states(kripke_structure, mgr, x)
  ap = bdd_atomic_propositions(kripke_structure, mgr, x)
  return init, T, ap


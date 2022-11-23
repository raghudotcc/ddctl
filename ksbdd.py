from cudd import Cudd
from util import *
from functools import reduce
import re

class ksBDD:
  """Get BDD encodings for the Kripke structure and CTL formula."""
  
  def __init__(self, ks):
    self.states = ks['states']
    self.ap = ks['ap']
    self.init = ks['init']
    self.T = ks['T']
    self.mgr = Cudd()
    self.nvar = len(bin(len(self.states))[2:])
    self.x = [self.mgr.bddVar(2*i,   'x' + str(i)) for i in range(self.nvar)]
    self.y = [self.mgr.bddVar(2*i+1, 'y' + str(i)) for i in range(self.nvar)]
    self.xcube = reduce(conjoin, self.x)
    self.ycube = reduce(conjoin, self.y)
    self.states_bit_vec = self.bdd_encodings_for_states()
  
  def bit_vec_repr(self, state):
    """
    Return the bit vector representation of a state.
    get the binary representation of the state and remove the '0b' prefix
    pad the binary representation with zeros in the front to make it nvar bits long
    reverse the binary representation to get the bit vector representation   
    """
    return bin(self.states.index(state))[2:].zfill(self.nvar)[::-1]

  def bdd_encodings_for_states(self):
    """Return the BDD encodings for the states."""
    return { state: self.bit_vec_repr(state) for state in self.states }

  def get_init_bdd(self):
    """Return the BDD encoding for the initial states."""
    init_bdd = self.mgr.bddZero()
    for state in self.init:
      initc_bdd = self.mgr.bddOne()
      for i in range(self.nvar):
        initc_bdd &= self.x[i] if self.states_bit_vec[state][i] == '1' else ~self.x[i]
      init_bdd |= initc_bdd
    return init_bdd

  def get_T_bdd(self):
    """Return the BDD encoding for the transitions."""
    T_bdd = self.mgr.bddZero()
    for state in self.states:
      for successor in self.T[state]:
        Tc_bdd = self.mgr.bddOne()
        for i in range(self.nvar):
          Tc_bdd &= self.x[i] if self.states_bit_vec[state][i] == '1' else ~self.x[i]
          Tc_bdd &= self.y[i] if self.states_bit_vec[successor][i] == '1' else ~self.y[i]
        T_bdd |= Tc_bdd
    return T_bdd

  def get_ap_bdd(self):
    """Return the BDD encodings for the atomic propositions."""
    ap_bdd = { apc : self.mgr.bddZero() for apc in flatten(self.ap.values()) }
    for state in self.ap:
      aps = self.ap[state]
      for apc in aps:
        apc_bdd = self.mgr.bddOne()
        for i in range(self.nvar):
          apc_bdd &= self.x[i] if self.states_bit_vec[state][i] == '1' else ~self.x[i]
        ap_bdd[apc] |= apc_bdd
    return ap_bdd

  def infer(self, encoding):
    """Return the inferred states."""
    encoding = str(encoding)
    inferred_states = [] 
    
    dnf = re.split(r'\|\s*(?![^()]*\))', encoding)
    for cube in dnf:
      if '(' in cube:
        dnf.remove(cube)
        inside_parentheses = re.findall(r'\((.*?)\)', cube)
        # inefficient - remove double list and a flatten
        inside_parentheses = flatten([s.split(' | ') for s in inside_parentheses])
        outside_parentheses = re.sub(r'\((.*?)\)', '', cube)
        
        for item in inside_parentheses:
          cube = outside_parentheses + item
          dnf.append(cube)

    for cube in dnf:
      curr_states = self.get_states_from_bdd('x', cube, encoding)
      next_states = self.get_states_from_bdd('y', cube)
          
      inferred_states.append({ 'current_states': curr_states, 'next_states': next_states })
    
      
    return inferred_states
    
    
  def get_states_from_bdd(self, var, cube, encoding=None):
    if (encoding == 'true'):
      return self.states
    elif (encoding == 'false'):
      return []
    else:
      v = re.findall(r'[~]?' + var + r'\d+', cube)
      states = []
      if v:
        for state in self.states:
          # check if the state satisfies the cube
          for i in range(self.nvar):
            if var + str(i) in v:
              if self.states_bit_vec[state][i] == '0':
                break
            elif '~' + var + str(i) in v:
              if self.states_bit_vec[state][i] == '1':
                break
          else:
            states.append(state)
      return states

    
      
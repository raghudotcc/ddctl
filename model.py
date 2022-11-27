from ksbdd import *
import parser
import ast
import graphviz
from util import *
import subprocess
import uuid


class Model:
  def __init__(self, ks, ctlf_ast, include_init=False, output=None):
    self.ctlf_ast = ctlf_ast
    self.ctl_visitor = CTLVisitor(ks, include_init, output)

  def check(self):
    """Check the CTL formula"""
    return self.ctl_visitor.visit(self.ctlf_ast)


class CTLVisitor(ast.NodeVisitor):
  def __init__(self, ks, include_init=False, output=None):
    self.ks = ks
    self.ksbdd = ksBDD(ks)
    self.init = self.ksbdd.get_init_bdd()
    self.T = self.ksbdd.get_T_bdd()
    self.ap = self.ksbdd.get_ap_bdd()
    self.include_init = include_init
    self.output = output
    self.graph = graphviz.Digraph(format='png',
                                  graph_attr={'rankdir': 'BT', 'splines': 'ortho'})

  def image(self, TR, From):
    """ Computes image with transition relation. """
    ImgY = TR.andAbstract(From, self.ksbdd.xcube)
    return ImgY.swapVariables(self.ksbdd.y, self.ksbdd.x)

  def preimage(self, TR, From):
    """Compute the predecessor of From"""
    fromY = From.swapVariables(self.ksbdd.x, self.ksbdd.y)
    return TR.andAbstract(fromY, self.ksbdd.ycube)

  def computeEG(self, phi):
    """EG phi greatest fixpoint computation"""
    Z = phi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z &= self.preimage(self.T, Z)
    if self.include_init:
      return Z if self.init <= Z else self.ksbdd.mgr.bddZero()
    else:
      return Z

  def computeEF(self, phi):
    """EF phi least fixpoint computation"""
    Z = phi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z |= self.image(self.T, Z)
    if self.include_init:
      return Z if self.init <= Z else self.ksbdd.mgr.bddZero()
    else:
      return Z

  def computeEU(self, phi, psi):
    """Compute the EU of phi and psi"""
    Z = psi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z = self.computeOr(Z, self.computeAnd(phi, self.preimage(self.T, Z)))
    if self.include_init:
      return Z if self.init <= Z else self.ksbdd.mgr.bddZero()
    else:
      return Z

  def computeEX(self, phi):
    """Compute the EX of phi"""
    return self.preimage(self.T, phi)

  def computeNot(self, phi):
    """Compute the negation of phi"""
    return ~phi

  def computeAnd(self, phi, psi):
    """Compute the conjunction of phi and psi"""
    return phi & psi

  def computeOr(self, phi, psi):
    """Compute the disjunction of phi and psi"""
    return phi | psi

  def computeImplies(self, phi, psi):
    """Compute the implication of phi and psi"""
    return self.computeOr(self.computeNot(phi), psi)

  def visit_Module(self, node):
    module = self.visit(node.body)
    if self.output:
      # if the output filename contains .png, then remove it
      if self.output.endswith('.png'):
        self.output = self.output[:-4]
      self.graph.render(self.output)
    return module

  def visit_EU(self, node):
    """Visit the EU node"""
    phi, phi_iden = self.visit(node.arg1)
    psi, psi_iden = self.visit(node.arg2)
    eu = self.computeEU(phi, psi)

    label = 'EU\n' + \
        str(reduce(mergecur, self.ksbdd.infer(eu))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)
    self.graph.edge(psi_iden, iden)
    return (eu, iden)

  def visit_EG(self, node):
    """Visit the EG node"""
    phi, phi_iden = self.visit(node.arg)
    eg = self.computeEG(phi)

    label = 'EG\n' + \
        str(reduce(mergecur, self.ksbdd.infer(eg))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)

    return (eg, iden)

  def visit_EF(self, node):
    """Visit the EF node"""
    phi, phi_iden = self.visit(node.arg)
    ef = self.computeEF(phi)

    label = 'EF\n' + \
        str(reduce(mergecur, self.ksbdd.infer(ef))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)

    return (ef, iden)

  def visit_EX(self, node):
    """Visit the EX node"""
    phi, phi_iden = self.visit(node.arg)
    ex = self.computeEX(phi)

    label = 'EX\n' + \
        str(reduce(mergecur, self.ksbdd.infer(ex))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)

    return (ex, iden)

  def visit_Not(self, node):
    """Visit the Not node"""
    phi, phi_iden = self.visit(node.arg)
    nt = self.computeNot(phi)

    label = '¬ \n' + \
        str(reduce(mergecur, self.ksbdd.infer(nt))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)

    return (nt, iden)

  def visit_And(self, node):
    """Visit the And node"""
    phi, phi_iden = self.visit(node.arg1)
    psi, psi_iden = self.visit(node.arg2)
    nd = self.computeAnd(phi, psi)

    label = '∧ \n' + \
        str(reduce(mergecur, self.ksbdd.infer(nd))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)
    self.graph.edge(psi_iden, iden)

    return (nd, iden)

  def visit_Or(self, node):
    """Visit the Or node"""
    phi, phi_iden = self.visit(node.arg1)
    psi, psi_iden = self.visit(node.arg2)
    r = self.computeOr(phi, psi)

    label = '∨ \n' + \
        str(reduce(mergecur, self.ksbdd.infer(r))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)
    self.graph.edge(psi_iden, iden)

    return (r, iden)

  def visit_Implies(self, node):
    """Visit the Implies node"""
    phi, phi_iden = self.visit(node.arg1)
    psi, psi_iden = self.visit(node.arg2)
    imp = self.computeImplies(phi, psi)

    label = '→ \n' + \
        str(reduce(mergecur, self.ksbdd.infer(imp))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)
    self.graph.edge(phi_iden, iden)
    self.graph.edge(psi_iden, iden)

    return (imp, iden)
  
  def visit_AtomicProposition(self, node):
    """Visit the AtomicProposition node"""
    lbl = self.ap[node.arg]

    label = node.arg + '\n' + \
        str(reduce(mergecur, self.ksbdd.infer(lbl))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)

    return (lbl, iden)

  def visit_TRUE(self, node):
    """Visit the True node"""
    als = self.ksbdd.mgr.bddOne()

    label = 'TRUE\n' + \
        str(reduce(mergecur, self.ksbdd.infer(als))['current_states'])
    iden = uuid.uuid4().hex
    self.graph.node(iden, label)

    return (als, iden)

  def visit_FALSE(self, node):
    """Visit the False node"""
    als = self.ksbdd.mgr.bddZero()

    label = 'FALSE\n' + \
        str(reduce(mergecur, self.ksbdd.infer(als))['current_states'])

    iden = uuid.uuid4().hex
    self.graph.node(iden, label)

    return (als, iden)
  


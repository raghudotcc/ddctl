from ksbdd import *
import parser
import ast


class Model:
  def __init__(self, ks, ctlf_ast):
    self.ctlf_ast = ctlf_ast
    self.ctl_visitor = CTLVisitor(ks)

  def check(self):
    """Check the CTL formula"""
    return self.ctl_visitor.visit(self.ctlf_ast)


class CTLVisitor(ast.NodeVisitor):
  def __init__(self, ks):
    self.ks = ks
    self.ksbdd = ksBDD(ks)
    self.init = self.ksbdd.get_init_bdd()
    self.T = self.ksbdd.get_T_bdd()
    self.ap = self.ksbdd.get_ap_bdd()

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
    return Z

  def computeEF(self, phi):
    """EF phi least fixpoint computation"""
    Z = phi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z |= self.image(self.T, Z)
    return Z

  def computeEU(self, phi, psi):
    """Compute the EU of phi and psi"""
    Z = psi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z = self.computeOr(Z, self.computeAnd(phi, self.preimage(self.T, Z)))
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
    print("Module: ", self.ksbdd.infer(module))
    return module

  def visit_EU(self, node):
    """Visit the EU node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    eu = self.computeEU(phi, psi)
    print("EU: ", self.ksbdd.infer(eu))
    return eu

  def visit_EG(self, node):
    """Visit the EG node"""
    phi = self.visit(node.arg)
    eg = self.computeEG(phi)
    print("EG: ", self.ksbdd.infer(eg))
    return eg

  def visit_EF(self, node):
    """Visit the EF node"""
    phi = self.visit(node.arg)
    ef = self.computeEF(phi)
    print("EF: ", self.ksbdd.infer(ef))

  def visit_EX(self, node):
    """Visit the EX node"""
    phi = self.visit(node.arg)
    ex = self.computeEX(phi)
    print("EX: ", self.ksbdd.infer(ex))
    return ex

  def visit_Not(self, node):
    """Visit the Not node"""
    phi = self.visit(node.arg)
    nt = self.computeNot(phi)
    print("Not: ", self.ksbdd.infer(nt))
    return nt

  def visit_And(self, node):
    """Visit the And node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    nd = self.computeAnd(phi, psi)
    print("And: ", self.ksbdd.infer(nd))
    return nd

  def visit_Or(self, node):
    """Visit the Or node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    r = self.computeOr(phi, psi)
    print("Or: ", self.ksbdd.infer(r))
    return r

  def visit_Implies(self, node):
    """Visit the Implies node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    imp = self.computeImplies(phi, psi)
    print("Implies: ", self.ksbdd.infer(imp))
    return imp
  
  def visit_AtomicProposition(self, node):
    """Visit the AtomicProposition node"""
    lbl = self.ap[node.arg]
    print("%s : " % node.arg, self.ksbdd.infer(lbl))
    return lbl

  def visit_TRUE(self, node):
    """Visit the True node"""
    als = self.ksbdd.mgr.bddOne()
    print("TRUE: ", self.ksbdd.infer(als))
    return als

  def visit_FALSE(self, node):
    """Visit the False node"""
    als = self.ksbdd.mgr.bddZero()
    print("FALSE: ", self.ksbdd.infer(als))
    return als

  

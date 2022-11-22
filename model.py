from ksbdd import *
import parser
import ast

class Model:
  def __init__(self, ks, ctlf):
    self.ks = ks
    self.ctl_ast = parser.parse(ctlf)
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
    return Z if self.init <= Z else self.ksbdd.mgr.bddZero()

  def computeEF(self, phi):
    """EF phi least fixpoint computation"""
    Z = phi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z |= self.image(self.T, Z)
    return Z if self.init <= Z else self.ksbdd.mgr.bddZero()

  def computeEU(self, phi, psi):
    """Compute the EU of phi and psi"""
    Z = psi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z = self.computeOr(Z, self.computeAnd(phi, self.preimage(self.T, Z)))
    return Z if self.init <= Z else self.ksbdd.mgr.bddZero()

  def computeEX(self, phi):
    """Compute the EX of phi"""
    return self.image(self.T, phi)
  
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

  def check(self):
    """Check the CTL formula"""
    return self.computeEG(~self.ap['p'])
    
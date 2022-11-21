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

  def pre(self, TR, From):
    """Compute the predecessor of From"""
    fromY = From.swapVariables(self.ksbdd.x, self.ksbdd.y)
    return TR.andAbstract(fromY, self.ksbdd.ycube)

  def EG(self, phi):
    """EG phi greatest fixpoint computation"""
    Z = phi
    zeta = self.ksbdd.mgr.bddZero()
    while Z != zeta:
      zeta = Z
      Z &= self.pre(self.T, Z)
    return self.kssbdd.infer(Z)

  def check(self):
    """Check the CTL formula"""
    pass





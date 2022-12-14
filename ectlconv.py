from nodes import *
import ast
import nodes

class ECTLConverter(ast.NodeTransformer):
  def visit_Module(self, node):
    return Module(self.visit(node.body))

  def same(self, node1, node2):
    """Check if two nodes are the same"""
    return ast.dump(node1) == ast.dump(node2)

  def ectl(self, node):
    new = node
    node = self.visit(node)
    while not self.same(node, new):
      new = node
      node = self.visit(node)

    # send new, node changes inside the for loop 
    # because of the ast.walk
    for node in ast.walk(node):
      if isinstance(node, nodes.Not):
        if not isinstance(node.arg, nodes.AtomicProposition):
          return (False, new)
    return (True, new)

  def visit_AX(self, node):
    """Visit the AX node"""
    return Not(EX(Not(self.visit(node.arg))))

  def visit_AG(self, node):
    """Visit the AG node"""
    return Not(EF(Not(self.visit(node.arg))))

  def visit_AF(self, node):
    """Visit the AF node"""
    return Not(EG(Not(self.visit(node.arg))))

  def visit_AU(self, node):
    """Visit the AU node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    # A ψ U φ = ¬((E ¬φ U ¬(φ ∨ ψ)) ∨ EG ¬φ)
    return Not(Or(EU(Not(psi), Not(Or(phi, psi))), EG(Not(phi))))

  def visit_EU(self, node):
    """Visit the EU node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    return EU(phi, psi)

  def visit_EG(self, node):
    """Visit the EG node"""
    phi = self.visit(node.arg)
    return EG(phi)

  def visit_EF(self, node):
    """Visit the EF node"""
    phi = self.visit(node.arg)
    return EU(TRUE(), phi)

  def visit_EX(self, node):
    """Visit the EX node"""
    phi = self.visit(node.arg)
    return EX(phi)

  def visit_Not(self, node):
    """Visit the Not node"""
    # distribute the negation
    if isinstance(node.arg, nodes.And):
      return Or(Not(self.visit(node.arg.arg1)), Not(self.visit(node.arg.arg2)))
    elif isinstance(node.arg, nodes.Or):
      return And(Not(self.visit(node.arg.arg1)), Not(self.visit(node.arg.arg2)))
    elif isinstance(node.arg, nodes.Implies):
      return And(self.visit(node.arg.arg1), Not(self.visit(node.arg.arg2)))
    elif isinstance(node.arg, nodes.Not):
      return self.visit(node.arg.arg)
    else:
      return Not(self.visit(node.arg))


  def visit_And(self, node):
    """Visit the And node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    if self.same(phi, psi):
      return phi
    return And(phi, psi)

  def visit_Or(self, node):
    """Visit the Or node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    if self.same(phi, psi):
      return phi
    return Or(phi, psi)


  def visit_Implies(self, node):
    """Visit the Implies node"""
    phi = self.visit(node.arg1)
    psi = self.visit(node.arg2)
    return Or(Not(phi), psi)

  def visit_AtomicProposition(self, node):
    return node

  def visit_TRUE(self, node):
    return node

  def visit_FALSE(self, node):
    return node
from ast import *

class A(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'A(%s)' % repr(self.arg)

class AX(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'AX(%s)' % repr(self.arg)

class AF(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'AF(%s)' % repr(self.arg)

class AG(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'AG(%s)' % repr(self.arg)

class AU(AST):
  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self._fields = ['arg1', 'arg2']

  def getChildren(self):
    return [self.arg1, self.arg2]

  def getChildNodes(self):
    return [self.arg1, self.arg2]

  def __repr__(self):
    return 'AU(%s, %s)' % (repr(self.arg1), repr(self.arg2))

class E(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'E(%s)' % repr(self.arg)

class EX(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'EX(%s)' % repr(self.arg)

class EF(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'EF(%s)' % repr(self.arg)

class EG(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'EG(%s)' % repr(self.arg)

class EU(AST):
  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self._fields = ['arg1', 'arg2']

  def getChildren(self):
    return [self.arg1, self.arg2]

  def getChildNodes(self):
    return [self.arg1, self.arg2]

  def __repr__(self):
    return 'EU(%s, %s)' % (repr(self.arg1), repr(self.arg2))


class Not(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'Not(%s)' % repr(self.arg)

class And(AST):
  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self._fields = ['arg1', 'arg2']

  def getChildren(self):
    return [self.arg1, self.arg2]

  def getChildNodes(self):
    return [self.arg1, self.arg2]

  def __repr__(self):
    return 'And(%s, %s)' % (repr(self.arg1), repr(self.arg2))

class Or(AST):
  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self._fields = ['arg1', 'arg2']

  def getChildren(self):
    return [self.arg1, self.arg2]

  def getChildNodes(self):
    return [self.arg1, self.arg2]

  def __repr__(self):
    return 'Or(%s, %s)' % (repr(self.arg1), repr(self.arg2))

class Implies(AST):
  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self._fields = ['arg1', 'arg2']

  def getChildren(self):
    return [self.arg1, self.arg2]

  def getChildNodes(self):
    return [self.arg1, self.arg2]

  def __repr__(self):
    return 'Implies(%s, %s)' % (repr(self.arg1), repr(self.arg2))

class AtomicProposition(AST):
  def __init__(self, arg):
    self.arg = arg
    self._fields = ['arg']

  def getChildren(self):
    return [self.arg]

  def getChildNodes(self):
    return [self.arg]

  def __repr__(self):
    return 'AtomicProposition(%s)' % repr(self.arg)

class TRUE(AST):
  def __init__(self):
    self._fields = []

  def getChildren(self):
    return []

  def getChildNodes(self):
    return []

  def __repr__(self):
    return 'TRUE'

class FALSE(AST):
  def __init__(self):
    self._fields = []

  def getChildren(self):
    return []

  def getChildNodes(self):
    return []

  def __repr__(self):
    return 'FALSE'
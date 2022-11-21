"""Parse ctl formulas using ply."""

import ply.yacc as yacc
import ply.lex as lex
import ast
from ast import *
from nodes import *
from grammar import *
import logging


class Lexer:
    reserved = {
        'A' : 'A',
        'E' : 'E',
        'U' : 'U',
        'AG' : 'AG',
        'EG' : 'EG',
        'AF' : 'AF',
        'EF' : 'EF',
        'AX' : 'AX',
        'EX' : 'EX',
    }

    tokens = [
        'atomic_proposition',
        'LPAREN',
        'RPAREN',
        'AND',
        'OR',
        'IMPLIES',
        'NOT',
        'WHITESPACE',
        'FALSE',
        'TRUE',
    ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_AND = r'&'
    t_OR = r'\|'
    t_IMPLIES = r'->'
    t_NOT = r'!'
    t_WHITESPACE = r'\s+'
    t_ignore = ' \t'


    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.lexer.begin('INITIAL')

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def t_FALSE(self, t):
        r'false|False|FALSE'
        t.value = False
        return t
    
    def t_TRUE(self, t):
        r'true|True|TRUE'
        t.value = True
        return t
        
    
    def t_atomic_proposition(self, t):
        r'[a-zA-Z0-9_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'atomic_proposition')
        return t        

    def t_error(self, t):
        raise Exception('Illegal character %s' % t.value[0])


class Parser(object):
  '''
  Available node types:
  A(), E(), AU(), AG(), EG(), AF(), EF(), AX(), EX(), EU()
  Not(), And(), Or(), Implies()
  '''
  tokens = Lexer.tokens

  precendence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IMPLIES'),
    ('left', 'A', 'E'),
    ('left', 'U'),
    ('left', 'AX', 'EX', 'AF', 'EF', 'AG', 'EG'),
  )

  def __init__(self, subset):
    self.functions = [getattr(Parser, f)
                          for f in dir(self) if f.startswith('p_')]
    for fattr in grammar[subset]:
        ply_fun, production = fattr
        for f in self.functions:
            if f.__name__ == ply_fun:
                f.__doc__ = production
    self.parser = yacc.yacc(module=self)

  def parse(self, ctl_formula):
      self.parsedata = ctl_formula
      return self.parser.parse(ctl_formula, lexer=Lexer())

  def p_ctl(self, p):      
      p[0] = Module(p[1])
      logging.debug('p_start: %s' % ast.dump(p[0]))

  def p_paren_expr(self, p):      
      p[0] = p[2]
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_true_expr(self, p):      
      p[0] = TRUE()
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_false_expr(self, p):      
      p[0] = FALSE()
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_atomic_proposition_expr(self, p):      
      p[0] = AtomicProposition(p[1])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_not_expr(self, p):      
      p[0] = Not(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_and_expr(self, p):      
      p[0] = And(p[1], p[3])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_or_expr(self, p):      
      p[0] = Or(p[1], p[3])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_implies_expr(self, p):      
      p[0] = Implies(p[1], p[3])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_A_expr(self, p):      
      p[0] = A(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_E_expr(self, p):      
      p[0] = E(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_AU_expr(self, p):      
      p[0] = AU(p[2], p[4])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_EU_expr(self, p):      
      p[0] = EU(p[2], p[4])
      logging.debug('p_ctl_expr: %s' % p[0])
      
  def p_AG_expr(self, p):      
      p[0] = AG(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_EG_expr(self, p):      
      p[0] = EG(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_AF_expr(self, p):      
      p[0] = AF(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])
  
  def p_EF_expr(self, p):      
      p[0] = EF(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_AX_expr(self, p):      
      p[0] = AX(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_EX_expr(self, p):      
      p[0] = EX(p[2])
      logging.debug('p_ctl_expr: %s' % p[0])

  def p_error(self, p):
      # use logging.error and give a more detailed error message
      # e.g. "Syntax error at '%s'" % p.value and color the error
        # in the formula
      dummy = 'Syntax error in formula '
      logging.error('Syntax error in formula: %s' % self.parsedata)
      for char in self.parsedata:
        if char == p.value:
            logging.error(
                ' ' * (len(dummy) + self.parsedata.index(char) - 1) + '\033[1;31m^\033[0m')
            break

                
    


# Logger configuration
debug = False
if debug:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

# set error and warning colors
logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))


# set up parser
def parse(ctl_formula, subset='ctl'):
    parser = Parser(subset)
    return parser.parse(ctl_formula)
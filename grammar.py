"""Grammar file for specifying the CTL formulas.

Note:
Ply uses docstring to generate the parser. We 
use this feature to enable isolating the grammar from
the parser logic. Unless you need to introduce a new 
node type, you should not need to change the parser 
logic in parse.py. For creating a new lang with 
existing node types, adding a new entry to 
the grammar dict should be sufficient.
"""

grammar = {
    'ctl' : [
        ('p_ctl', """ctl : ctl_expr"""),
        ('p_paren_expr', """ctl_expr : LPAREN ctl_expr RPAREN"""),
        ('p_true_expr', """ctl_expr : TRUE"""),
        ('p_false_expr', """ctl_expr : FALSE"""),
        ('p_label_expr', """ctl_expr : label"""),
        ('p_not_expr', """ctl_expr : NOT ctl_expr"""),
        ('p_and_expr', """ctl_expr : ctl_expr AND ctl_expr"""),
        ('p_or_expr', """ctl_expr : ctl_expr OR ctl_expr"""),
        ('p_implies_expr', """ctl_expr : ctl_expr IMPLIES ctl_expr"""),
        ('p_A_expr', """ctl_expr : A ctl_expr"""),
        ('p_E_expr', """ctl_expr : E ctl_expr"""),
        ('p_AU_expr', """ctl_expr : A ctl_expr U ctl_expr"""),
        ('p_EU_expr', """ctl_expr : E ctl_expr U ctl_expr"""),
        ('p_AG_expr', """ctl_expr : AG ctl_expr"""),
        ('p_EG_expr', """ctl_expr : EG ctl_expr"""),
        ('p_AF_expr', """ctl_expr : AF ctl_expr"""),
        ('p_EF_expr', """ctl_expr : EF ctl_expr"""),
        ('p_AX_expr', """ctl_expr : AX ctl_expr"""),
        ('p_EX_expr', """ctl_expr : EX ctl_expr"""),
    ],
}

# -*- coding: utf-8 -*-
"""
Genomy
A programming language inspired by genomics
"""

import re
sIDENTIFIER = "[^-+#: ]+"
IDENTIFIER = re.compile(sIDENTIFIER)
ENHANCER = re.compile("\+\s*(%s)" % sIDENTIFIER)
SUPPRESSOR = re.compile("-\s*(%s)" % sIDENTIFIER)
BODY = re.compile(":\s*(%s)" % sIDENTIFIER)
CODE = """
+START :OUT_H
+OUT_H :OUT_E
+OUT_E :OUT_L
-SUP_L +OUT_L :OUT_L
+OUT_L :SUP_L
-SUP_O +SUP_L :OUT_O :SUP_O
"""
NONE = "NONE" # it always be in environment

class Gene(object):
    def __init__(self, body, enhancer, suppressor):
        self.body = body
        self.enhancer = enhancer
        self.suppressor = suppressor
    
    def __call__(self, env):
        if any(s in e for e in env for s in self.suppressor):
            return NONE
        if any(s in e for e in env for s in self.enhancer):
            return self.body
        return NONE

    def __repr__(self):
        buf = []
        buf += ["-%s" % s for s in self.suppressor]
        buf += ["+%s" % s for s in self.enhancer]
        buf += [":%s" % self.body]
        return " ".join(buf)


def parse(code):
    genes = []
    for line in CODE.split("\n"):
        if line.startswith("#"):
            continue # comment line

        enhancer = re.findall(ENHANCER, line)
        suppressor = re.findall(SUPPRESSOR, line)
        body = re.findall(BODY, line)
        for b in body:
            genes.append(Gene(b, enhancer, suppressor))

    return genes


def run(genes, env=[]):
    if isinstance(env, list): env = set(env)
    if not NONE in env: env.add(NONE)
    return set(g(env) for g in genes)


def show_env(env):
    """
    ignore "NONE" protein and pretty print
    """
    if NONE in env:
        env = env.copy()
        env.remove(NONE)
    print " ".join(sorted(env))

genes = parse(CODE)
print genes
env = set(["START"])
show_env(env)
for i in range(10):
    env = run(genes, env)
    show_env(env)


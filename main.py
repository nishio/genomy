# -*- coding: utf-8 -*-
"""
Genomy
A programming language inspired by genomics
"""
import re
import sys
import argparse

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
    for line in code.split("\n"):
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


def repr_env(env):
    """
    ignore "NONE" protein and pretty print
    """
    if NONE in env:
        env = env.copy()
        env.remove(NONE)
    return " ".join(sorted(env))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='read code from file')
    parser.add_argument('-n', '--num', help='number of iteration', default=10)
    parser.add_argument('--show_genes', help='show genes before run', action='store_true')
    parser.add_argument('environment', metavar='P', type=str, nargs='*',
                        help='proteins in initial environment')

    args = parser.parse_args()
    if args.file:
        code = file(args.file).read()
    else:
        code = sys.stdin.read()
    genes = parse(code)

    if args.show_genes:
        print genes

    env = set(args.environment)
    print 0, repr_env(env)
    for i in range(10):
        env = run(genes, env)
        print i + 1, repr_env(env)


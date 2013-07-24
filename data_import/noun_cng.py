#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict

words = defaultdict(set)

with open("sblgnt.txt") as f:
    for line in f:
        bcv, ccat_pos, ccat_parse, robinson, text, word, form, lemma = line.strip().split()
        if ccat_pos == "N-" and robinson.startswith("N-"):
            if "@" not in robinson:
                if "-S" not in robinson and "-C" not in robinson:
                    if "-LI" not in robinson and "-OI" not in robinson:
                        if "-PRI" not in robinson:
                            if form.endswith("(ν)"):
                                words[form[:-4]].add(robinson[2:])
                                words[form[:-4] + "ν"].add(robinson[2:])
                            else:
                                words[form].add(robinson[2:])

for word in sorted(words):
    print word, "|".join(sorted(words[word]))
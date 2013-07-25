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
                            if robinson[2] != "V":
                                if form.endswith("(ν)"):
                                    words[form[:-4]].add(robinson[2:])
                                    words[form[:-4] + "ν"].add(robinson[2:])
                                else:
                                    words[form].add(robinson[2:])

exclude = [
    "APF|APM",
    "APF|GSF",
    "APF|NPF",
    "APM|NPM",
    "ASN|NSM|NSN",
    "DSF|DSM",
    "DSM|GSM",
    "GSF|GSM",
    "GSM|NSF",
    "NPF|NPM",
    "NSF|NSM",
    "ASF|ASM",
    "ASF|ASN",
    "ASF|NSF",
    "ASM|GSM",
]


for word in sorted(words):
    parses = "|".join(sorted(words[word]))
    if parses not in exclude:
        if parses in ["APN|NPN", "ASN|NSN"]:
            parses = "C" + parses[1:3]
        if parses[2] == "N" and parses[0] in ["N", "A"]:
            parses = "C" + parses[1:3]
        print word, parses

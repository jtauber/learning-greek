# coding: utf-8

import unicodedata

# from accentuation import recessive


def remove_diacritic(*diacritics):
    """
    Given a collection of Unicode diacritics, return a function that takes a
    string and returns the string without those diacritics.
    """
    def _(text):
        return unicodedata.normalize("NFC", "".join(
            ch
            for ch in unicodedata.normalize("NFD", text)
            if ch not in diacritics)
        )
    return _

OXIA = ACUTE = "\u0301"
VARIA = GRAVE = "\u0300"
PERISPOMENI = CIRCUMFLEX = "\u0342"

remove = remove_diacritic(ACUTE, GRAVE, CIRCUMFLEX)


def load_file(filename, fields):
    with open(filename) as fd:
        for line in fd:
            row = line.split("#")[0].strip()
            if row:
                yield dict(zip(fields, row.split("|")))


verbs = list(load_file("raw_course_data/verbs.txt", ["chapter", "lemma", "principal-parts", "active-gloss", "middle-gloss"]))
nouns = list(load_file("raw_course_data/nouns.txt", ["chapter", "citation-form", "tags", "gloss"]))
adjectives = list(load_file("raw_course_data/adjectives.txt", ["chapter", "citation-form", "gloss"]))
others = list(load_file("raw_course_data/other.txt", ["chapter", "citation-form", "gloss"]))
articles = list(load_file("raw_course_data/article.txt", ["cng", "form"]))
demonstratives1 = list(load_file("raw_course_data/demonstrative1.txt", ["cng", "form"]))
demonstratives2 = list(load_file("raw_course_data/demonstrative2.txt", ["cng", "form"]))

# def get_nominal_forms(noun, NS, GS, ART):
#     if NS.endswith("ᾱ") and GS.endswith("ᾱς") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ᾳ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-1] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", NS + "ς")
#         ]
#     elif NS.endswith("ᾱ́") and GS.endswith("ᾶς") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ᾷ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-2] + "αί"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αῖς"),
#             ("AP", NS + "ς")
#         ]
#     elif NS.endswith("ή") and GS.endswith("ῆς") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῇ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-2] + "αί"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αῖς"),
#             ("AP", NS[:-1] + "ᾱ́ς")
#         ]
#     elif NS.endswith("η") and GS.endswith("ης") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῃ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-2] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", NS[:-1] + "ᾱς")
#         ]
#     elif NS.endswith("ῆ") and GS.endswith("ῆς") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῇ"),
#             ("AS", NS + "ν")
#         ]
#     elif NS.endswith("ος") and GS.endswith("ου") and ART in ["ὁ", "ἡ", "ὁ or ἡ"]:
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῳ"),
#             ("AS", NS[:-2] + "ον"),
#             ("VS", NS[:-2] + "ε"),
#             ("NP", NS[:-2] + "οι"),
#             ("GP", GS[:-2] + "ων"),
#             ("DP", GS[:-2] + "οις"),
#             ("AP", NS[:-2] + "ους")
#         ]
#     elif NS.endswith("όν") and GS.endswith("οῦ") and ART == "τό":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῷ"),
#             ("AS", NS),
#             ("NP", NS[:-2] + "ά"),
#             ("GP", GS[:-2] + "ῶν"),
#             ("DP", GS[:-2] + "οῖς"),
#             ("AP", NS[:-2] + "ά")
#         ]
#     elif NS.endswith("ον") and GS.endswith("ου") and ART == "τό":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῳ"),
#             ("AS", NS),
#             ("NP", NS[:-2] + "α"),
#             ("GP", GS[:-2] + "ων"),
#             ("DP", GS[:-2] + "οις"),
#             ("AP", NS[:-2] + "α")
#         ]
#     elif NS.endswith("ός") and GS.endswith("οῦ") and ART in ["ὁ", "ἡ", "ὁ or ἡ"]:
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῷ"),
#             ("AS", NS[:-2] + "όν"),
#             ("VS", NS[:-2] + "έ"),
#             ("NP", NS[:-2] + "οί"),
#             ("GP", GS[:-2] + "ῶν"),
#             ("DP", GS[:-2] + "οῖς"),
#             ("AP", NS[:-2] + "ούς")
#         ]
#     elif NS.endswith("α") and GS.endswith("ᾱς") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ᾳ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-1] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", GS[:-2] + "ᾱς")
#         ]
#     elif NS.endswith("α") and GS.endswith("ης") and ART == "ἡ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῃ"),
#             ("AS", NS + "ν"),
#             ("VS", NS),
#             ("NP", NS[:-1] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", GS[:-2] + "ᾱς")
#         ]
#     elif NS.endswith("ᾱς") and GS.endswith("ου") and ART == "ὁ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ᾳ"),
#             ("AS", NS[:-1] + "ν"),
#             ("VS", NS[:-1]),
#             ("NP", NS[:-2] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", GS[:-2] + "ᾱς")
#         ]
#     elif NS.endswith("ης") and GS.endswith("ου") and ART == "ὁ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῃ"),
#             ("AS", NS[:-1] + "ν"),
#             ("VS", NS[:-2] + "α") if NS.endswith("της") else ("VS", NS[:-1]),
#             ("NP", NS[:-2] + "αι"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αις"),
#             ("AP", GS[:-2] + "ᾱς")
#         ]
#     elif NS.endswith("ής") and GS.endswith("οῦ") and ART == "ὁ":
#         return [
#             ("NS", NS),
#             ("GS", GS),
#             ("DS", GS[:-2] + "ῇ"),
#             ("AS", NS[:-1] + "ν"),
#             ("VS", NS[:-2] + "ά") if NS.endswith("τής") else ("VS", NS[:-1]),
#             ("NP", NS[:-2] + "αί"),
#             ("GP", remove(GS[:-2]) + "ῶν"),
#             ("DP", GS[:-2] + "αῖς"),
#             ("AP", GS[:-2] + "ᾱ́ς")
#         ]
#     else:
#         raise Exception("unknown citation form pattern", NS, GS, ART)
#
#
# PRIMARY_ACTIVE = {
#     "1S": "ω",
#     "2S": "εις",
#     "3S": "ει",
#     "1P": "ομεν",
#     "2P": "ετε",
#     "3P": "ουσι(ν)",
# }
#
# PRIMARY_MIDDLE = {
#     "1S": "ομαι",
#     "2S": "ῃ/ει",
#     "3S": "εται",
#     "1P": "ομεθα",
#     "2P": "εσθε",
#     "3P": "ονται",
# }
#
# SECONDARY_ACTIVE = {
#     "1S": "ον",
#     "2S": "ες",
#     "3S": "ε(ν)",
#     "1P": "ομεν",
#     "2P": "ετε",
#     "3P": "ον",
# }
#
# SECONDARY_MIDDLE = {
#     "1S": "ομην",
#     "2S": "ου",
#     "3S": "ετο",
#     "1P": "ομεθα",
#     "2P": "εσθε",
#     "3P": "οντο",
# }
#
#
# d1 = {
#     "PA": (1,  0, -1, "",   PRIMARY_ACTIVE),
#     "PM": (1,  0, -1, "",   PRIMARY_MIDDLE),
#     "IA": (1,  1, -1, "",   SECONDARY_ACTIVE),
#     "IM": (1,  1, -1, "",   SECONDARY_MIDDLE),
#     "FA": (2,  0, -1, "",   PRIMARY_ACTIVE),
#     "FM": (2,  0, -1, "",   PRIMARY_MIDDLE),
#     "FP": (6, -1, -2, "ησ", PRIMARY_MIDDLE),
# }
#
#
# def get_forms(verb, tv):
#     e = d1[tv]
#     part = verb["principal-parts"].split(", ")[e[0] - 1]
#     if part == "---":
#         return None
#     stem = remove(part[:e[2]] + e[3])
#     if e[1] == 0:
#         pass
#     elif e[1] == 1:
#         # add augment
#         if stem[0] in "δθλμπ":
#             stem = "ἐ" + stem
#         elif stem[0] == "ἀ":
#             stem = "ἠ" + stem
#         else:
#             raise Exception(stem[0])
#     elif e[1] == -1:
#         # remove augment
#         if stem[0] == "ἠ":
#             stem = "ἀ" + stem[1:]
#         elif stem[0] == "ἐ":
#             stem = stem[1:]
#         else:
#             raise Exception(stem[0])
#
#     return [
#         (ending, "/".join(
#             recessive(stem + f)
#             for f in e[4][ending].split("/")
#         ))
#         for ending in ["1S", "2S", "3S", "1P", "2P", "3P"]
#     ]
#
#
# d2 = {
#     "PA": (1,  0, -1, "",   "ειν"),
#     "PM": (1,  0, -1, "",   "εσθαι"),
#     "FA": (2,  0, -1, "",   "ειν"),
#     "FM": (2,  0, -1, "",   "εσθαι"),
#     "FP": (6, -1, -2, "ησ", "εσθαι"),
# }
#
#
# def get_infinitive(verb, tv):
#     e = d2[tv]
#     part = verb["principal-parts"].split(", ")[e[0] - 1]
#     if part == "---":
#         return None
#     infinitives = []
#     for alt in part.split("/"):
#         stem = remove(alt[:e[2]] + e[3])
#         if e[1] == 0:
#             pass
#         elif e[1] == 1:
#             # add augment
#             if stem[0] in "δθλμπ":
#                 stem = "ἐ" + stem
#             elif stem[0] == "ἀ":
#                 stem = "ἠ" + stem
#             else:
#                 raise Exception(stem[0])
#         elif e[1] == -1:
#             # remove augment
#             if stem[0] == "ἠ":
#                 stem = "ἀ" + stem[1:]
#             elif stem[0] == "ἐ":
#                 stem = stem[1:]
#             else:
#                 raise Exception(stem[0])
#         infinitives.append(recessive(stem + e[4]))
#     return "/".join(infinitives)

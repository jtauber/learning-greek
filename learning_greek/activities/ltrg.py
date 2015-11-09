# coding: utf-8

import random

from pinax.lms.activities.base import ShortAnswerQuiz, MultipleShortAnswerQuiz

from .utils import remove, verbs, nouns, adjectives, others, articles, demonstratives1, demonstratives2
from accentuation import recessive


def get_verbs(part):
    for verb in verbs:
        for v in verb["principal-parts"].split(", ")[part - 1].split("/"):
            stem = remove(v)[:-1]
            yield stem + "ω"
            yield stem + "εις"
            yield stem + "ει"
            yield stem + "ομεν"
            yield stem + "ετε"
            yield stem + "ουσιν"
            yield stem + "ουσι"


def non_verbs():
    for noun in nouns:
        n = noun["citation-form"].split(", ")[0]
        yield n

    for adjective in adjectives:
        a = adjective["citation-form"].split(", ")[0]
        yield a

    for other in others:
        for o in other["citation-form"].split(", ")[0].split("/"):
            yield o


class RecessiveVerbAccentQuiz(ShortAnswerQuiz):

    title = "Recessive Verb Accent Quiz"
    description = "given an unaccented, inflected verb, place the recessive accent"

    repeatable = True

    def construct_quiz(self):

        questions = []

        for verb in random.sample(set(get_verbs(1)), 10):
            questions.append((verb, recessive(verb)))

        return questions


class PersistentAccentQuiz(ShortAnswerQuiz):

    title = "Persistent Accent Quiz"
    description = "given an unaccented non-verb citation form, place the accent correctly"

    repeatable = True

    def construct_quiz(self):

        questions = []

        for word in random.sample(set(non_verbs()), 10):
            questions.append((remove(word), word))

        return questions


class DeclineArticleQuiz(MultipleShortAnswerQuiz):

    title = "Decline Article Quiz"
    description = "given a gender, decline the definite article"

    repeatable = True

    def construct_quiz(self):

        ARTICLE = {}
        for article in articles:
            ARTICLE[article["cng"]] = article["form"]

        gender = random.choice([("masculine", "M"), ("feminine", "F"), ("neuter", "N")])

        questions = [(
            gender[0], [(cn[0], ARTICLE[cn[1] + gender[1]]) for cn in [
                ("nominative singular", "NS"),
                ("genitive singular", "GS"),
                ("dative singular", "DS"),
                ("accusative singular", "AS"),
                ("nominative plural", "NP"),
                ("genitive plural", "GP"),
                ("dative plural", "DP"),
                ("accusative plural", "AP"),
            ]]
        )]

        return questions


class DeclineDemonstrative1Quiz(MultipleShortAnswerQuiz):

    title = "Decline οὗτος Quiz"
    description = "given a gender, decline the demonstrative οὗτος"

    repeatable = True

    def construct_quiz(self):

        DEMONSTRATIVE = {}
        for demonstrative in demonstratives1:
            DEMONSTRATIVE[demonstrative["cng"]] = demonstrative["form"]

        gender = random.choice([("masculine", "M"), ("feminine", "F"), ("neuter", "N")])

        questions = [(
            gender[0], [(cn[0], DEMONSTRATIVE[cn[1] + gender[1]]) for cn in [
                ("nominative singular", "NS"),
                ("genitive singular", "GS"),
                ("dative singular", "DS"),
                ("accusative singular", "AS"),
                ("nominative plural", "NP"),
                ("genitive plural", "GP"),
                ("dative plural", "DP"),
                ("accusative plural", "AP"),
            ]]
        )]

        return questions


class DeclineDemonstrative2Quiz(MultipleShortAnswerQuiz):

    title = "Decline ὅδε Quiz"
    description = "given a gender, decline the demonstrative ὅδε"

    repeatable = True

    def construct_quiz(self):

        DEMONSTRATIVE = {}
        for demonstrative in demonstratives2:
            DEMONSTRATIVE[demonstrative["cng"]] = demonstrative["form"]

        gender = random.choice([("masculine", "M"), ("feminine", "F"), ("neuter", "N")])

        questions = [(
            gender[0], [(cn[0], DEMONSTRATIVE[cn[1] + gender[1]]) for cn in [
                ("nominative singular", "NS"),
                ("genitive singular", "GS"),
                ("dative singular", "DS"),
                ("accusative singular", "AS"),
                ("nominative plural", "NP"),
                ("genitive plural", "GP"),
                ("dative plural", "DP"),
                ("accusative plural", "AP"),
            ]]
        )]

        return questions


class DeclineNounQuiz(MultipleShortAnswerQuiz):

    repeatable = True

    def construct_quiz(self):

        questions = [(
            self.CITATION_FORM, [(cn[0], self.PARADIGM[cn[1] + self.GENDER]) for cn in [
                ("nominative singular", "NS"),
                ("genitive singular", "GS"),
                ("dative singular", "DS"),
                ("accusative singular", "AS"),
                ("nominative plural", "NP"),
                ("genitive plural", "GP"),
                ("dative plural", "DP"),
                ("accusative plural", "AP"),
            ]]
        )]

        return questions


class DeclineNoun1aQuiz(DeclineNounQuiz):

    title = "Decline ᾱ, ᾱς Noun Quiz"
    description = "given a ᾱ, ᾱς noun, decline it"

    CITATION_FORM = "οἰκίᾱ, ᾱς, ἡ"
    GENDER = "F"
    PARADIGM = {
        "NSF": "οἰκίᾱ",
        "GSF": "οἰκίᾱς",
        "DSF": "οἰκίᾳ",
        "ASF": "οἰκίᾱν",
        "NPF": "οἰκίαι",
        "GPF": "οἰκιῶν",
        "DPF": "οἰκίαις",
        "APF": "οἰκίᾱς",
    }


class DeclineNoun1bQuiz(DeclineNounQuiz):

    title = "Decline η, ης Noun Quiz"
    description = "given a η, ης noun, decline it"

    CITATION_FORM = "δίκη, ης, ἡ"
    GENDER = "F"
    PARADIGM = {
        "NSF": "δίκη",
        "GSF": "δίκης",
        "DSF": "δίκῃ",
        "ASF": "δίκην",
        "NPF": "δίκαι",
        "GPF": "δικῶν",
        "DPF": "δίκαις",
        "APF": "δίκᾱς",
    }


class DeclineNoun1cQuiz(DeclineNounQuiz):

    title = "Decline α, ᾱς Noun Quiz"
    description = "given a α, ᾱς noun, decline it"

    CITATION_FORM = "μοῖρα, μοίρᾱς, ἡ"
    GENDER = "F"
    PARADIGM = {
        "NSF": "μοῖρα",
        "GSF": "μοίρᾱς",
        "DSF": "μοίρᾳ",
        "ASF": "μοῖραν",
        "NPF": "μοῖραι",
        "GPF": "μοιρῶν",
        "DPF": "μοίραις",
        "APF": "μοίρᾱς",
    }


class DeclineNoun1dQuiz(DeclineNounQuiz):

    title = "Decline α, ης Noun Quiz"
    description = "given a α, ης noun, decline it"

    CITATION_FORM = "δόξα, δόξης, ἡ"
    GENDER = "F"
    PARADIGM = {
        "NSF": "δόξα",
        "GSF": "δόξης",
        "DSF": "δόξῃ",
        "ASF": "δόξαν",
        "NPF": "δόξαι",
        "GPF": "δοξῶν",
        "DPF": "δόξαις",
        "APF": "δόξᾱς",
    }


class DeclineNoun1eQuiz(DeclineNounQuiz):

    title = "Decline ᾱς, ου Noun Quiz"
    description = "given a ᾱς, ου noun, decline it"

    CITATION_FORM = "νεᾱνίᾱς, νεᾱνίου, ὁ"
    GENDER = "M"
    PARADIGM = {
        "NSM": "νεᾱνίᾱς",
        "GSM": "νεᾱνίου",
        "DSM": "νεᾱνίᾳ",
        "ASM": "νεᾱνίᾱν",
        "NPM": "νεᾱνίαι",
        "GPM": "νεᾱνιῶν",
        "DPM": "νεᾱνίαις",
        "APM": "νεᾱνίᾱς",
    }


class DeclineNoun1fQuiz(DeclineNounQuiz):

    title = "Decline ης, ου Noun Quiz"
    description = "given a ης, ου noun, decline it"

    CITATION_FORM = "πολίτης, πολίτου, ὁ"
    GENDER = "M"
    PARADIGM = {
        "NSM": "πολίτης",
        "GSM": "πολίτου",
        "DSM": "πολίτῃ",
        "ASM": "πολίτην",
        "NPM": "πολῖται",
        "GPM": "πολιτῶν",
        "DPM": "πολίταις",
        "APM": "πολίτᾱς",
    }


class DeclineNoun2aQuiz(DeclineNounQuiz):

    title = "Decline ος, ου Noun Quiz"
    description = "given a ος, ου noun, decline it"

    CITATION_FORM = "νόμος, ου, ὁ"
    GENDER = "M"
    PARADIGM = {
        "NSM": "νόμος",
        "GSM": "νόμου",
        "DSM": "νόμῳ",
        "ASM": "νόμον",
        "NPM": "νόμοι",
        "GPM": "νόμων",
        "DPM": "νόμοις",
        "APM": "νόμους",
    }


class DeclineNoun2bQuiz(DeclineNounQuiz):

    title = "Decline ον, ου Noun Quiz"
    description = "given a ον, ου noun, decline it"

    CITATION_FORM = "τέκνον, ου, τό"
    GENDER = "N"
    PARADIGM = {
        "NSN": "τέκνον",
        "GSN": "τέκνου",
        "DSN": "τέκνῳ",
        "ASN": "τέκνον",
        "NPN": "τέκνα",
        "GPN": "τέκνων",
        "DPN": "τέκνοις",
        "APN": "τέκνα",
    }


class DeclineAdjective12Quiz(ShortAnswerQuiz):

    title = "Form First-Second-Declension Adjective Quiz"
    description = "given an adjective and a case, number, gender, give the inflected form"

    repeatable = True

    def construct_quiz(self):

        ADJECTIVES = [
            {
                "NSM": "καλός",
                "GSM": "καλοῦ",
                "DSM": "καλῷ",
                "ASM": "καλόν",
                "VSM": "καλέ",
                "NSF": "καλή",
                "GSF": "καλῆς",
                "DSF": "καλῇ",
                "ASF": "καλήν",
                "VSF": "καλή",
                "NSN": "καλόν",
                "GSN": "καλοῦ",
                "DSN": "καλῷ",
                "ASN": "καλόν",
                "VSN": "καλόν",
                "NPM": "καλοί",
                "GPM": "καλῶν",
                "DPM": "καλοῖς",
                "APM": "καλούς",
                "VPM": "καλοί",
                "NPF": "καλαί",
                "GPF": "καλῶν",
                "DPF": "καλαῖς",
                "APF": "καλάς",
                "VPF": "καλαί",
                "NPN": "καλά",
                "GPN": "καλῶν",
                "DPN": "καλοῖς",
                "APN": "καλά",
                "VPN": "καλά",
            },
            {
                "NSM": "ἄδικος",
                "GSM": "ἀδίκου",
                "DSM": "ἀδίκῳ",
                "ASM": "ἄδικον",
                "VSM": "ἄδικε",
                "NSF": "ἄδικος",
                "GSF": "ἀδίκου",
                "DSF": "ἀδίκῳ",
                "ASF": "ἄδικον",
                "VSF": "ἄδικε",
                "NSN": "ἄδικον",
                "GSN": "ἀδίκου",
                "DSN": "ἀδίκῳ",
                "ASN": "ἄδικον",
                "VSN": "ἄδικον",
                "NPM": "ἄδικοι",
                "GPM": "ἀδίκων",
                "DPM": "ἀδίκοις",
                "APM": "ἀδίκους",
                "VPM": "ἄδικοι",
                "NPF": "ἄδικοι",
                "GPF": "ἀδίκων",
                "DPF": "ἀδίκοις",
                "APF": "ἀδίκους",
                "VPF": "ἄδικοι",
                "NPN": "ἄδικα",
                "GPN": "ἀδίκων",
                "DPN": "ἀδίκοις",
                "APN": "ἄδικα",
                "VPN": "ἄδικα",
            },
            {
                "NSM": "Ἀθηναῖος",
                "GSM": "Ἀθηναίου",
                "DSM": "Ἀθηναίῳ",
                "ASM": "Ἀθηναῖον",
                "VSM": "Ἀθηναῖε",
                "NSF": "Ἀθηναίᾱ",
                "GSF": "Ἀθηναίᾱς",
                "DSF": "Ἀθηναίᾳ",
                "ASF": "Ἀθηναίᾱν",
                "VSF": "Ἀθηναίᾱ",
                "NSN": "Ἀθηναῖον",
                "GSN": "Ἀθηναίου",
                "DSN": "Ἀθηναίῳ",
                "ASN": "Ἀθηναῖον",
                "VSN": "Ἀθηναῖον",
                "NPM": "Ἀθηναῖοι",
                "GPM": "Ἀθηναίων",
                "DPM": "Ἀθηναίοις",
                "APM": "Ἀθηναίους",
                "VPM": "Ἀθηναῖοι",
                "NPF": "Ἀθηναῖαι",
                "GPF": "Ἀθηναίων",
                "DPF": "Ἀθηναίαις",
                "APF": "Ἀθηναίᾱς",
                "VPF": "Ἀθηναῖαι",
                "NPN": "Ἀθηναῖα",
                "GPN": "Ἀθηναίων",
                "DPN": "Ἀθηναίοις",
                "APN": "Ἀθηναῖα",
                "VPN": "Ἀθηναῖα",
            },
        ]

        # @@@ avoid consecutive duplicates

        cases = {"N": "nominative", "G": "genitive", "D": "dative", "A": "accusative", "V": "vocative"}
        numbers = {"S": "singular", "P": "plural"}
        genders = {"M": "masculine", "F": "feminine", "N": "neuter"}

        questions = []
        for i in range(10):
            adjective = random.choice(ADJECTIVES)
            parse = random.choice(adjective.keys())
            question = "{} {} {} of {}".format(cases[parse[0]], numbers[parse[1]], genders[parse[2]], adjective["NSM"])
            answer = adjective[parse]
            questions.append((question, answer))

        return questions


class VerbEndings(MultipleShortAnswerQuiz):

    repeatable = True

    def construct_quiz(self):

        questions = [(
            "enter endings", [(pn[0], self.PARADIGM[pn[1]]) for pn in [
                ("1st person singular", "1S"),
                ("2nd person singular", "2S"),
                ("3rd person singular", "3S"),
                ("1st person plural", "1P"),
                ("2nd person plural", "2P"),
                ("3rd person plural", "3P"),
            ]]
        )]

        return questions


class OmegaVerbsPrimaryActiveEndings(VerbEndings):

    title = "primary active endings of omega verbs"
    description = "primary active endings of omega verbs"

    PARADIGM = {
        "1S": "ω",
        "2S": "εις",
        "3S": "ει",
        "1P": "ομεν",
        "2P": "ετε",
        "3P": "ουσι(ν)",
    }


class OmegaVerbsPrimaryMiddlePassiveEndings(VerbEndings):

    title = "primary middle/passive endings of omega verbs"
    description = "primary middle/passive endings of omega verbs"

    ENDING_SET_NAME = "primary middle/passive endings of omega verbs"
    PARADIGM = {
        "1S": "ομαι",
        "2S": "ῃ ει",
        "3S": "εται",
        "1P": "ομεθα",
        "2P": "εσθε",
        "3P": "ονται",
    }


class OmegaVerbsSecondaryActiveEndings(VerbEndings):

    title = "secondary active endings of omega verbs"
    description = "secondary active endings of omega verbs"

    ENDING_SET_NAME = "secondary active endings of omega verbs"
    PARADIGM = {
        "1S": "ον",
        "2S": "ες",
        "3S": "ε(ν)",
        "1P": "ομεν",
        "2P": "ετε",
        "3P": "ον",
    }


class OmegaVerbsSecondaryMiddlePassiveEndings(VerbEndings):

    title = "secondary middle/passive endings of omega verbs"
    description = "secondary middle/passive endings of omega verbs"

    ENDING_SET_NAME = "secondary middle/passive endings of omega verbs"
    PARADIGM = {
        "1S": "ομην",
        "2S": "ου",
        "3S": "ετο",
        "1P": "ομεθα",
        "2P": "εσθε",
        "3P": "οντο",
    }


class FirstAoristActiveEndings(VerbEndings):

    title = "first aorist active endings"
    description = "first aorist active endings"

    PARADIGM = {
        "1S": "α",
        "2S": "ας",
        "3S": "ε(ν)",
        "1P": "αμεν",
        "2P": "ατε",
        "3P": "αν",
    }


class FirstAoristMiddleEndings(VerbEndings):

    title = "first aorist middle endings"
    description = "first aorist middle endings"

    PARADIGM = {
        "1S": "αμην",
        "2S": "ω",
        "3S": "ατο",
        "1P": "αμεθα",
        "2P": "ασθε",
        "3P": "αντο",
    }


class FirstAoristPassiveEndings(VerbEndings):

    title = "first aorist passive endings"
    description = "first aorist middle endings"

    PARADIGM = {
        "1S": "ην",
        "2S": "ης",
        "3S": "η",
        "1P": "ημεν",
        "2P": "ητε",
        "3P": "ησαν",
    }


class VerbInflection(ShortAnswerQuiz):

    repeatable = True

    def construct_quiz(self):

        # @@@ avoid consecutive duplicates

        tenses = {"P": "present", "I": "imperfect", "F": "future"}
        voices = {"A": "active", "M": "middle", "P": "passive"}
        mood = {"I": "indicative", "N": "infinitive"}
        persons = {"1": "1st person", "2": "2nd person", "3": "3rd person"}
        numbers = {"S": "singular", "P": "plural"}

        questions = []
        for i in range(5):
            parse = random.choice(self.VERB_FORMS.keys())
            if parse[2] == "N":
                question = "{} {} {} of {}".format(tenses[parse[0]], voices[parse[1]], mood[parse[2]], self.VERB_FORMS["PAI.1S"])
            else:
                question = "{} {} {} {} {} of {}".format(tenses[parse[0]], voices[parse[1]], mood[parse[2]], persons[parse[4]], numbers[parse[5]], self.VERB_FORMS["PAI.1S"])
            answer = self.VERB_FORMS[parse]
            questions.append((question, answer))

        return questions


class Chapter3VerbInflection(VerbInflection):

    title = "Chapter 3 Verb Inflection"
    description = "give the present, imperfect and future inflected forms from chapter 3"

    VERB_FORMS = {
        "PAI.1S": "παύω",
        "PAI.2S": "παύεις",
        "PAI.3S": "παύει",
        "PAI.1P": "παύομεν",
        "PAI.2P": "παύετε",
        "PAI.3P": "παύουσι(ν)",
        "PMI.1S": "παύομαι",
        "PMI.2S": "παύῃ παύει",
        "PMI.3S": "παύεται",
        "PMI.1P": "παυόμεθα",
        "PMI.2P": "παύεσθε",
        "PMI.3P": "παύονται",
        "PPI.1S": "παύομαι",
        "PPI.2S": "παύῃ παύει",
        "PPI.3S": "παύεται",
        "PPI.1P": "παυόμεθα",
        "PPI.2P": "παύεσθε",
        "PPI.3P": "παύονται",
        "IAI.1S": "ἔπαυον",
        "IAI.2S": "ἔπαυες",
        "IAI.3S": "ἔπαυε(ν)",
        "IAI.1P": "ἐπαύομεν",
        "IAI.2P": "ἐπαύετε",
        "IAI.3P": "ἔπαυον",
        "IMI.1S": "ἐπαυόμην",
        "IMI.2S": "ἐπαύου",
        "IMI.3S": "ἐπαύετο",
        "IMI.1P": "ἐπαυόμεθα",
        "IMI.2P": "ἐπαύεσθε",
        "IMI.3P": "ἐπαύοντο",
        "IPI.1S": "ἐπαυόμην",
        "IPI.2S": "ἐπαύου",
        "IPI.3S": "ἐπαύετο",
        "IPI.1P": "ἐπαυόμεθα",
        "IPI.2P": "ἐπαύεσθε",
        "IPI.3P": "ἐπαύοντο",
        "PAN": "παύειν",
        "PMN": "παύεσθαι",
        "PPN": "παύεσθαι",
        "FAI.1S": "παύσω",
        "FAI.2S": "παύσεις",
        "FAI.3S": "παύσει",
        "FAI.1P": "παύσομεν",
        "FAI.2P": "παύσετε",
        "FAI.3P": "παύσουσι(ν)",
        "FMI.1S": "παύσομαι",
        "FMI.2S": "παύσῃ παύσει",
        "FMI.3S": "παύσεται",
        "FMI.1P": "παυσόμεθα",
        "FMI.2P": "παύσεσθε",
        "FMI.3P": "παύσονται",
        "FAN": "παύσειν",
        "FMN": "παύσεσθαι",
        "FPI.1S": "παυθήσομαι",
        "FPI.2S": "παυθήσῃ παυθήσει",
        "FPI.3S": "παυθήσεται",
        "FPI.1P": "παυθησόμεθα",
        "FPI.2P": "παυθήσεσθε",
        "FPI.3P": "παυθήσονται",
        "FPN": "παυθήσεσθαι",
    }


class Chapter4EpsilonContractedVerbInflection(VerbInflection):

    title = "Chapter 4 Epsilon-Contracted Verb Inflection"
    description = "give the present, imperfect and future epsilon-contracted inflected forms from chapter 4"

    VERB_FORMS = {
        "PAI.1S": "ποιῶ",
        "PAI.2S": "ποιεῖς",
        "PAI.3S": "ποιεῖ",
        "PAI.1P": "ποιοῦμεν",
        "PAI.2P": "ποιεῖτε",
        "PAI.3P": "ποιοῦσι(ν)",
        "PMI.1S": "ποιοῦμαι",
        "PMI.2S": "ποιῇ ποιεῖ",
        "PMI.3S": "ποιεῖται",
        "PMI.1P": "ποιούμεθα",
        "PMI.2P": "ποιεῖσθε",
        "PMI.3P": "ποιοῦνται",
        "PPI.1S": "ποιοῦμαι",
        "PPI.2S": "ποιῇ ποιεῖ",
        "PPI.3S": "ποιεῖται",
        "PPI.1P": "ποιούμεθα",
        "PPI.2P": "ποιεῖσθε",
        "PPI.3P": "ποιοῦνται",
        "IAI.1S": "ἐποίουν",
        "IAI.2S": "ἐποίεις",
        "IAI.3S": "ἐποίει",
        "IAI.1P": "ἐποιοῦμεν",
        "IAI.2P": "ἐποιεῖτε",
        "IAI.3P": "ἐποίουν",
        "IMI.1S": "ἐποιούμην",
        "IMI.2S": "ἐποιοῦ",
        "IMI.3S": "ἐποιεῖτο",
        "IMI.1P": "ἐποιούμεθα",
        "IMI.2P": "ἐποιεῖσθε",
        "IMI.3P": "ἐποιοῦντο",
        "IPI.1S": "ἐποιούμην",
        "IPI.2S": "ἐποιοῦ",
        "IPI.3S": "ἐποιεῖτο",
        "IPI.1P": "ἐποιούμεθα",
        "IPI.2P": "ἐποιεῖσθε",
        "IPI.3P": "ἐποιοῦντο",
        "PAN": "ποιεῖν",
        "PMN": "ποιεῖσθαι",
        "PPN": "ποιεῖσθαι",
    }


class Chapter4AlphaContractedVerbInflection(VerbInflection):

    title = "Chapter 4 Alpha-Contracted Verb Inflection"
    description = "give the present, imperfect and future alpha-contracted inflected forms from chapter 4"

    VERB_FORMS = {
        "PAI.1S": "νικῶ",
        "PAI.2S": "νικᾷς",
        "PAI.3S": "νικᾷ",
        "PAI.1P": "νικῶμεν",
        "PAI.2P": "νικᾶτε",
        "PAI.3P": "νικῶσι(ν)",
        "PMI.1S": "νικῶμαι",
        "PMI.2S": "νικᾷ",
        "PMI.3S": "νικᾶται",
        "PMI.1P": "νικώμεθα",
        "PMI.2P": "νικᾶσθε",
        "PMI.3P": "νικῶνται",
        "PPI.1S": "νικῶμαι",
        "PPI.2S": "νικᾷ",
        "PPI.3S": "νικᾶται",
        "PPI.1P": "νικώμεθα",
        "PPI.2P": "νικᾶσθε",
        "PPI.3P": "νικῶνται",
        "IAI.1S": "ἐνίκων",
        "IAI.2S": "ἐνίκᾱς",
        "IAI.3S": "ἐνίκᾱ",
        "IAI.1P": "ἐνικῶμεν",
        "IAI.2P": "ἐνικᾶτε",
        "IAI.3P": "ἐνίκων",
        "IMI.1S": "ἐνικώμην",
        "IMI.2S": "ἐνικῶ",
        "IMI.3S": "ἐνικᾶτο",
        "IMI.1P": "ἐνικώμεθα",
        "IMI.2P": "ἐνικᾶσθε",
        "IMI.3P": "ἐνικῶντο",
        "IPI.1S": "ἐνικώμην",
        "IPI.2S": "ἐνικῶ",
        "IPI.3S": "ἐνικᾶτο",
        "IPI.1P": "ἐνικώμεθα",
        "IPI.2P": "ἐνικᾶσθε",
        "IPI.3P": "ἐνικῶντο",
        "PAN": "νικᾶν",
        "PMN": "νικᾶσθαι",
        "PPN": "νικᾶσθαι",
    }


class Chapter4OmicronContractedVerbInflection(VerbInflection):

    title = "Chapter 4 Omicron-Contracted Verb Inflection"
    description = "give the present, imperfect and future omicron-contracted inflected forms from chapter 4"

    VERB_FORMS = {
        "PAI.1S": "δηλῶ",
        "PAI.2S": "δηλοῖς",
        "PAI.3S": "δηλοῖ",
        "PAI.1P": "δηλοῦμεν",
        "PAI.2P": "δηλοῦτε",
        "PAI.3P": "δηλοῦσι(ν)",
        "PMI.1S": "δηλοῦμαι",
        "PMI.2S": "δηλοῖ",
        "PMI.3S": "δηλοῦται",
        "PMI.1P": "δηλούμεθα",
        "PMI.2P": "δηλοῦσθε",
        "PMI.3P": "δηλοῦνται",
        "PPI.1S": "δηλοῦμαι",
        "PPI.2S": "δηλοῖ",
        "PPI.3S": "δηλοῦται",
        "PPI.1P": "δηλούμεθα",
        "PPI.2P": "δηλοῦσθε",
        "PPI.3P": "δηλοῦνται",
        "IAI.1S": "ἐδήλουν",
        "IAI.2S": "ἐδήλους",
        "IAI.3S": "ἐδήλου",
        "IAI.1P": "ἐδηλοῦμεν",
        "IAI.2P": "ἐδηλοῦτε",
        "IAI.3P": "ἐδήλουν",
        "IMI.1S": "ἐδηλούμην",
        "IMI.2S": "ἐδηλοῦ",
        "IMI.3S": "ἐδηλοῦτο",
        "IMI.1P": "ἐδηλούμεθα",
        "IMI.2P": "ἐδηλοῦσθε",
        "IMI.3P": "ἐδηλοῦντο",
        "IPI.1S": "ἐδηλούμην",
        "IPI.2S": "ἐδηλοῦ",
        "IPI.3S": "ἐδηλοῦτο",
        "IPI.1P": "ἐδηλούμεθα",
        "IPI.2P": "ἐδηλοῦσθε",
        "IPI.3P": "ἐδηλοῦντο",
        "PAN": "δηλοῦν",
        "PMN": "δηλοῦσθαι",
        "PPN": "δηλοῦσθαι",
    }

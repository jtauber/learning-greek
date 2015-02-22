# coding: utf-8

import random

from pinax.lms.activities.base import ShortAnswerQuiz, MultipleShortAnswerQuiz

from .utils import remove, verbs, nouns, adjectives, others, articles, demonstratives1
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

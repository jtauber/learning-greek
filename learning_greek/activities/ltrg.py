# coding: utf-8

import random

from pinax.lms.activities.base import ShortAnswerQuiz

from .utils import remove, verbs
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


class RecessiveVerbAccentQuiz(ShortAnswerQuiz):

    title = "Recessive Verb Accent Quiz"
    description = "given an unaccented, inflected verb, place the recessive accent"

    repeatable = True

    def construct_quiz(self):

        questions = []

        for verb in random.sample(set(get_verbs(1)), 10):
            questions.append((verb, recessive(verb)))

        return questions

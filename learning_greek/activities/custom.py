# coding: utf-8

import random

from django import forms

from .base import Survey, MultiPageSurvey, TwoChoiceQuiz


class DemographicSurvey(Survey):

    title = "Demographic Survey"
    description = "basic demographic questions"

    questions = [
        {
            "name": "birthyear",
            "label": "Year of Birth",
            "help_text": "what year were you born in?",
            "field_class": forms.CharField,
        },
        {
            "name": "gender",
            "label": "Gender",
            "field_class": forms.ChoiceField,
            "extra_args": {
                "choices": [("", ""), ("M", "Male"), ("F", "Female")]
            }
        }
    ]


class DemographicSurvey2(MultiPageSurvey):

    title = "Demographic Survey"
    description = "basic demographic questions (over two pages)"

    pages = [
        [
            {
                "name": "birthyear",
                "label": "Year of Birth",
                "help_text": "what year were you born in?",
                "field_class": forms.CharField,
            }
        ],
        [
            {
                "name": "gender",
                "label": "Gender",
                "field_class": forms.ChoiceField,
                "extra_args": {
                    "choices": [("", ""), ("M", "Male"), ("F", "Female")]
                }
            }
        ]
    ]


class UpperCaseQuiz(TwoChoiceQuiz):
    
    title = "Upper Case"
    description = "given a lower-case letter, what's the upper-case equivalent"
    
    def construct_quiz(self):
        questions = []
        letters = u"αβγδεζηθικλμνξοπρστυφχψω"
        for i in range(10):
            choices = random.sample(letters, 2)
            question = random.choice(choices)
            questions.append((question, [choice.upper() for choice in choices]))
        return questions


class LowerCaseQuiz(TwoChoiceQuiz):
    
    title = "Lower Case"
    description = "given an upper-case letter, what's the lower-case equivalent"
    
    def construct_quiz(self):
        questions = []
        letters = u"αβγδεζηθικλμνξοπρστυφχψω"
        for i in range(10):
            choices = random.sample(letters, 2)
            question = random.choice(choices).upper()
            questions.append((question, choices))
        return questions

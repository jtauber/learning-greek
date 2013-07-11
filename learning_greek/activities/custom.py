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


SPOKEN_LANGUAGES_HELP_TEXT = """

<p>Use the following standard definitions to assess your proficiency at any languages you speak.</p>

<table class="table table-striped">
  <tr>
    <th>Level</th><th>Speaking</th><th>Reading</th>
  </tr>
  <tr>
    <td>Elementary</td>
    <td>Able to satisfy routine travel needs and minimum courtesy requirements</td>
    <td>Able to read some personal and place names, street signs, office and shop designations, numbers and isolated words and phrases</td>
  </tr>
  <tr>
    <td nowrap>Limited Working</td>
    <td>Able to satisfy routine social demands and limited work requirements</td>
    <td>Able to read simple prose, in a form equivalent to typescript or printing, on subjects within a familiar context</td>
  </tr>
  <tr>
    <td nowrap>Minimum Professional</td>
    <td>Able to speak the language with sufficient structural accuracy and vocabulary to participate effectively in most formal and informal conversations on practical, social, and professional topics</td>
    <td>Able to read standard newspaper items addressed to the general reader, routine correspondence, reports, and technical materials in the individual's special field.</td>
  </tr>
  <tr>
    <td nowrap>Full Professional</td>
    <td>Able to use the language fluently and accurately on all levels pertinent to professional needs.</td>
    <td>Able to read all styles and forms of the language pertinent to professional needs.</td>
  </tr>
  <tr>
    <td nowrap>Native or Bilingual</td>
    <td>Equivalent to that of an educated native speaker.</td>
    <td>Equivalent to that of an educated native.</td>
  </tr>
</table>
"""


class SpokenLanguagesSurvey(Survey):
    
    title = "Spoken Languages You Know"
    description = "spoken languages you know and your proficiency at them"
    
    help_text = SPOKEN_LANGUAGES_HELP_TEXT
    
    questions = [
        {
            "name": "level5",
            "label": "Native or Bilingual",
            "help_text": "list languages separated by commas or leave blank if none",
            "field_class": forms.CharField,
        },
        {
            "name": "level4",
            "label": "Full Professional",
            "help_text": "list languages separated by commas or leave blank if none",
            "field_class": forms.CharField,
            "required": False,
        },
        {
            "name": "level3",
            "label": "Minimum Professional",
            "help_text": "list languages separated by commas or leave blank if none",
            "field_class": forms.CharField,
            "required": False,
        },
        {
            "name": "level2",
            "label": "Limited Working",
            "help_text": "list languages separated by commas or leave blank if none",
            "field_class": forms.CharField,
            "required": False,
        },
        {
            "name": "level1",
            "label": "Elementary",
            "help_text": "list languages separated by commas or leave blank if none",
            "field_class": forms.CharField,
            "required": False,
        }
    ]


class GoalsSurvey(Survey):

    title = "Goals for Using Site"
    description = "what your goals in using / contributing to the site are"

    questions = [
        {
            "name": "goals",
            "label": "Goals in using site",
            "help_text": "select any of the above goals you have for using and/or contributing to the site",
            "field_class": forms.MultipleChoiceField,
            "required": False,
            "extra_args": {
                "widget": forms.CheckboxSelectMultiple,
                "choices": [
                    ("1", "I want to learn enough Greek to make better use of tools such as lexicons and commentaries"),
                    ("2", "I want to be able to read the New Testament in the original language"),
                    ("2", "I want to be able to read other texts in Koine Greek"),
                    ("3", "I want to refresh the Greek I've already studied"),
                    ("3", "I teach Greek and am assessing this site for my students"),
                    ("3", "I teach Greek and want to contribute ideas and activities for this site"),
                    ("4", "I'm a developer who wants to help contribute to the code behind this site"),
                    ("4", "I'm a linguist or philologist who is interested in the data gathered by this site for research purposes"),
                    ("4", "I'm a learning scientist who is interested in the data gathered by this site for research purposes"),
                ]
            }
        }
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

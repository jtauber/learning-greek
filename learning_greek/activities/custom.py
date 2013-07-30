# coding: utf-8

import random

from django import forms

from .base import Survey, Quiz, TwoChoiceQuiz, LikertQuiz

from learning_greek.language_data.models import NounCumulativeCount, NounCaseNumberGender, DickinsonCoreList


class SuggestionBox(Survey):
    
    title = "Suggestion Box"
    description = "make a suggestion on how to improve the site"
    
    repeatable = True
    
    questions = [
        {
            "name": "suggestion",
            "label": "Suggestion",
            "field_class": forms.CharField,
            "extra_args": {
                "widget": forms.Textarea(attrs={"rows": "5", "class": "span8"}),
            }
        }
    ]


class DemographicSurvey(Survey):
    
    title = "Demographic Survey"
    description = "basic demographic questions"
    
    repeatable = False
    
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
    
    repeatable = False
    
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
    
    repeatable = False
    
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
                    ("3", "I want to be able to read other texts in Koine Greek"),
                    ("4", "I want to refresh the Greek I've already studied"),
                    ("5", "I teach Greek and am assessing this site for my students"),
                    ("6", "I teach Greek and want to contribute ideas and activities for this site"),
                    ("7", "I'm a developer who wants to help contribute to the code behind this site"),
                    ("8", "I'm a linguist or philologist who is interested in the data gathered by this site for research purposes"),
                    ("9", "I'm a learning scientist who is interested in the data gathered by this site for research purposes"),
                ]
            }
        }
    ]


class UpperCaseQuiz(TwoChoiceQuiz):
    
    title = "Upper Case"
    description = "given a lower-case letter, what's the upper-case equivalent"
    
    repeatable = True
    
    def construct_quiz(self):
        
        questions = []
        letters = u"αβγδεζηθικλμνξοπρστυφχψω"
        
        while len(questions) < 10:
            choices = random.sample(letters, 2)
            question = random.choice(choices)
            if question not in [item[0] for item in questions]:
                questions.append((question, [choice.upper() for choice in choices]))
        
        return questions


class LowerCaseQuiz(TwoChoiceQuiz):
    
    title = "Lower Case"
    description = "given an upper-case letter, what's the lower-case equivalent"
    
    repeatable = True
    
    def construct_quiz(self):
        
        questions = []
        letters = u"αβγδεζηθικλμνξοπρστυφχψω"
        
        while len(questions) < 10:
            choices = random.sample(letters, 2)
            question = random.choice(choices).upper()
            if question not in [item[0] for item in questions]:
                questions.append((question, choices))
        
        return questions


class NounFamiliarity(LikertQuiz):
    
    title = "Noun Familiarity"
    description = "do you know the meaning of the given nouns?"
    
    repeatable = True
    
    scale = [
        "I definitely don't know it",
        "I don't think I know it",
        "I'm not sure if I know it or not",
        "I think I know it",
        "I definitely know it",
    ]
    
    def construct_quiz(self):
        
        questions = []
        
        while len(questions) < 10:
            value = random.randint(1, 28239)
            noun = NounCumulativeCount.get_value(value)
            if noun not in questions:
                questions.append(noun)
        
        return questions


class DCCNounFamiliarity(LikertQuiz):
    
    title = "Noun Familiarity (DCC Core List)"
    description = "do you know the meaning of the given nouns?"
    
    repeatable = True
    
    scale = [
        "I definitely don't know it",
        "I don't think I know it",
        "I'm not sure if I know it or not",
        "I think I know it",
        "I definitely know it",
    ]
    
    def construct_quiz(self):
        
        questions = []
        
        while len(questions) < 10:
            noun = DickinsonCoreList.objects.filter(pos="noun").order_by("?")[0].lemma
            if noun not in questions:
                questions.append(noun)
        
        return questions


class LetterFamiliarity(LikertQuiz):
    
    title = "Letter Familiarity"
    description = "are you familiar with these Greek letters?"
    
    repeatable = True
    
    scale = [
        "I definitely don't know it",
        "I don't think I know it",
        "I'm not sure if I know it or not",
        "I think I know it",
        "I definitely know it",
    ]
    
    def construct_quiz(self):
        letters = u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρσςτυφχψω"
        questions = random.sample(letters, 10)
        
        return questions


class PreviousGreekKnowledge(Survey):
    
    title = "Previous Greek Knowledge"
    description = "how much have you already studied Ancient Greek (if at all)?"
    
    repeatable = False
    
    questions = [
        {
            "name": "previous_greek",
            "label": "What's the furthest you've studied Ancient Greek?",
            "field_class": forms.ChoiceField,
            "required": True,
            "extra_args": {
                "widget": forms.RadioSelect,
                "choices": [
                    ("1", "I've never studied any Ancient Greek"),
                    ("2", "I know the alphabet and a few words"),
                    ("3", "I've taught myself from a textbook or two"),
                    ("4", "I've done a semester of formal study"),
                    ("5", "I've done more than one semester of formal study"),
                    ("6", "I majored in Ancient Greek"),
                    ("7", "I did graduate study in Ancient Greek"),
                ]
            }
        }
    ]


class NounInflectionQuiz(Quiz):
    
    title = "Noun Inflection Quiz"
    description = "what is the case, number of gender of these nouns?"
    
    repeatable = True
    
    valid_answer = ["left", "right", "unknown"]
    template_name = "activities/two_choice_quiz_variant.html"
    
    def construct_quiz(self):
        questions = []
        
        while len(questions) < 10:
            noun = NounCaseNumberGender.objects.order_by("?")[0]
            lemma = noun.lemma
            question_type = random.choice(["case", "number", "gender"])
            
            if question_type == "case":
                alternatives = ["nominative", "accusative", "nominative or accusative", "genitive", "dative"]
                answer = noun.get_case_display()
            elif question_type == "number":
                alternatives = ["singular", "plural"]
                answer = noun.get_number_display()
            elif question_type == "gender":
                alternatives = ["masculine", "feminine", "neuter"]
                answer = noun.get_gender_display()
            
            alternatives.remove(answer)
            alternative = random.choice(alternatives)
            
            if (lemma, question_type) not in [(item[0], item[1]) for item in questions]:
                question = (lemma, question_type, random.sample([answer, alternative], 2))
                questions.append(question)
        
        return questions


class LowerCaseAlphabetOrderQuiz(Quiz):
    
    title = "Lower Case Alphabet Order Quiz"
    description = "what letter goes between the given two in the Greek alphabet?"
    
    repeatable = True
    
    valid_answer = ["left", "right"]
    template_name = "activities/order_quiz.html"
    
    def construct_quiz(self):
        questions = []
        letters = ["(start)"] + list(u"αβγδεζηθικλμνξοπρστυφχψω") + ["(end)"]
        
        while len(questions) < 10:
            
            n = random.randint(1, 24)
            before, answer, after = letters[n - 1: n + 2]
            other_choice = random.choice(list(set(u"αβγδεζηθικλμνξοπρστυφχψω") - set([before, answer, after])))
            left, right = random.sample([answer, other_choice], 2)
            
            if before not in [question["before"] for question in questions]:
                questions.append(dict(before=before, left=left, right=right, after=after))
        
        return questions

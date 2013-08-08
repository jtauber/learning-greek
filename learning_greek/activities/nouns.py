# coding: utf-8

import random

from oxlos.activities.base import Quiz, LikertQuiz, TwoChoiceLikertWithAnswersQuiz

from learning_greek.language_data.models import NounCumulativeCount, NounCaseNumberGender, DickinsonCoreList


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


class NounInflectionWithAnswersQuiz(TwoChoiceLikertWithAnswersQuiz):
    
    title = "Noun Inflection (with answers) Quiz"
    description = "what is the case, number of gender of these nouns?"
    
    repeatable = True
    
    question_template = "activities/_noun_inflection_question.html"
    answer_template = "activities/_noun_inflection_result_question.html"
    
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
                question = ((lemma, question_type), random.sample([answer, alternative], 2), answer)
                questions.append(question)
        
        return questions


class DCCNounGlossToGreek(TwoChoiceLikertWithAnswersQuiz):
    
    title = "Noun Gloss to Greek (DCC Core List)"
    description = "given a gloss, which is the correct Greek Noun?"
    
    repeatable = True
    
    question_template = "activities/_gloss.html"
    answer_template = "activities/_answer.html"
    
    def construct_quiz(self):
        
        questions = []
        
        while len(questions) < 10:
            noun1 = DickinsonCoreList.objects.filter(pos="noun").order_by("?")[0]
            noun2 = DickinsonCoreList.objects.filter(pos="noun").exclude(pk=noun1.pk).order_by("?")[0]
            if noun1.lemma in [question[2] for question in questions]:
                continue
            
            choices = random.sample([noun1, noun2], 2)
            question = random.choice(choices)
            questions.append((question.definition, [choice.lemma for choice in choices], question.lemma))
        
        return questions

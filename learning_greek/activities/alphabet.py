# coding: utf-8

import random

from django.shortcuts import redirect, render
from django.utils import simplejson

from oxlos.activities.base import Quiz, TwoChoiceQuiz, TwoChoiceWithAnswersQuiz, LikertQuiz


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


class UpperCaseWithAnswersQuiz(TwoChoiceWithAnswersQuiz):
    
    title = "Upper Case (with answers)"
    description = "given a lower-case letter, what's the upper-case equivalent"
    
    repeatable = True
    
    def construct_quiz(self):
        
        questions = []
        letters = u"αβγδεζηθικλμνξοπρστυφχψω"
        
        while len(questions) < 10:
            choices = random.sample(letters, 2)
            question = random.choice(choices)
            if question not in [item[0] for item in questions]:
                questions.append((question, [choice.upper() for choice in choices], question.upper()))
        
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


class GreekKeyboard(object):
    
    title = "Greek Keyboard"
    description = "learn and practice the Greek keyboard layout"
    
    repeatable = True
    
    def __init__(self, occurrence_state, activity_state):
        
        self.occurrence_state = occurrence_state
        self.activity_state = activity_state
    
    def handle_request(self, request):
        
        if not self.occurrence_state.data:
            first_time = True
        else:
            first_time = False
        
        if request.method == "POST":
            if request.is_ajax():
                l = simplejson.loads(request.POST.get("log"))
                question = l[0]
                answers = l[1:]
                self.occurrence_state.data.setdefault("answers", []).append((question, answers))
                if len(answers) == 1:
                    question_letter = question[0]
                    time_taken = (answers[-1][1] - question[1]) / 1000.
                    if time_taken <= self.occurrence_state.data.setdefault("best_times", {}).get(question_letter, time_taken):
                        self.occurrence_state.data["best_times"][question_letter] = time_taken
                    if time_taken <= self.activity_state.data.setdefault("best_times", {}).get(question_letter, time_taken):
                        self.activity_state.data["best_times"][question_letter] = time_taken
                        self.activity_state.save()
                self.occurrence_state.save()
            else:
                self.occurrence_state.mark_completed()
                
                return redirect("activity_completed", self.occurrence_state.activity_slug)
        
        return render(request, "activities/greek_keyboard.html", {
            "title": self.title,
            "description": self.description,
            "first_time": first_time,
        })
    
    def completed(self, request):
        
        results = [
            (letter, occurrence_best, self.activity_state.data.get("best_times", {}).get(letter))
            for (letter, occurrence_best) in sorted(self.occurrence_state.data.get("best_times", {}).items())
        ]
        
        return render(request, "activities/greek_keyboard_completed.html", {
            "title": self.title,
            "description": self.description,
            "results": results,
        })

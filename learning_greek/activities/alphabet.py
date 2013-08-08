# coding: utf-8

import random

from django.shortcuts import redirect, render
from django.utils import simplejson

from oxlos.activities.base import Quiz, TwoChoiceQuiz, TwoChoiceWithAnswersQuiz, LikertQuiz, TwoChoiceLikertWithAnswersQuiz


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


class KoinePronunciation(TwoChoiceLikertWithAnswersQuiz):
    
    title = "Koine Pronunciation of Letters"
    description = "how were these letters pronounced the Koine period? "
    
    repeatable = True
    
    question_template = "activities/_question.html"
    answer_template = "activities/_answer.html"
    
    def construct_quiz(self):
        
        pronunciation = [
            (u"Α", "ah"),
            (u"Β", "v"),
            (u"Γ", "gh, y, ng"),
            (u"Δ", "dh"),
            (u"Ε", u"ĕ"),
            (u"Ζ", "z"),
            (u"Η", u"ē"),
            (u"Θ", "th"),
            (u"Ι", "i, y"),
            (u"Κ", "k"),
            (u"Λ", "l"),
            (u"Μ", "m"),
            (u"Ν", "n"),
            (u"Ξ", "ks"),
            (u"Ο", "o"),
            (u"Π", "p"),
            (u"Ρ", "r"),
            (u"Σ", "s"),
            (u"Τ", "t"),
            (u"Υ", u"ü, v"),
            (u"Φ", "f"),
            (u"Χ", "x, ch"),
            (u"Ψ", "ps"),
            (u"Ω", "o"),
            (u"ΑΙ", u"ĕ"),
            (u"ΕΙ", "i"),
            (u"OI", u"ü"),
            (u"ΟΥ", "u"),
            (u"ΑΥ", "av, af"),
            (u"ΕΥ", u"ĕv, ĕf"),
            (u"ΗΥ", "ev, ef"),
            (u"Αι", u"ĕ"),
            (u"Ει", "i"),
            (u"Oι", u"ü"),
            (u"Ου", "u"),
            (u"Αυ", "av, af"),
            (u"Ευ", u"ĕv, ĕf"),
            (u"Ηυ", "ev, ef"),
            (u"ΓΓ", "ngg"),
            (u"ΓΚ", "ngk"),
            (u"ΓΧ", "ngch"),
            (u"α", "ah"),
            (u"β", "v"),
            (u"γ", "gh, y, ng"),
            (u"δ", "dh"),
            (u"ε", u"ĕ"),
            (u"ζ", "z"),
            (u"η", u"ē"),
            (u"θ", "th"),
            (u"ι", "i, y"),
            (u"κ", "k"),
            (u"λ", "l"),
            (u"μ", "m"),
            (u"ν", "n"),
            (u"ξ", "ks"),
            (u"ο", "o"),
            (u"π", "p"),
            (u"ρ", "r"),
            (u"σ", "s"),
            (u"ς", "s"),
            (u"τ", "t"),
            (u"υ", u"ü, v"),
            (u"φ", "f"),
            (u"χ", "x, ch"),
            (u"ψ", "ps"),
            (u"ω", "o"),
            (u"αι", u"ĕ"),
            (u"ει", "i"),
            (u"οι", u"ü"),
            (u"ου", "u"),
            (u"αυ", "av, af"),
            (u"ευ", u"ĕv, ĕf"),
            (u"ηυ", "ev, ef"),
            (u"γγ", "ngg"),
            (u"γκ", "ngk"),
            (u"γχ", "ngch"),
        ]
        
        questions = []
        
        while len(questions) < 10:
            letter1 = random.choice(pronunciation)
            letter2 = random.choice(pronunciation)
            if letter1[1] == letter2[1]:
                continue
            
            choices = random.sample([letter1, letter2], 2)
            question = random.choice(choices)
            
            if question[1] in [q[2] for q in questions]:
                continue
            
            questions.append((question[0], [choice[1] for choice in choices], question[1]))
        
        return questions

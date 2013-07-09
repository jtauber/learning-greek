# coding: utf-8

from django.shortcuts import redirect, render
from django.utils import timezone


from learning_greek.activities.forms import SurveyForm


class Survey(object):
    
    def __init__(self, activity_state):
        self.activity_state = activity_state
    
    def handle_request(self, request):
        if request.method == "POST":
            form = SurveyForm(request.POST, questions=self.questions)
            if form.is_valid():
                self.activity_state.state.update({"answers": form.cleaned_data})
                self.activity_state.completed = timezone.now()
                self.activity_state.save()
                return redirect("dashboard")  # @@@
        else:
            form = SurveyForm(questions=self.questions)
        return render(request, "activities/survey.html", {
            "title": self.title,
            "description": self.description,
            "form": form
        })


class MultiPageSurvey(Survey):
    
    def handle_request(self, request):
        data = self.activity_state.state
        if not data:
            data = {"page": 0}
        elif not data.get("page"):
            data["page"] = 0
        elif data["page"] == len(self.pages):
            # done
            return redirect("dashboard")  # @@@
        
        questions = self.pages[data["page"]]
        
        if request.method == "POST":
            form = SurveyForm(request.POST, questions=questions)
            if form.is_valid():
                self.activity_state.state.update({"answers_%d" % data["page"]: form.cleaned_data})
                self.activity_state.state.update({"page": data["page"] + 1})
                if data["page"] == len(self.pages):
                    self.activity_state.completed = timezone.now()
                    self.activity_state.save()
                    return redirect("dashboard")
                else:
                    self.activity_state.save()
                    return redirect("activity_play", self.activity_state.activity_slug)
        else:
            form = SurveyForm(questions=questions)
        
        return render(request, "activities/survey.html", {
            "title": self.title,
            "description": self.description,
            "page_number": data["page"] + 1,
            "num_pages": len(self.pages),
            "form": form
        })


class TwoChoiceQuiz(object):
    
    title = "Upper Case"
    description = "given a lower-case letter, what's the upper-case equivalent"
    
    def __init__(self, activity_state):
        self.activity_state = activity_state
        
        if not self.activity_state.state:
            self.activity_state.state = {"questions": self.construct_quiz()}
            self.activity_state.save()
        elif not self.activity_state.state.get("questions"):
            self.activity_state.state["questions"] = self.construct_quiz()
            self.activity_state.save()
    
    def handle_request(self, request):
        data = self.activity_state.state
        if not data:
            data = {"question_number": 0}
        elif not data.get("question_number"):
            data["question_number"] = 0
        elif data["question_number"] == len(data["questions"]):
            # done
            return redirect("dashboard")  # @@@
        
        question = data["questions"][data["question_number"]]
        
        if request.method == "POST":
            if request.POST.get("question_number") == str(data["question_number"] + 1):
                answer = request.POST.get("answer")
                if answer in ["left", "right"]:
                    self.activity_state.state.update({"answers_%d" % data["question_number"]: answer})
                    self.activity_state.state.update({"question_number": data["question_number"] + 1})
                    if data["question_number"] == len(data["questions"]):
                        self.activity_state.completed = timezone.now()
                        self.activity_state.save()
                        return redirect("dashboard")
                    else:
                        self.activity_state.save()
                        return redirect("activity_play", self.activity_state.activity_slug)
        
        return render(request, "activities/two_choice_quiz.html", {
            "title": self.title,
            "description": self.description,
            "question_number": data["question_number"] + 1,
            "num_questions": len(data["questions"]),
            "question": question,
        })
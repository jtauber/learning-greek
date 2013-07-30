# coding: utf-8

from django.shortcuts import redirect, render


from learning_greek.activities.forms import SurveyForm


class Survey(object):
    
    def __init__(self, activity_state):
        
        self.activity_state = activity_state
    
    def handle_request(self, request):
        
        if request.method == "POST":
            form = SurveyForm(request.POST, questions=self.questions)
            
            if form.is_valid():
                self.activity_state.data.update({"answers": form.cleaned_data})
                self.activity_state.mark_completed()
                
                return redirect("dashboard")  # @@@
        else:
            form = SurveyForm(questions=self.questions)
        
        return render(request, "activities/survey.html", {
            "title": self.title,
            "description": self.description,
            "help_text": getattr(self, "help_text", None),
            "form": form
        })


class MultiPageSurvey(Survey):
    
    def handle_request(self, request):
        
        data = self.activity_state.data
        
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
                self.activity_state.data.update({"answers_%d" % data["page"]: form.cleaned_data})
                self.activity_state.data.update({"page": data["page"] + 1})
                
                if data["page"] == len(self.pages):
                    self.activity_state.mark_completed()
                    
                    return redirect("dashboard")
                else:
                    self.activity_state.save()
                    
                    return redirect("activity_play", self.activity_state.activity_slug)
        else:
            form = SurveyForm(questions=questions)
        
        return render(request, "activities/survey.html", {
            "title": self.title,
            "description": self.description,
            "help_text": getattr(self, "help_text", None),
            "page_number": data["page"] + 1,
            "num_pages": len(self.pages),
            "form": form
        })


class Quiz(object):
    
    extra_context = {}
    
    def __init__(self, activity_state):
        
        self.activity_state = activity_state
        
        if not self.activity_state.data:
            self.activity_state.data = {"questions": self.construct_quiz()}
            self.activity_state.save()
        elif not self.activity_state.data.get("questions"):
            self.activity_state.data["questions"] = self.construct_quiz()
            self.activity_state.save()
    
    def handle_request(self, request):
        
        data = self.activity_state.data
        
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
                
                if answer in self.valid_answer:
                    self.activity_state.data.update({"answer_%d" % data["question_number"]: answer})
                    self.activity_state.data.update({"question_number": data["question_number"] + 1})
                    
                    if data["question_number"] == len(data["questions"]):
                        self.activity_state.mark_completed()
                        
                        return redirect("dashboard")
                    else:
                        self.activity_state.save()
                        
                        return redirect("activity_play", self.activity_state.activity_slug)
        
        ctx = {
            "title": self.title,
            "description": self.description,
            "help_text": getattr(self, "help_text", None),
            "question_number": data["question_number"] + 1,
            "num_questions": len(data["questions"]),
            "question": question,
        }
        ctx.update(self.extra_context)
        
        return render(request, self.template_name, ctx)


class TwoChoiceQuiz(Quiz):
    
    template_name = "activities/two_choice_quiz.html"
    valid_answer = ["left", "right"]


class LikertQuiz(Quiz):
    
    template_name = "activities/likert_quiz.html"
    valid_answer = ["1", "2", "3", "4", "5"]
    
    @property
    def extra_context(self):
        return {"scale": self.scale}

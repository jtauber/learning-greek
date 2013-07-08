from django import forms
from django.shortcuts import redirect, render
from django.utils import timezone


from learning_greek.forms import SurveyForm


class DemographicSurvey(object):

    title = "Demographic Survey"
    description = "basic demographic questions"

    def __init__(self, activity_state):
        self.questions = [
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
        return render(request, "survey.html", {
            "title": self.title,
            "description": self.description,
            "form": form
        })


class DemographicSurvey2(object):

    title = "Demographic Survey"
    description = "basic demographic questions (over two pages)"

    def __init__(self, activity_state):
        self.pages = [
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
        self.activity_state = activity_state
    
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
        
        return render(request, "survey.html", {
            "title": self.title,
            "description": self.description,
            "page_number": data["page"] + 1,
            "num_pages": len(self.pages),
            "form": form
        })


ACTIVITIES = {
    "demographic": DemographicSurvey,
    "demographic2": DemographicSurvey2,
}

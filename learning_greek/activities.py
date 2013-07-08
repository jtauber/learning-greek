from django import forms
from django.shortcuts import redirect, render


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
                self.activity_state.save()
                return redirect("dashboard")  # @@@
        else:
            form = SurveyForm(questions=self.questions)
        return render(request, "survey.html", {
            "title": self.title,
            "description": self.description,
            "form": form
        })


ACTIVITIES = {
    "demographic": DemographicSurvey,
}

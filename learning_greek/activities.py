from django import forms
from django.shortcuts import redirect, render


from learning_greek.forms import SurveyForm


class DemographicSurvey(object):
    
    def __init__(self, state):
        self.questions = [
            {
                "name": "Age",
                "help_text": "what is your age?",
                "field_class": forms.CharField,
            }
        ]
    
    def handle_request(self, request):
        if request.method == "POST":
            form = SurveyForm(request.POST, questions=self.questions)
            if form.is_valid():
                answers = form.cleaned_data
                # @@@ persist
                print answers
                return redirect("dashboard")  # @@@
        else:
            form = SurveyForm(questions=self.questions)
        return render(request, "survey.html", {"form": form})


ACTIVITIES = {
    "demographic": DemographicSurvey,
}

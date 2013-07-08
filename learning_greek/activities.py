from django import forms
from django.shortcuts import redirect, render


from learning_greek.forms import SurveyForm


class DemographicSurvey(object):
    
    def __init__(self, activity_state):
        self.questions = [
            {
                "name": "Age",
                "help_text": "what is your age?",
                "field_class": forms.CharField,
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
        return render(request, "survey.html", {"form": form})


ACTIVITIES = {
    "demographic": DemographicSurvey,
}

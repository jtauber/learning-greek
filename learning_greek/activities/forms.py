from django import forms


class SurveyForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop("questions")
        super(SurveyForm, self).__init__(*args, **kwargs)
        for question in self.questions:
            field_class = question["field_class"]
            kwargs = {
                "label": question["label"],
            }
            if question.get("help_text"):
                kwargs.update({"help_text": question["help_text"]})
            kwargs.update(question.get("extra_args", {}))
            self.fields[question["name"]] = field_class(**kwargs)

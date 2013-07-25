from django.db import models


class NounCumulativeCount(models.Model):
    
    lemma = models.CharField(max_length=50)
    cumulative_count = models.IntegerField()
    
    @classmethod
    def get_value(cls, value):
        return cls.objects.filter(
            cumulative_count__gt=value
        ).order_by("cumulative_count")[0].lemma


def import_nouncumulativecount(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            count, lemma = line.strip().split()
            total += int(count)
            NounCumulativeCount(lemma=lemma, cumulative_count=total).save()
            print lemma, total


class NounCaseNumberGender(models.Model):
    
    lemma = models.CharField(max_length=50)
    case = models.CharField(max_length=1, choices=[
        ("N", "nominative"),
        ("A", "accusative"),
        ("C", "nominative or accusative"),
        ("G", "genitive"),
        ("D", "dative"),
    ])
    number = models.CharField(max_length=1, choices=[
        ("S", "singular"),
        ("P", "plural"),
    ])
    gender = models.CharField(max_length=1, choices=[
        ("M", "masculine"),
        ("F", "feminine"),
        ("N", "neuter"),
    ])


def import_nouncng(filename):
    with open(filename) as f:
        for line in f:
            lemma, cng = line.strip().split()
            case, number, gender = cng
            NounCaseNumberGender(lemma=lemma, case=case, number=number, gender=gender).save()

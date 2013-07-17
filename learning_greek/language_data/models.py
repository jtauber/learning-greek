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

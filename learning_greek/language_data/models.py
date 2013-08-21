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


class DickinsonCoreList(models.Model):
    
    lemma = models.CharField(max_length=50)
    headword = models.TextField()
    definition = models.TextField()
    pos = models.CharField(max_length=20)
    pos_detail = models.CharField(max_length=50)
    semantic_group = models.CharField(max_length=50)


def import_dcc_core_list(filename):
    count = 0
    with open(filename) as f:
        for line in f:
            lemma, headword, definition, pos, pos_detail, semantic_group = line.strip().split("|")
            DickinsonCoreList(lemma=lemma, headword=headword, definition=definition, pos=pos, pos_detail=pos_detail, semantic_group=semantic_group).save()
            count += 1
    print count


class AbsSyntax(models.Model):
    
    node_id = models.CharField(max_length=15)
    parent_node = models.CharField(max_length=15, null=True)
    category = models.CharField(max_length=10)
    rule = models.CharField(max_length=50, null=True)
    words = models.TextField()


def import_abs_syntax(filename):
    
    with open(filename) as f:
        for line in f:
            node_id, parent_node, category_rule, parse, words = line.strip().split(" ", 4)
            if "{" in category_rule:
                category, rule = category_rule.split("{")
                rule = rule[:-1]
            else:
                category = "T"
                rule = None
            
            if parent_node == "None":
                parent_node = None
            
            AbsSyntax(node_id=node_id, parent_node=parent_node, category=category, rule=rule, words=words).save()

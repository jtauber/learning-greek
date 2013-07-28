#!/usr/bin/env python

with open("greek_core_list.xml") as f:
    for line in f:
        if line.startswith(("<?xml", "<nodes>", "</nodes>")):
            pass
        elif line.startswith("  <node>"):
            fields = {}
        elif line.startswith("  </node>"):
            print "{lemma}|{headword}|{definition}|{pos1}|{pos2}|{semantic-group}".format(**fields)
        elif line.startswith("    <HEADWORD>"):
            s = line.find(">")
            e = line[s:].find("<")
            fields["headword"] = line[s+1:s+e]
            fields["lemma"] = fields["headword"].split()[0].strip(",")
        elif line.startswith("    <DEFINITION>"):
            s = line.find(">")
            e = line[s:].find("<")
            fields["definition"] = line[s+1:s+e]
        elif line.startswith("    <PART-OF-SPEECH>"):
            s = line.find(">")
            e = line[s:].find("<")
            fields["pos2"] = line[s+1:s+e]
            fields["pos1"] = fields["pos2"].split(":")[0]
        elif line.startswith("    <SEMANTIC-GROUP>"):
            s = line.find(">")
            e = line[s:].find("<")
            fields["semantic-group"] = line[s+1:s+e]
        elif line.startswith("    <FREQUENCY-RANK>"):
            pass
        else:
            print line
            quit()

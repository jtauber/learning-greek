from django.shortcuts import render, get_object_or_404


from .models import AbsSyntax


def node_detail(request, node_id):
    node = get_object_or_404(AbsSyntax, node_id=node_id)
    
    parent_node_id = node.parent_node
    
    if parent_node_id:
        parent_node = AbsSyntax.objects.get(node_id=parent_node_id)
    else:
        parent_node = None
    
    category = node.category
    
    rule = node.rule
    
    words = []
    for word in node.words.split():
        word_details = word.split("/")
        child_node = AbsSyntax.objects.filter(node_id=word_details[0])
        if child_node:
            child_node = child_node[0]
        else:
            child_node = None
        words.append({
            "child_node": child_node,
            "node_id": word_details[0],
            "morph_id": word_details[1],
            "text": word_details[2],
        })
    words = sorted(words, key=lambda x: x["morph_id"])
    
    bcv = {
        "43": "John",
    }[node_id[:2]], int(node_id[2:5]), int(node_id[5:8])
    
    return render(request, "language_data/node_detail.html", {
        "bcv": bcv,
        "parent_node": parent_node,
        "category": category,
        "rule": rule,
        "words": words,
    })
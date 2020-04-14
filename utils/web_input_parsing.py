def _tree2paths(tree, paths, current_path):
    current_path += tree["node"] + " "
    paths.append(tree["node"] + " *root* " + current_path + "\n")
    for child in tree["children"]:
        _tree2paths(child, paths, current_path)


def dict_to_paths(trees):
    paths = []
    paths.append('*root* *root* \n')
    for tree in trees:
        _tree2paths(tree, paths, "")

    return paths


def input_text_to_path(input_text):
    """
    Takes text input in the form of simple sentences: CHILD is [NOT] PARENT
    Parses it to a "tree paths" representation that is used in the paper.
    "human is not animal, socrates is human"
    :param input_text: "human is animal, socrates is human, kant is human"
    :return: words_paths = ['*root* *root* \n',
                   'animal *root* animal \n',
                   'human *root* animal human \n',
                   'socrates *root* animal human socrates \n']
    """
    entities = []
    texts = input_text.split(",")
    has_parent = []
    for text in texts:
        words = text.split()
        child = words[0]
        parent = words[-1]

        child_node = next((x for x in entities if x["node"] == child), None)
        if not child_node:
            child_node = {"node": child, "children": []}
            entities.append(child_node)

        parent_node = next((x for x in entities if x["node"] == parent), None)
        if not parent_node:
            parent_node = {"node": parent, "children": []}
            entities.append(parent_node)

        if len(words) == 3:
            has_parent.append(child_node)
            parent_node["children"].append(child_node)

    return dict_to_paths([entry for entry in entities if entry not in has_parent])


def


print(dict_to_paths(input_text_to_dict(text)))

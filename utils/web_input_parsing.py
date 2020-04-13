import json

words_paths = ['*root* *root* \n',
               'animal *root* animal \n',
               'human *root* animal human \n',
               'socrates *root* animal human socrates \n']
maybe_json = """[{
	"node": "animal",
	"children": [{
		"node": "human",
		"children": [{
			"node": "socrates",
			"children": []
		}]
	}]
}]"""


def _tree2paths(tree, paths, current_path):
    current_path += tree["node"] + " "
    paths.append(tree["node"] + " *root* " + current_path + "\n")
    for child in tree["children"]:
        _tree2paths(child, paths, current_path)


def json_to_paths(input_json):
    trees = json.loads(input_json)
    paths = []
    paths.append('*root* *root* \n')
    for tree in trees:
        _tree2paths(tree, paths, "")

    return paths


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []




# input string to json
text = "human is animal, socrates is human, kant is human"
text2 = "human is not animal, socrates is human"

def input_text_to_dict(input_text):
    out = {}
    entities = []
    texts = input_text.split(",")
    for text in texts:
        words = text.split()
        if len(words) == 3:
            child = words[0]
            parent = words[2]
            entities.append((parent, child))

    print(entities)
    lst = entities

    # Build a directed graph and a list of all names that have no parent
    graph = {name: set() for tup in lst for name in tup}
    has_parent = {name: False for tup in lst for name in tup}
    for parent, child in lst:
        graph[parent].add(child)
        has_parent[child] = True

    # All names that have absolutely no parent:
    roots = [name for name, parents in has_parent.items() if not parents]

    # traversal of the graph (doesn't care about duplicates and cycles)
    def traverse(hierarchy, graph, names):
        for name in names:
            hierarchy["name"] = name
            hierarchy["name"] = graph[name]
            # if "children" in hierarchy:
            #     hierarchy["children"].append(traverse({}, graph, graph[name]))
            # else:
            hierarchy["children"] = traverse({}, graph, graph[name])
        return hierarchy
    print(graph)
    hierarchy = traverse({}, graph, roots)
    # {'mike': {'hellen': {}, 'john': {'elisa': {}, 'marry': {}}}}
    print(hierarchy)




input_text_to_dict(text)
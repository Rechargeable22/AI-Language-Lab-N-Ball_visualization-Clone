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






# input string to json
text = "human is animal, socrates is human, kant is human"
text2 = "human is not animal, socrates is human"

def input_text_to_dict(input_text):
    out = {}
    entities = []
    texts = input_text.split(",")
    has_parent=[]
    for text in texts:
        words = text.split()
        child = words[0]
        parent = words[-1]

        child_node=next((x for x in entities if x["name"]==child), None)
        if not child_node:
            child_node={"name":child,"children":[]}
            entities.append(child_node)

        parent_node = next((x for x in entities if x["name"] == parent), None)
        if not parent_node:
            parent_node = {"name": parent, "children": []}
            entities.append(parent_node)

        if len(words)==3:
            has_parent.append(child_node)
            parent_node["children"].append(child_node)


    out=[entry for entry in entities if entry not in has_parent]
    print(out )




input_text_to_dict(text2)
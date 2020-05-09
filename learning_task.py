import random

def gen_is():
    coll = [" is ", " is not "]
    return random.choices(coll, [2, 1], k=1)[0]


if __name__ == '__main__':
    # collect parameters needed
    x = 4
    y = 7
    base = "president"

    # randomly select z entites from wordnet that are somewhat related to the base entity
    # these should be randomly generated from wordnet but make sense in the context
    mock_entities = ["lawyer", "dentist", "woman", "man", "philosopher", "maniac", "musician", "mathematician"]
    z = 4
    words = [base] + random.sample(mock_entities, k=z)

    # generate x random statements involving the base and z entities that are true per definition. Our groundtruth
    # in the task there are different statements involving "some" and "all". I think our project only works with "all".
    # how do we deal with contradictions?
    groundtruth = []
    for _ in range(x):
        a, b = random.sample(words, 2)
        sentence = a + gen_is() + b
        groundtruth.append(sentence)

    # generate y random statements as before. These are not necessarily be true but depend on the groundtruth
    statements = []
    for _ in range(y):
        a, b = random.sample(words, 2)
        sentence = a + gen_is() + b
        statements.append(sentence)

    print(groundtruth)
    print(statements)

    # let user answer whether he thinks each statement is true or false. Show a Venn Diagram for each statement.
    # It might be more useful to highlight the words in question in a diagram of the whole structure.


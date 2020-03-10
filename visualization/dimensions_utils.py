from sklearn.decomposition import PCA
import numpy as np
from visualization.vectors_utils_2d import get_vector_and_length


def reduce_dimensions(balls_dic):
    vectors = []
    words = []
    circles_dic = {}
    for word, values in balls_dic.items():
        words.append(word)
        vectors.append(np.multiply(values[:-2], values[-2]))
    reduced_vectors = PCA(2).fit_transform(vectors)
    for i, word in enumerate(words):
        vector, length = get_vector_and_length(reduced_vectors[i])
        circles_dic[word] = [vector[0], vector[1], length, balls_dic[word][-1]]
    return circles_dic

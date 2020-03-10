import os, glob, shutil


def save_data(file_path, circles_dic):
    with open(file_path, 'w') as file:
        for word, values in circles_dic.items():
            file.write(word + " ")
            file.write(" ".join(str(value) for value in values))
            file.write("\n")


def read_balls_file(file_path, circles_dic=None):
    if circles_dic is None:
        circles_dic = dict()
    with open(file_path, mode="r", encoding="utf-8") as balls_file:
        for line in balls_file.readlines():
            tokens = line.strip().split()
            circles_dic[tokens[0]] = [float(ele) for ele in tokens[1:]]
        return circles_dic


def read_children_file(ws_children_file, children_dic=None):
    if children_dic is None:
        children_dic = dict()
    with open(ws_children_file, 'r') as children_file:
        for ln in children_file:
            if ln is None or ln == "":
                continue
            tokens = ln.split()
            children_dic[tokens[0]] = tokens[1:]
        return children_dic


def read_words_to_show_file(file_path):
    words_to_show = []
    if file_path is None or file_path == "":
        return words_to_show
    with open(file_path, mode="r", encoding="utf-8") as filw:
        for line in filw.readlines():
            words_to_show.extend(line.strip().split(" "))
    return words_to_show


def write_data_to_file(file_path, lines):
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
            if '\n' not in line:
                file.write("\n")


def read_word2vec_file(glove_file_path):
    glove_words_set = set()
    with open(glove_file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            glove_words_set.add(line[:-1].split()[0])
    return glove_words_set


def read_input_words(input_file_path):
    words = []
    with open(input_file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            words.extend([x.strip() for x in str(line).split(',')])
    return words


def set_up_data_folder(output_path):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    else:
        for file in glob.glob(output_path + "/*"):
            if "glove" not in file and "data_out" not in file and "input" not in file:
                os.remove(file)
            elif "data_out" in file:
                shutil.rmtree(file)

import argparse
import os

from balls_generation import train_word2ball, initialize_dictionaries
from tree_generation.generate_tree import generate_files
from visualization.circles_fixer import reduce_and_fix
from visualization.ploting import visualize
from utils.files_utils import set_up_data_folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_nball')
    parser.add_argument('--w2v')
    parser.add_argument('--sample')
    parser.add_argument('--input')
    parser.add_argument('--output_path')
    parser.add_argument('--balls')
    parser.add_argument('--children')
    parser.add_argument('--circles')
    parser.add_argument('--showenWords')
    parser.add_argument('-g', '--generate_nballs', action='store_true')
    parser.add_argument('-v', '--vis', action='store_true')
    parser.add_argument('-rf', '--reduceAndFix', action='store_true')

    args = parser.parse_args()

    if args.generate_nballs:
        if args.w2v and (args.input or args.sample) and args.output_path:
            set_up_data_folder(args.output_path)
            print("Start generating tree files")
            children_file_path, cat_code_file_path = generate_files(args.w2v, args.input, args.sample, args.output_path)
            if children_file_path is None or cat_code_file_path is None:
                print("Unable to generating tree files. Check your input!")
                return
            else:
                print("Finish generating tree files")

            print("Start generating balls")
            n_balls_file_path = args.output_path + '/nballs.txt'
            logFile = os.path.join(args.output_path, 'traing.log')
            balls_files_path = os.path.join(args.output_path, "data_out")
            wsChildrenDic, word2vecDic, wscatCodeDic = initialize_dictionaries(word2vecFile=args.w2v,
                                                                               catDicFile=cat_code_file_path,
                                                                               wsChildrenFile=children_file_path)
            train_word2ball(root="*root*", outputPath=balls_files_path, wsChildrenDic=wsChildrenDic,
                            word2vecDic=word2vecDic, wscatCodeDic=wscatCodeDic, logFile=logFile,
                            word2ballDic=dict(),
                            outputBallFile=n_balls_file_path)
            if os.path.exists(n_balls_file_path):
                print("Finish generating balls successfully")
                print("N-balls file can be found in ", n_balls_file_path)
            else:
                print("Finish generating balls unsuccessfully")

    if args.reduceAndFix:
        if args.balls and args.children and args.output_path:
            reduce_and_fix(args.balls, args.children, args.output_path)

    if args.vis and args.circles:
        visualize(args.circles, args.showenWords)


if __name__ == "__main__":
    main()

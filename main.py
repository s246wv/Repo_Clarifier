from lib.evaluate_repository import *
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Evaluate a repository and its README.")
    parser.add_argument("eval_dir", help="The directory to evaluate.")

    args = parser.parse_args()
    eval_dir = args.eval_dir

    if not os.path.isdir(eval_dir):
        print(f"Error: '{eval_dir}' is not a valid directory.")
    else:
        eval_dir_structure = read_directory_structure(eval_dir)
        evaluation_result = "/_/_/_/_/_/ディレクトリ階層の評価/_/_/_/_/_/\n\n"
        evaluation_result = evaluate_directory(eval_dir_structure)
        evaluation_result += "\n\n/_/_/_/_/_/READMEの評価/_/_/_/_/_/\n\n"
        evaluation_result += evaluate_README(eval_dir, eval_dir_structure)
        print(evaluation_result)


if __name__ == "__main__":
    main()

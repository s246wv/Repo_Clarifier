from read_dir import read_directory_structure
import json
import sys
import os

with open("scoring.json", "r") as f:
    SCORING_NORM = str(json.load(f))

def call_llm(input: str):
    print(input)
    return "good"

def evaluate_repository(dir_str: str):
    prompt = """<SCORING_NORM>を参照に、<REPO_DIR>を評価してください。
    <SCORING_NORM>は評価基準と基準毎の重要度を表しています。
    <REPO_DIR>はGitHub repositoryのディレクトリ階層です。他の人に見せても良いようにブラッシュアップしようとしています。
    出力は下記の形式でお願いします。{"score": <float value>, "description": <Description of the evaluation result>, "solution": <Solution to enhance the repository>}"""
    input = f"{prompt}\n<SCORING_NORM>\n{SCORING_NORM}\n</SCORING_NORM>\n<REPO_DIR>\n{dir_str}\n</REPO_DIR>"
    return call_llm(input)

if __name__ == "__main__":
    # Example usage: evaluate the current directory
    if len(sys.argv) > 1:
        eval_dir = sys.argv[1]
        if not os.path.isdir(eval_dir):
            print(f"Error: '{eval_dir}' is not a valid directory.")
        else:
            eval_dir_structure = read_directory_structure(eval_dir)
            evaluation_result = evaluate_repository(eval_dir_structure)
            print(evaluation_result)

from read_dir import read_directory_structure
import json
import sys
import os
import openai

with open("scoring.json", "r") as f:
    SCORING_NORM = str(json.load(f))

# llama.cppでllmが動いている想定
client = openai.OpenAI(base_url="http://localhost:8080/v1",api_key="dummy")

def call_llm(input: str):
    messages = []
    messages.append(dict(role="system", content="You are a helpful assistant."))
    messages.append(dict(role="user", content=input))
    completion = client.chat.completions.create(model="dummy",messages=messages)
    return completion.choices[0].message.content


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

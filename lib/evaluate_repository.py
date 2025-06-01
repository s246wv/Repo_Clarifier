from .read_dir import read_directory_structure
from pathlib import Path
import yaml
import sys
import os
import openai
import re

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
yaml_file_path = project_root / "rule" / "scoring.yaml"
with open(yaml_file_path, "r") as f:
    SCORING_NORM = yaml.dump(yaml.safe_load(f), allow_unicode=True)

# llama.cppでllmが動いている想定
client = openai.OpenAI(base_url="http://localhost:8080/v1",api_key="dummy")

def call_llm(input: str):
    messages = []
    messages.append(dict(role="system", content="You are a helpful assistant."))
    messages.append(dict(role="user", content=input))
    completion = client.chat.completions.create(model="dummy",messages=messages)
    return completion.choices[0].message.content


def evaluate_directory(dir_str: str):
    prompt = f"""以下の<SCORING_NORM>（リポジトリ評価基準）と<REPO_DIR>（対象リポジトリのディレクトリ階層）を詳細に比較・分析してください。
このリポジトリを、他の開発者にとってより分かりやすく、質の高いものにするための評価と、具体的な改善提案を生成することが目的です。

<SCORING_NORM>
{SCORING_NORM}
</SCORING_NORM>

<REPO_DIR>
{dir_str}
</REPO_DIR>

分析と評価、提案生成の手順：
1.  **プロジェクトの種類の推測:** <REPO_DIR> 内の主要な設定ファイル（例: package.json, tsconfig.json, webpack関連ファイルなど）から、このプロジェクトの主要な言語やフレームワークを推測してください。
2.  **評価項目の照合と現状分析:**
    a. 推測したプロジェクトの種類を考慮し、<REPO_DIR> の構造と<SCORING_NORM> の各評価項目（ファイルやディレクトリパターン）を照合します。
    b. <SCORING_NORM> に記載されている重要なファイルやディレクトリが、<REPO_DIR> の**適切な場所に存在するか**どうかを確認してください。
    c. **存在する場合:** その項目名を挙げ、肯定的に評価してください。（例: 「README.mdが存在し、プロジェクト理解の基本が整っています。」）
    d. **存在しない場合:** その項目名を挙げ、それが不足していることを指摘してください。（例: 「テストコードを格納する 'tests' ディレクトリが見当たりません。」）
    e. **構成の改善点:** 既存のディレクトリ構造（例: `src/`, `public/`, `docs/`）について、<SCORING_NORM>の観点からより良くするための具体的な提案があれば指摘してください。
3.  **スコア算出:** <SCORING_NORM> の `importance_score` と上記2の分析結果を総合的に考慮し、リポジトリ全体の質に対するスコア（1.0から5.0の範囲で、5.0が最高）を算出してください。
4.  **評価と改善提案の記述:**
    * `description` (string): スコアとともに、リポジトリ全体の現状についての簡潔な総評（手順2で分析した良い点、不足している点など）を記述してください。
    * `solution` (string): <REPO_DIR> の現状をより良くするために、**具体的にどのような改善アプローチを取るべきか**という方針や考え方を記述してください。手順2で指摘した不足点や改善点を踏まえ、特に重要と思われる改善策に焦点を当ててください。
    * `improvements` (list of strings): `solution`で述べた方針に基づき、**実行可能で具体的な改善アクション**を3～5個程度提案してください。各提案は、「（どのファイル/ディレクトリに対して）具体的に何をするか」が明確にわかるように記述してください。（例：「`README.md` にプロジェクトのビルド方法と実行手順を追記する。」「テストコード用の `tests` ディレクトリを作成し、主要コンポーネントの単体テストを追加する。」など）

出力は下記のJSON形式で厳密にお願いします。
{{
  "score": <float, 例: 3.8>,
  "description": "<string, 全体的な評価コメント>",
  "solution": "<string, 現状を踏まえた具体的な改善策や方針>",
  "improvements": ["<string, 具体的な改善提案1>", "<string, 具体的な改善提案2>", ...]
}}
"""
    return call_llm(prompt)

def evaluate_README(eval_dir: str, dir_str: str):
    lines = dir_str.split("\n")
    ind = -1
    for i, line in enumerate(lines):
        if re.search(r"README\.(md|rst|txt)", line, re.IGNORECASE):
           ind = i
           break
    if ind == -1:
        return -1
    else:
        readme_line = lines[ind]
        indent_n = readme_line.find("README") // 4
        readme_filename = readme_line.split(" (file)")[0][indent_n*4:]
        for line in list(reversed(lines))[0-ind:]:
            if line.startswith("    "):
                current_indent = (len(line) - len(line.lstrip(" "))) // 4
                if current_indent == indent_n:
                    continue
                else:
                    if line.endswith("(directory)"):
                        readme_path = eval_dir + line.replace(" (directory)", "") + readme_filename
                    else:
                        print("something wrong")
            else:
                if line.endswith("(directory)"):
                    if line.replace(" (directory)", "") == "/":
                        readme_path = eval_dir + readme_filename
                    else:
                        readme_path = eval_dir + line.replace(" (directory)") + readme_filename
    if readme_path:
        with open(readme_path, "r") as f:
            readme_content = f.read()
        prompt = f"""以下はREADMEの内容です。このリポジトリを、他の開発者にとってより分かりやすく、質の高いものにするために、具体的な改善提案を生成してください。
<README>{readme_content}</README>"""
        return call_llm(prompt)
    else:
        return "READMEが見当たりません。"



if __name__ == "__main__":
    # Example usage: evaluate the current directory
    if len(sys.argv) > 1:
        eval_dir = sys.argv[1]
        if not os.path.isdir(eval_dir):
            print(f"Error: '{eval_dir}' is not a valid directory.")
        else:
            eval_dir_structure = read_directory_structure(eval_dir)
            evaluation_result = evaluate_directory(eval_dir_structure)
            evaluation_result += "\n"
            evaluation_result += evaluate_README(eval_dir, eval_dir_structure)
            print(evaluation_result)

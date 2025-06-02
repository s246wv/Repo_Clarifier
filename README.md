# Repo Clarifier: LLMでリポジトリを評価します

## Overview

- GitHub repositoryのディレクトリ階層を評価するためのスクリプトです。
- ディレクトリ階層を読み、構造が明確であるか、重要な情報が記載されているかを検証します。
  - ディレクトリ階層を抽出し、`rule`下の規定と照らし合わせ、重要なファイルの存在を確認します。
  - READMEファイルを読み、改善点を提案します。

## Installation
```bash
git clone git@github.com:s246wv/Repo_Clarifier.git
cd Repo_Clarifier
uv pip install -e .
```

## How to use
- local directoryを対象とします。
  - 事前にGitHub repositoryをlocalにダウンロードしておいてください。
- local llmに対してリクエストすることを想定しています。
  - [llama.cpp](https://github.com/ggml-org/llama.cpp)を利用してテストしており、http://localhost:8080/v1 に対して`openai`パッケージを使ってアクセスしています。
  - 必要に応じて`evaluate_repository.py`を修正してください。

```bash
python main.py [評価したいディレクトリ]
```

## License
This repository is licensed under MIT License (see [LICENSE file](LICENSE) for details)  
このリポジトリのライセンスは MIT License です(詳細は[LICENSEファイル](LICENSE)を御覧ください)。

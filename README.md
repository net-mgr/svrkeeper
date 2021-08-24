# svrkeeper

## 環境
- Debian 10
- Python3.6以上
- Bash

## インストール方法
1. GitHubでForkする

Webテストを行う場合、Forkして、所有者としてアクセス可能なリポジトリにする必要があります。

2. GitHubからcloneする。

以下のコマンドのnet-mgrは自身のアカウント名または自身に所有権がある組織になります。
```bash
git clone https://github.com/net-mgr/svrkeeper.git
```

3. pip3をインストールし、Pythonの必要なモジュールをインストール

```bash
$ sudo apt install python3-pip openssl
$ pip3 install -r requirements.txt
```

4. `config/`以下に設定ファイルを設置

設定ファイルの例を`config_sample/`に配置しています。
設定ファイルの説明は[config/README.md](config/README.md)に記述しています。

## テストの実行方法

`./run.sh`を実行し、設定ファイルを作成したときに使用したパスワードを入力する。
```bash
$ ./run.sh
# Input setting file password: 
##################################################
# Results of each category
# Category 3: Web test
# => All tests were passed.
##################################################
# Total result
# => All tests were passed.
```

テスト結果は各カテゴリごとに出力されます。

|テスト結果のメッセージ                                      | 説明                                                             |
|:-----------------------------------------------------------|:-----------------------------------------------------------------|
|# => All tests were passed.                                 |そのカテゴリのテストはすべて合格またはテストが実施されていません。|
|# => Some tests were not passed. Check results.             |そのカテゴリのテストのうち、1つ以上で不合格です。                 |
|# => Some tests has error. Check results.                   |そのカテゴリのテストでエラーが発生しています。                    |

また、テスト結果は以下のファイルに保存されています。

|カテゴリ |保存先              |
|:--------|:-------------------|
|web      |results/Web_test.log|

## ディレクトリ構成

| ディレクトリ名 | 内容|
| config |テストに必要なパラメータや暗号化した認証情報を保存|
| config_sample | configに設置するファイルの例を保存。テストには使わない。 |
| results | テスト結果を保存 |
| scripts | テストを実行するスクリプトを保存。すべて`run.sh`からのみ呼び出す|

## TODO
- `scripts/web_test.sh`の内部からのアクセスのテスト
- その他のテスト
- `run.sh`でカテゴリを選んでテストする仕組み
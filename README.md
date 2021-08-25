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

`./run.sh`を実行する。

```bash
$ ./run.sh
```

テストはカテゴリを1つ指定することで、そのカテゴリのみ実行されます。

```bash
$ ./run.sh login
$ ./run.sh mail
$ ./run.sh web
$ ./run.sh edit
$ ./run.sh backup
$ ./run.sh dns
$ ./run.sh access
```
テストを実行するとパスワードの入力を求められます。設定ファイルを作成したときに使用したパスワードを入力してください。

```bash
# Input setting file password: 
##################################################
# Results of each category
# Category 1: Login test
# => All tests were passed.
# Category 2: Mail test
# => All tests were passed.
# Category 3: Web test
# => All tests were passed.
# Category 4: File editing test
# => All tests were passed.
# Category 5: Backup test
# => All tests were passed.
# Category 6: DNS test
# => All tests were passed.
# Category 7: Access point test
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

|カテゴリ           | 保存先                        |
|:------------------|:------------------------------|
| Login test        | results/login_test.log        |
| Mail test         | results/mail_test.log         |
| Web test          | results/Web_test.log          |
| File editing test | results/edit_file_test.log    |
| Backup test       | results/backup_test.log       |
| DNS test          | results/dns_test.log          |
| Access point test | results/access_point_test.log |





## ディレクトリ構成

| ディレクトリ名 | 内容|
|:-----------|:----|
| config |テストに必要なパラメータのファイルを保存。また、暗号化した認証情報は`config/setting.sec.sh`に暗号化して保存。（詳しくは[config/README.md](config/README.md)|
| config_sample | configに設置するファイルの例を保存。テストには使わない。 |
| results | テスト結果を保存 |
| scripts | テストを実行するスクリプトを保存。すべて`run.sh`からのみ呼び出す|

## TODO
- `scripts/web_test.sh`の内部からのアクセスのテストの実装
- その他のテストの実装（現在は`exit 0`のみになっている)
    - `scripts/access_point_test.sh`
    - `scripts/backup_test.sh`
    - `scripts/dns_test.sh`
    - `scripts/edit_file_test.sh`
    - `scripts/login_test.sh`
    - `scripts/mail_test.sh`

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
sudo apt install python3-pip
pip3 install -r requirements.txt
```

4. `config/`以下に設定ファイルを設置

設定ファイルの例を`config_sample/`に配置しています。
設定ファイルの説明は[config/README.md](config/README.md)に記述しています。

## テストの実行方法

```bash
./run.sh
```
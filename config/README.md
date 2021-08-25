configの書き方
============

## Webテスト

### 外部から

GitHub ActionsからWebサイトにアクセスできるか確認するテストです。
必要な設定ファイルは下に示す2つです。

| ファイル名              | 説明                                                                |
|:------------------------|:--------------------------------------------------------------------|
|setting.sec.sh           | 他のテストと共通のファイルです。このテストでは、GitHub Actionsにアクセスするために必要な情報をこのファイルに書き込む必要があります。|
|web_outside.json         | テストの対象となるURLと想定されるテスト結果を設定するファイルです。 | 


設定ファイルの書き方を説明します。

1. GitHubでPersonal access tokensを生成する
GitHubにPCのブラウザでログインし、右上の自分のアイコン→`Settings`→`Developer settings`→`Personal access tokens`
→`Generate new token`の順にクリックする。

次に、以下のように設定する

| 項目名        | 設定例                                         |
|:--------------|:-----------------------------------------------|
| Note          | 自分にとってわかりやすいメモ                   |
| Expiration    | No expiration または、このスクリプトを使う期間 |
| Select scopes | repoにチェック                                 |


2. `config/setting.sh`に設定を記述

必要な情報は以下の4つ
- Forkしたリポジトリの所有者→以下の例の`net-mgr`の部分に置き換える
- リポジトリ名(変更していなければ、`svrkeeper`)→以下の例の`svrkeeper`の部分を置き換える
- リポジトリにアクセス権を持つユーザのユーザ名→以下の例の`user_name`の部分を置き換える
- 1.で生成したアクセストークン→以下の例の`ghp-tokentokentoken`の部分を置き換える

`config/setting.sh`の例を以下に示す。

```bash
export GITHUB_OWNER=net-mgr
export GITHUB_REPO_NAME=svrkeeper
export GITHUB_USERNAME=user_name
export GITHUB_TOKEN=ghp_tokentokentoken
```

3. opensslで暗号化する

下のコマンドのパスワードを任意のパスワードに書き換えて実行（このパスワードはテスト実行のたびに求められます）
```bash
openssl enc -e -aes256 -pbkdf2 -in config/setting.sh -out config/setting.sec.sh -k パスワード
```

4. `config/web_outside.json`に設定を記述

エンコーディングは必ずUTF-8(BOMなし)にする。

テスト1つずつをディクショナリ型で表現したリストとして記述する。

テスト1つに以下の項目を設定する

| 項目名（key) | 必須・任意 |説明                                                                                                |
|:-------------|:----------:|:---------------------------------------------------------------------------------------------------|
| description  | 任意       | テスト結果に表示される文字列                                                                       |
| url          | 必須       | テスト時にアクセスするURL                                                                          |
| status       | 必須       | テスト時にURLにアクセスした際、HTTPレスポンスに含まれるステータスコード（想定するステータスコード）|

設定例を以下に示す。

```bash
[
	{
		"description": "テスト１: https://example.comに正常にアクセスできるか確認（ステータスコード200が正常）",
		"url": "https://example.com",
		"status": 200
	},
	{
		"description": "テスト2: Basic認証がかかっているかテストする例",
		"url": "https://example.com/401",
		"status": 401
	},
	{
		"description": "テスト3: アクセス拒否されるか確認する例",
		"url": "https://example.com/403",
		"status": 403
	}
]
```
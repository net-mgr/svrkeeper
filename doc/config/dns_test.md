## DNSテストの設定ファイルの書き方

DNSテストはGitHub Actionsからのアクセス結果を確認するテスト（以降、外側からのテスト）とこのテストスクリプトがインストールされた計算機から行うテスト（以降、内側からのテスト）があります。外側からのテストと内側からのテストの両方を設定することができます。また、外側からのテストと内側からのテストどちらかのみを設定することもできます。

このテストスクリプトはLAN内部から実行し、内側からのテストでは，内部から指定したドメインの名前を解決します．
外側からのテストでLAN内部と結果が異なる名前解決可能なドメインについて確認することを意図しています。

### 外部からのテスト

GitHub Actionsから名前解決できるか確認するテストです。
必要な設定ファイルは下に示す2つです。

| ファイル名              | 説明                                                                |
|:------------------------|:--------------------------------------------------------------------|
|setting.sec.sh           | 他のテストと共通のファイルです。このテストでは、GitHub Actionsにアクセスするために必要な情報をこのファイルに書き込む必要があります。|
|dns_outside.json         | 外側からのDNSテストの対象となるドメインおよびIPアドレスと想定されるテスト結果を設定するファイルです。 | 


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

必要な情報は以下の5つ
- Forkしたリポジトリの所有者→以下の例の`net-mgr`の部分に置き換える
- リポジトリ名(変更していなければ、`svrkeeper`)→以下の例の`svrkeeper`の部分を置き換える
- ブランチ名（変更していなければ、`main`）→以下の例の`main`の部分を置き換える
- リポジトリにアクセス権を持つユーザのユーザ名→以下の例の`user_name`の部分を置き換える
- 1.で生成したアクセストークン→以下の例の`ghp-tokentokentoken`の部分を置き換える

`config/setting.sh`の例を以下に示す。

```bash
export GITHUB_OWNER=net-mgr
export GITHUB_REPO_NAME=svrkeeper
export GITHUB_BRANCH=main
export GITHUB_USERNAME=user_name
export GITHUB_TOKEN=ghp_tokentokentoken
```

3. opensslで暗号化する

下のコマンドのパスワードを任意のパスワードに書き換えて実行（このパスワードはテスト実行のたびに求められます）
```bash
openssl enc -e -aes256 -pbkdf2 -in config/setting.sh -out config/setting.sec.sh -k パスワード
```

4. `config/dns_outside.json`に設定を記述

エンコーディングは必ずUTF-8(BOMなし)にする。

テスト1つずつをディクショナリ型で表現したリストとして記述する。

テスト1つに以下の項目を設定する

| 項目名（key) | 必須・任意                | 説明                                                                                                             |
|:-------------|:-------------------------:|:-----------------------------------------------------------------------------------------------------------------|
| description  | 任意                      | テスト結果に表示される文字列                                                                                     |
| flag         | 必須                      | `true`なら名前解決に成功すると正常，`false`なら名前解決に失敗すると正常扱いとなる                                |
| method       | 必須                      | `default`なら正引き，`reverse`なら逆引きでテストを行う                                                           |
| domain       | methodがdefaultの場合必須 | 正引きの場合，名前解決可能かテストするドメインを指定する                                                         |
|              |                           | 逆引きの場合，IPアドレスから解決されたドメインと一致するか確認するドメインを指定する（存在しない場合，確認を行わない） |
| addr         | methodがreverseの場合必須 | 正引きの場合，解決されたIPアドレスと一致するか確認するIPアドレスを指定する（空の場合，確認を行わない）           |
|              |                           | 逆引きの場合，名前解決可能かテストするIPアドレスを指定する                                                       |


設定例を以下に示す。

```bash
[
	{
	    "description": "テスト1:example.comの名前が解決できることを確認(正引き)",
	    "method": "default",
	    "flag": "true",
	    "domain": "example.com"
	},{
	    "description": "テスト2: example.comの名前と指定したIPが一致することを確認(正引き)",
	    "method": "default",
	    "flag": "true",
	    "domain": "example.com",
	    "addr": "93.184.216.34"
	},{
	    "description": "テスト3: www.example.comの名前と指定したIPが一致しないことを確認(正引き)",
	    "method": "default",
	    "flag": "false",
	    "domain": "example.com",
	    "addr": "192.168.1.1"
	},{
	    "description": "テスト4:IPから名前解決できることを確認(逆引き)",
	    "method": "reverse",
	    "flag": "true",
	    "addr": "153.126.193.74"
	},{
	    "description": "テスト5: IPから解決した名前が指定したドメインと一致することを確認(逆引き)",
	    "method": "reverse",
	    "flag": "true",
	    "domain": "ik1-332-26320.vs.sakura.ne.jp",
	    "addr": "153.126.193.74"
	},{
	    "description": "テスト6: IPから解決した名前が指定したドメインと一致しないことを確認(逆引き)",
	    "method": "reverse",
	    "flag": "false",
	    "domain": "example.com",
	    "addr": "153.126.193.74"
	}
]
```
### 内側からのテスト

ネットワークの内側から名前解決できるか確認するテストです。
必要な設定ファイルは下に示す1つです。

| ファイル名              | 説明                                                                |
|:------------------------|:--------------------------------------------------------------------| 
|dns_inside.json         | 内側からのWDNSテストの対象となるドメインおよびIPアドレスと想定されるテスト結果を設定するファイルです。 | 


1. `config/dns_inside.json`に設定を記述

エンコーディングは必ずUTF-8(BOMなし)にする。

テスト1つずつをディクショナリ型で表現したリストとして記述する。

テスト1つに以下の項目を設定する

| 項目名（key) | 必須・任意 | 説明                                                                                                |
|:-------------|:----------:|:----------------------------------------------------------------------------------------------------|
| description  | 任意                      | テスト結果に表示される文字列                                                                                     |
| flag         | 必須                      | `true`なら名前解決に成功すると正常，`false`なら名前解決に失敗すると正常扱いとなる                                |
| method       | 必須                      | `default`なら正引き，`reverse`なら逆引きでテストを行う                                                           |
| domain       | methodがdefaultの場合必須 | 正引きの場合，名前解決可能かテストするドメインを指定する                                                         |
|              |                           | 逆引きの場合，IPアドレスから解決されたドメインと一致するか確認するドメインを指定する（存在しない場合，確認を行わない） |
| addr         | methodがreverseの場合必須 | 正引きの場合，解決されたIPアドレスと一致するか確認するIPアドレスを指定する（空の場合，確認を行わない）           |
|              |                           | 逆引きの場合，名前解決可能かテストするIPアドレスを指定する                                                       |
                                             |

設定例を以下に示す。

```bash
[
	{
	    "description": "テスト1:example.comの名前が解決できることを確認(正引き)",
	    "method": "default",
	    "flag": "true",
	    "domain": "example.com",
	    "addr": ""
	},{
	    "description": "テスト2: example.comの名前と指定したIPが一致することを確認(正引き)",
	    "method": "default",
	    "flag": "true",
	    "domain": "example.com",
	    "addr": "93.184.216.34"
	},{
	    "description": "テスト3: www.example.comの名前と指定したIPが一致しないことを確認(正引き)",
	    "method": "default",
	    "flag": "false",
	    "domain": "example.com",
	    "addr": "192.168.1.1"
	},{
	    "description": "テスト4:IPから名前解決できることを確認(逆引き)",
	    "method": "reverse",
	    "flag": "true",
	    "domain": "",
	    "addr": "153.126.193.74"
	},{
	    "description": "テスト5: IPから解決した名前が指定したドメインと一致することを確認(逆引き)",
	    "method": "reverse",
	    "flag": "true",
	    "domain": "ik1-332-26320.vs.sakura.ne.jp",
	    "addr": "153.126.193.74"
	},{
	    "description": "テスト6: IPから解決した名前が指定したドメインと一致しないことを確認(逆引き)",
	    "method": "reverse",
	    "flag": "false",
	    "domain": "example.com",
	    "addr": "153.126.193.74"
	}
]

```

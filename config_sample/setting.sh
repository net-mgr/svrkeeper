# このファイルは以下のコマンドで暗号化する必要があります。また、暗号化したあとは、暗号化前のファイルを削除してください。
# $ openssl enc -e -aes256 -pbkdf2 -in setting.sh -out setting.sec.sh -k パスワード
# $ rm setting.sh

#Web outside test
# アクセス先： https://api.github.com/repos/{WEB_GITHUB_OWNER}/{WEB_GITHUB_REPO_NAME}/
# Basic認証でusernameをWEB_GITHUB_USERNAME、パスワードをWEB_GITHUB_TOKENとしてアクセスします。
# WEB_GITHUB_BRANCHに設定されたブランチを指定してGitHub Actionsを実行します。
# WEB_GITHUB_OWNER、WEB_GITHUB_REPO_NAME、GITHUB_USENAME、WEB_GITHUB_TOKENのいずれかが設定されていない場合、Web outside testは実行されない。
export WEB_GITHUB_OWNER=net-mgr
export WEB_GITHUB_REPO_NAME=svrkeeper
export WEB_GITHUB_BRANCH=main
export WEB_GITHUB_USERNAME=user_name
export WEB_GITHUB_TOKEN=ghp_tokentokentoken

#########################################################################
### Mail inside test
## Mail Sender settings

export MAIL_INTERNAL_SENDER_ACCOUNT=net-test
export MAIL_INTERNAL_SENDER_ACCOUNT_PASS=passwd
export MAIL_INTERNAL_SMTPSV_ADDRESS=smtps@sample
#      MAIL_INTERNAL_SMTPSV_PORT: 587 or 465 or 25(not recommended)
export MAIL_INTERNAL_SMTPSV_PORT=587

## Mail Receiver settings
#      MAIL_INTERNAL_RECEIVE_PORT: "pop3"  => 110
#                                  "pop3s" => 995
#                                  "imap"  => 143
#                                  "imaps" => 993
export MAIL_INTERNAL_TEST_TARGETS_NUM=2
export MAIL_INTERNAL_RECEIVER_ADDRESS_1=user1@sample
export MAIL_INTERNAL_RECEIVER_ACCOUNT_1=user1
export MAIL_INTERNAL_RECEIVER_ACCOUNT_PASS_1=user1_passwd
export MAIL_INTERNAL_RECEIVESV_ADDRESS_1=pop3s@sample
export MAIL_INTERNAL_RECEIVESV_PORT_1=995

export MAIL_INTERNAL_RECEIVER_ADDRESS_2=mail-list1@sample ## user1を含むメーリングリスト
export MAIL_INTERNAL_RECEIVER_ACCOUNT_2=user1 ## メーリングリストに含まれるアカウント
export MAIL_INTERNAL_RECEIVER_ACCOUNT_PASS_2=user1_passwd
export MAIL_INTERNAL_RECEIVESV_ADDRESS_2=pop3s@sample
export MAIL_INTERNAL_RECEIVESV_PORT_2=995

export MAIL_INTERNAL_RECEIVER_NONEXIST_ACCOUNT=no-address@sample


#################################
### Mail outside test
export MAIL_GMAIL_ADDRESS=sample@gmail.com
export MAIL_GMAIL_CLIENT_SECRETS_PATH="$SCRIPTS_DIR/config_sample/client_secrets.json"
export MAIL_GMAIL_TOKEN_PATH="$SCRIPTS_DIR/config_sample/token.json"

export MAIL_EXTERNAL_RECEIVER_NONEXIST_ACCOUNT=notexist@notexist
#########################################################################

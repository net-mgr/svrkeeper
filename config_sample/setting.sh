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

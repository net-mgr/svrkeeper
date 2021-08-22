#/usr/bin/bash

DIR=`dirname $0`

. $DIR/../config/web_outside_auth.sh

python3 $DIR/web/outside_main.py $GITHUB_OWNER $GITHUB_REPO_NAME $GITHUB_USERNAME $GITHUB_TOKEN --web-outside-json $DIR/../config/web_outside.json

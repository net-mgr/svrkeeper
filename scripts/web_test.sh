#/usr/bin/bash
#
# Webに関するテストを実行
# 
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
# 

DIR=$(cd $(dirname $0); pwd)

# テストに必要な設定があるか
test_outside_exec=1
test_inside_exec=1

if [ -z $GITHUB_OWNER ]; then
    test_outside_exec=0
fi
if [ -z $GITHUB_REPO_NAME ]; then
    test_outside_exec=0
fi
if [ -z $GITHUB_USERNAME ]; then
    test_outside_exec=0
fi
if [ -z $GITHUB_TOKEN ]; then
    test_outside_exec=0
fi
# web_outside.jsonの確認
if [ ! -e $DIR/../config/web_outside.json ]; then
    test_outside_exec=0
fi
# web_inside.jsonの確認
if [ ! -e $DIR/../config/web_inside.json ]; then
    test_inside_exec=0
fi

# 設定ファイルがあるテストの実行: 
# TEST_OUTSIDE_RESULTとTEST_INSIDE_RESULTについて
# 0: テスト合格
# 1: テストで異常発生
# 2: テスト不合格
TEST_OUTSIDE_RESULT=0
TEST_INSIDE_RESULT=0

if [ $test_outside_exec -eq 1 ]; then
    python3 $DIR/web/outside_main.py $GITHUB_OWNER $GITHUB_REPO_NAME $GITHUB_USERNAME $GITHUB_TOKEN --web-outside-json $DIR/../config/web_outside.json
    TEST_OUTSIDE_RESULT=$?
else
    echo "No Web outside test executed."
fi

if [ $test_inside_exec -eq 1 ]; then
    # TODO テストの実装：現在は以下のtrueコマンドをテストの代わりとしている
    # true
    python3 $DIR/web/inside_main.py --web-inside-json $DIR/../config/web_inside.json
    TEST_INSIDE_RESULT=$?
fi


# テスト結果の集約
if [ $TEST_OUTSIDE_RESULT -eq 2 ];then
    TEST_RESULT=1
fi
if [ $TEST_INSIDE_RESULT -eq 2 ];then
    TEST_RESULT=1
fi

if [ $TEST_OUTSIDE_RESULT -eq 1 ];then
    TEST_RESULT=-1
fi
if [ $TEST_INSIDE_RESULT -eq 1 ];then
    TEST_RESULT=-1
fi

exit $TEST_RESULT

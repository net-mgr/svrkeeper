#/usr/bin/bash
#
# Mailに関するテストを実行
# 
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
# 
DIR=$(cd $(dirname $0); pwd)

test_inside_exec=1
test_outside_exec=1

# TEST_OUTSIDE_RESULTとTEST_INSIDE_RESULTについて
# 0: テスト合格
# 1: テストで異常発生
# 2: テスト不合格
TEST_INSIDE_RESULT=0
TEST_OUTSIDE_RESULT=0

if [ $test_inside_exec -eq 1 ]; then
    python3 $DIR/mail/inside_main.py 
    TEST_INSIDE_RESULT=$?
else
    echo "No Mail inside test executed."
fi

if [ $test_outside_exec -eq 1 ]; then
    python3 $DIR/mail/outside_main.py 
    TEST_OUTSIDE_RESULT=$?
else
    echo "No Mail outside test executed."
fi

TEST_RESULT=0

# テスト結果の集約
if [ $TEST_INSIDE_RESULT -eq 2 ];then
    TEST_RESULT=1
fi
if [ $TEST_OUTSIDE_RESULT -eq 2 ];then
    TEST_RESULT=1
fi

if [ $TEST_INSIDE_RESULT -eq 1 ];then
    TEST_RESULT=-1
fi
if [ $TEST_OUTSIDE_RESULT -eq 1 ];then
    TEST_RESULT=-1
fi

exit $TEST_RESULT

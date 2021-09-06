#!/bin/bash
#
# アクセスポイントに関するテストを実行
#
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
#

function main() {
    echo "######################################################################"
    echo "Access Points Test : Test for accessing access point"

    all_passed=1
    num=1
    SCRIPTS_DIR=$(cd $(dirname $0); pwd)
    while read line
    do
        access_test $num $line || all_passed=0
        num=$(expr $num + 1)
    done < ${SCRIPTS_DIR}/../config/access_point_list.txt

    echo "##################################################"
    if [ $all_passed -eq 1 ]; then
        echo "=> All tests were passed."
        exit 0
    else
        echo "=> Some tests were not passed. Check results."
        exit 1
    fi
}

function access_test() {
    local num=$1
    local domain=$2
    echo "##################################################"
    echo "# Number $num: Is it possible to access $domain?"
    echo "# Expectation: $domain returns ping"
    echo "# Attempting: ping -c 1 $domain"
    ping -c 1 $domain
    if [ $? -eq 0 ]; then
        echo -e "=> Passed.\n"
        return 0
    else
        echo -e "=> Failed.\n"
        return 1
    fi
}

main
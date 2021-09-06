#!/bin/bash
#
# ファイル編集に関するテストを実行
#
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
#

TMPFILE="$HOME/.tmpfile_to_test_server"

function main() {
    echo "######################################################################"
    echo -e "Edit File Test : Test for creation and edit file in home directory\n"

    # File create test
    if can_create_tmpfile; then
        echo -e "=> Success\n"
    else
        echo "=> Failed"
        echo -e "File edit test was skipped\n"
        result_summary 0 1 1
        return 1
    fi

    # File edit test
    if can_edit_tmpfile; then
        echo -e "=> Success\n"
    else
        echo -e "=> Failed\n"
        result_summary 1 1 0
        return 1
    fi

    result_summary 2 0 0
    return 0
}

function result_summary() {
    pass_num=$1
    fail_num=$2
    skip_num=$3

    echo "test result : $pass_num passed, $fail_num failed, $skip_num skipped"
    if [ $fail_num = 0 ]; then
        echo "All tests were passed"
    else
        echo "Some tests were failed"
    fi
}

function can_create_tmpfile() {
    echo "File creation test: \`touch $TMPFILE\`"

    if touch $TMPFILE; then
        rm $TMPFILE
        return 0 # Success
    else
        return 1 # Fail
    fi
}

function can_edit_tmpfile() {
    echo "File edit test: \`cat <message> > $TMPFILE\`"

    message="This is tmpfile to test server"
    echo "$message" > $TMPFILE
    if [ "$(cat $TMPFILE)" = "$message" ]; then
        rm $TMPFILE
        return 0 # Success
    else
        return 1 # Fail
    fi
}

main


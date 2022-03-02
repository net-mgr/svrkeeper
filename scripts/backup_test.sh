#!/bin/bash
#
# Backupに関するテストを実行
#
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
#

function main() {
    echo "######################################################################"
    echo "Backup Test : Test for buckup"

    all_passed=1

    SCRIPTS_DIR=$(cd $(dirname $0); pwd)
    source "${SCRIPTS_DIR}/../config/config.sh"

    ssh -i $BACKUP_SSH_KEY $BACKUP_USER@$BACKUP_HOST "$BACKUP_SH $BACKUP_SCRIPT"
    if [ $? -ne 0 ]; then
        echo -e "=> Failed. (SSH TO REMOTE FAILED)\n"
        all_passed=0
    fi

    echo "##################################################"
    if [ $all_passed -eq 1 ]; then
        echo "=> All tests were passed."
        exit 0
    else
        echo "=> Some tests were not passed. Check results."
        exit 1
    fi
}

main

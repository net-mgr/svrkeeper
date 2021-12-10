#!/bin/bash

# バックアップ先にこのファイルと ../config/backup_config.sh を置く．

#echo "`date`: backup started." >> $LOGFILE

function main() {
    SCRIPTS_DIR=$(cd $(dirname $0); pwd)
    source "${SCRIPTS_DIR}/../config/backup_config.sh"
    for i in ${!BACKUP_SRC_DIR[@]}; do
        echo "####################################################################"
        echo "*** backup FROM ${BACKUP_HOST[i]}:${BACKUP_SRC_DIR[i]} TO ${BACKUP_DEST_DIR[i]}"
        echo "####################################################################"
        $BACKUP_COMMAND $BACKUP_OPTIONS "ssh -i $SSH_KEY" ${BACKUP_USER}@${BACKUP_HOST[i]}:${BACKUP_SRC_DIR[i]} ${BACKUP_DEST_DIR[i]}
        if [ $? -ne 0 ]; then
            echo "`date`: backup FROM ${BACKUP_HOST[i]}:${BACKUP_SRC_DIR[i]} TO ${BACKUP_DEST_DIR[i]}" >> $LOGFILE
            exit 1
        fi
    done

    echo "`date`: backup SUCCEEDED."
}

main

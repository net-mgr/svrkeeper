#!/usr/bin/env python3
# GitHub Actionsで実行するスクリプト
# dns_outside.jsonファイルからjsonを読み込み、
# それぞれのURLにアクセスし、ステータスコードが一致するか確認
# 結果はresult.txtに書き込む

import json
import socket

def dnslookup(hosts, result):
    i = 1
    for host in hosts:
        addr = socket.gethostbyname(host['domain'])
        if addr != host['addr']:
            result.append(i)
        i += 1


if __name__ == '__main__':
    # read json
    with open('dns_outside.json', 'r') as json_hosts:
        hosts = json.load(json_items)
    result = []
    dnslookup(hosts, result)
    with open('result.txt', 'w') as result_file:
        for i in result:
            result_file.write(str(i)+'\n')

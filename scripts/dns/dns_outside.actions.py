#!/usr/bin/env python3
# GitHub Actionsで実行するスクリプト
# dns_outside.jsonファイルからjsonを読み込み、
# それぞれのURLにアクセスし、ステータスコードが一致するか確認
# 結果はresult.txtに書き込む

import json
import socket

def dnslookup(host, result, i):
    try:
        flag = ('true' == host['flag'])
        addr = socket.gethostbyname(host['domain'])
        if len(host['addr']) != 0:
            if (addr == host['addr']) ^ flag:
                result.append(i)
    except:
        result.append(i)

def reverse_dnslookup(host, result, i):
    try:
        flag = ('true' == host['flag'])
        host_name = socket.gethostbyaddr(host['addr'])[0]
        if len(host['domain']) != 0:
            if (host_name == host['domain']) ^ flag:
                result.append(i)
    except:
        result.append(i)


if __name__ == '__main__':
    # read json
    with open('dns_outside.json', 'r') as json_hosts:
        hosts = json.load(json_hosts)
    result = []
    i = 1
    for host in hosts:
        if host['method'] == 'default':
            if "addr" not in host:
                dns_outside["addr"]=""
                dnslookup(host, result, i)
        else:
            if "domain" not in host:
                dns_outside["domain"]=""
                reverse_dnslookup(host, result, i)
        i += 1
            
    with open('result.txt', 'w') as result_file:
        for i in result:
            result_file.write(str(i)+'\n')

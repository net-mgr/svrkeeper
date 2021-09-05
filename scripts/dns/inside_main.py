import sys
import argparse
import json
import zipfile
import tempfile
import os
import socket

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dns-inside-json", help="../config/dns_inside.json以外に設定ファイルを置く場合はここにスクリプトからの相対パスを指定",default="../config/dns_inside.json")
    args = parser.parse_args()

    try:
        dns_inside_json=read_file(args.dns_inside_json)
        dns_inside_list=json.loads(dns_inside_json)
    except FileNotFoundError as e:
        print("ファイル"+args.dns_inside_json+"がreadで開けません。設定ファイルを確認してください")
        print("エラーメッセージ："+str(e))
        sys.exit(1)
    except UnicodeDecodeError as e:
        print("ファイル"+args.dns_inside_json+"はUTF-8ではありません。設定ファイルを確認してください")
        print("エラーメッセージ："+str(e))
        sys.exit(1)
    except json.decoder.JSONDecodeError as e:
        print("ファイル"+args.dns_inside_json+"はjson形式ではありません。設定ファイルを確認してください")
        print("parserからのエラーメッセージ："+str(e))
        sys.exit(1)
    
    try:
        make_valid_dns_inside_json(dns_inside_list)
    except ValueError as e:
        print("設定ファイル："+args.dns_inside_json+"に以下の問題があります。")
        print(e)
        sys.exit(1)

    error_flag = False
    for host in dns_inside_list:
        if host['method'] == 'default':
            if "addr" not in host:
                host["addr"]=""
            error_flag |= dnslookup(host)
        else:
            if "domain" not in host:
                host["domain"]=""
            error_flag |= reverse_dnslookup(host)
                
    if error_flag == True:
        sys.exit(2)
        
    print("All web inside tests passed")
    sys.exit(0)        
        
def error_print(host):
    print("test failed: "+host["description"])
    print("method: "+host["method"])
    print("flag: "+host["flag"])
    print("domain: "+host["domain"])
    print("addr: "+host["addr"])
    print("")

def dnslookup(host):
    try:
        flag = ('true' == host['flag'])
        addr = socket.gethostbyname(host['domain'])
        if len(host['addr']) != 0:
            if (addr == host['addr']) ^ flag:
                error_print(host)
                return True
        return False
    except:
        error_print(host)
        return True

def reverse_dnslookup(host):
    try:
        flag = ('true' == host['flag'])
        host_name = socket.gethostbyaddr(host['addr'])[0]
        if len(host['domain']) != 0:
            if (host_name == host['domain']) ^ flag:
                error_print(host)
                return True
        return False
    except:
        error_print(host)
        return True

def read_file(file_name):
    """
    read_fileは、引数に指定されたファイルを読み込み、文字列として返す
    """
    l=[]
    with open(file_name) as f:
        l=f.read()
    return l

def make_valid_dns_inside_json(dns_inside_list):
    """
    make_valid_dns_inside_jsonは、ディクショナリのリストを引数として受け取る。
    各ディクショナリにdescription, method, flag, domain, addrのキーがあるか確認し、
    method，flag，domain，およびaddrがない場合は、ValueErrorを送出する
    descriptionがない場合は空白のdescriptionを追加する
    """
    for dns_inside in dns_inside_list:
        if "description" not in dns_inside:
            dns_inside["description"]=""
        if "method" not in dns_inside:
            raise ValueError("リストのすべての要素に'method'が必要です。'method'が無い要素があります。テスト対象のmethodを記述するか、その要素を削除してください")            
        if "flag" not in dns_inside:
            raise ValueError("リストのすべての要素に'flag'が必要です。'flag'が無い要素があります。テスト対象のflagを記述するか、その要素を削除してください")
        if  dns_inside["method"] == "default":
            if "domain" not in dns_inside:
                raise ValueError("正引きのリストのすべての要素に'domain'が必要です。'domain'が無い要素があります。テスト対象のドメインを記述するか、その要素を削除してください")
            if "addr" not in dns_inside:
                dns_inside["addr"]=""
        else:
            if "domain" not in dns_inside:
                dns_inside["domain"]=""
            if "addr" not in dns_inside:
                raise ValueError("逆引きのリストのすべての要素に'addr'が必要です。'addr'が無い要素があります。テスト対象のIPアドレスを記述するか、その要素を削除してください")

if __name__ == "__main__":
    main()

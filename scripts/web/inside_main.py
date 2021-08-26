import sys
import argparse
import json
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--web-inside-json", help="../config/web_inside.json以外に設定ファイルを置く場合はここにスクリプトからの相対パスを指定",default="../config/web_inside.json")
    args = parser.parse_args()

    try:
        web_inside_json=read_file(args.web_inside_json)
        web_inside_list=json.loads(web_inside_json)
    except FileNotFoundError as e:
        print("ファイル"+args.web_inside_json+"がreadで開けません。設定ファイルを確認してください")
        print("エラーメッセージ："+str(e))
        sys.exit(1)
    except UnicodeDecodeError as e:
        print("ファイル"+args.web_inside_json+"はUTF-8ではありません。設定ファイルを確認してください")
        print("エラーメッセージ："+str(e))
        sys.exit(1)
    except json.decoder.JSONDecodeError as e:
        print("ファイル"+args.web_inside_json+"はjson形式ではありません。設定ファイルを確認してください")
        print("parserからのエラーメッセージ："+str(e))
        sys.exit(1)
    
    try:
        make_valid_web_inside_json(web_inside_list)
    except ValueError as e:
        print("設定ファイル："+args.web_inside_json+"に以下の問題があります。")
        print(e)
        sys.exit(1)

    # jsonのurlにアクセスする処理
    error_flag = False
    for web_inside in web_inside_list:
        response = requests.get(web_inside["url"])
        # errorがでたら出力
        if response.status_code != web_inside["status"]:
            print("test failed: "+web_inside["description"])
            print("url: "+web_inside["url"])
            print("")
            error_flag = True

    if error_flag == True:
        sys.exit(2)
        
    print("All web inside tests passed")
    sys.exit(0)        

def read_file(file_name):
    """
    read_fileは、引数に指定されたファイルを読み込み、文字列として返す
    """
    l=[]
    with open(file_name) as f:
        l=f.read()
    return l

def make_valid_web_inside_json(web_inside_list):
    """
    make_valid_web_inside_jsonは、ディクショナリのリストを引数として受け取る。
    各ディクショナリにdescription, url, statusのキーがあるか確認し、
    urlとstatusがない場合は、ValueErrorを送出する
    descriptionがない場合は空白のdescriptionを追加する
    """
    for web_inside in web_inside_list:
        if "description" not in web_inside:
            web_inside["description"]=""
        if "url" not in web_inside:
            raise ValueError("リストのすべての要素に'url'が必要です。'url'が無い要素があります。テスト対象のURLを記述するか、その要素を削除してください")
        if "status" not in web_inside:
            raise ValueError("リストのすべての要素に'status'が必要です。'status'が無い要素があります。'url'にアクセスしたときに想定されるステータスコードを要素に必ず含んでください。")

if __name__ == "__main__":
    main()

import sys
import argparse
import json
import zipfile
import tempfile
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
import GithubApi

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

    #jsonのurlにアクセスする処理
        
    sys.exit(0)
    
    # api=GithubApi.GithubApi(args.github_user,args.github_token,args.github_owner,args.github_repos_name)
    
    # try:
    #     api.make_github_secrets("web_inside_json",web_inside_json.replace('"','\\"'))
    #     api.exec_github_actions("exec_web_inside_test")
    # except ValueError as e:
    #     print(e)
    #     sys.exit(1)


    # test_result=""
    # with tempfile.TemporaryDirectory() as tmp:
    #     try:
    #         api.download_github_artifacts(api.work_id,times=10,interval=5,output_dir=tmp)
    #     except ValueError as e:
    #         print(e)
    #         sys.exit(1)
    #     test_result=read_zip(os.path.join(tmp,api.work_id)+".zip","result.txt")
    # error_list=test_result.split()
    # if len(error_list)==0:
    #     print("All web inside tests passed")
    #     sys.exit(0)
    # else:
    #     for i in error_list:
    #         print("test failed: "+web_inside_list[int(i)-1]["description"])
    #         print("url: "+web_inside_list[int(i)-1]["url"])
    #         print("")
    #     sys.exit(2)


# def read_zip(zip_file_name,file_name):
#     """
#     read_zipはzip_file_name内に保存されたfile_nameを読み込み、ファイルの内容を文字列として返します。
#     """
#     content=""
#     with tempfile.TemporaryDirectory() as tmp:
#         with zipfile.ZipFile(zip_file_name) as existing_zip:
#             existing_zip.extract(file_name,os.path.join(tmp,"result"))
#         with open(os.path.join(tmp,"result/result.txt")) as f:
#             content=f.read()
#     return content
        
    
#     pass

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

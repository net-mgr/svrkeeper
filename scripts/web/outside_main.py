import sys
import argparse
import json
import zipfile
import tempfile
import os
import GithubApi

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("github_owner",help="https://api.github.com/repos/{github_owner}/{github_repos_name}/")
	parser.add_argument("github_repos_name",help="https://api.github.com/repos/{github_owner}/{github_repos_name}/")
	parser.add_argument("github_user", help="リポジトリへのアクセス権があるユーザのユーザ名")
	parser.add_argument("github_token", help="github_userが作成したトークン（必要なscope：repo）")
	parser.add_argument("--web-outside-json", help="../config/web_outside.json以外に設定ファイルを置く場合はここにスクリプトからの相対パスを指定",default="../config/web_outside.json")
	args = parser.parse_args()

	try:
		web_outside_json=read_file(args.web_outside_json)
		web_outside_list=json.loads(web_outside_json)
	except FileNotFoundError as e:
		print("ファイル"+args.web_outside_json+"がreadで開けません。設定ファイルを確認してください")
		print("エラーメッセージ："+str(e))
		sys.exit(-1)
	except UnicodeDecodeError as e:
		print("ファイル"+args.web_outside_json+"はUTF-8ではありません。設定ファイルを確認してください")
		print("エラーメッセージ："+str(e))
		sys.exit(-1)
	except json.decoder.JSONDecodeError as e:
		print("ファイル"+args.web_outside_json+"はjson形式ではありません。設定ファイルを確認してください")
		print("parserからのエラーメッセージ："+str(e))
		sys.exit(-1)
	
	# TODO: エラー処理
	make_valid_web_outside_json(web_outside_list)

	api=GithubApi.GithubApi(args.github_user,args.github_token,args.github_owner,args.github_repos_name)
	api.make_github_secrets("web_outside_json",web_outside_json.replace('"','\\"'))

	api.exec_github_actions("exec_web_outside_test")
	
	test_result=""
	with tempfile.TemporaryDirectory() as tmp:
		api.download_github_artifacts(api.work_id,times=10,interval=5,output_dir=tmp)
		test_result=read_zip(os.path.join(tmp,api.work_id)+".zip","result.txt")
	error_list=test_result.split()
	if len(error_list)==0:
		sys.exit(0)
	else:
		for i in error_list:
			print("test failed: "+web_outside_list[int(i)-1]["description"])
			print("url: "+web_outside_list[int(i)-1]["url"])
		sys.exit(1)


def read_zip(zip_file_name,file_name):
	"""
	read_zipはzip_file_name内に保存されたfile_nameを読み込み、ファイルの内容を文字列として返します。
	"""
	content=""
	with tempfile.TemporaryDirectory() as tmp:
		with zipfile.ZipFile(zip_file_name) as existing_zip:
			existing_zip.extract(file_name,os.path.join(tmp,"result"))
		with open(os.path.join(tmp,"result/result.txt")) as f:
			content=f.read()
	return content
		
	
	pass

def read_file(file_name):
	"""
	read_fileは、引数に指定されたファイルを読み込み、文字列として返す
	"""
	l=[]
	with open(file_name) as f:
		l=f.read()
	return l

def make_valid_web_outside_json(web_outside_list):
	"""
	make_valid_web_outside_jsonは、ディクショナリのリストを引数として受け取る。
	各ディクショナリにdescription, url, statusのキーがあるか確認し、
	urlとstatusがない場合は、ValueErrorを送出する
	descriptionがない場合は空白のdescriptionを追加する
	"""
	for web_outside in web_outside_list:
		if "description" not in web_outside:
			web_outside["description"]=""
		if "url" not in web_outside:
			raise ValueError("リストのすべての要素に'url'が必要です。'url'が無い要素があります。テスト対象のURLを記述するか、その要素を削除してください")
		if "status" not in web_outside:
			raise ValueError("リストのすべての要素に'status'が必要です。'status'が無い要素があります。'url'にアクセスしたときに想定されるステータスコードを要素に必ず含んでください。")

if __name__ == "__main__":
	main()

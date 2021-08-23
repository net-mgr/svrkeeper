import requests
from requests.auth import HTTPBasicAuth
import json
from base64 import b64encode
from nacl import encoding, public
import secrets
import string
import time
import os

class GithubApi:
	def __init__(self, github_user, github_token, repos_owner, repos_name):
		self.github_user=github_user
		self.github_token=github_token
		self.repos_owner=repos_owner
		self.repos_name=repos_name
		self.work_id=self.pass_gen()

	@staticmethod
	def pass_gen(size=16):
		"""
		指定された長さの無作為な文字列を作成する。
		"""
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		return ''.join(secrets.choice(chars) for _ in range(size))

	
	@staticmethod
	def encrypt(public_key: str, secret_value: str) -> str:
		"""
		GitHub Secretsを作成する前に暗号化する関数
		Encrypt a Unicode string using the public key.
		URL: https://docs.github.com/ja/rest/reference/actions#create-or-update-a-repository-secret
		"""
		public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
		sealed_box = public.SealedBox(public_key)
		encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
		return b64encode(encrypted).decode("utf-8")

	def make_github_secrets(self,  secrets_name, secrets_value):
		"""
		指定されたレポジトリにSecretを作成する。
		アクセス先：https://api.github.com/repos/{repos_owner}/{repos_name}/actions/secrets
		secrets_name: secretsの名前
		secrets_value: 機密情報
		"""
		base_url="https://api.github.com/repos/"+self.repos_owner+"/"+self.repos_name+"/actions/secrets"		
		headers={'accept': 'application/vnd.github.v3+json'}

		# public keyの取得 TODO: エラー処理
		public_key_request=requests.get(base_url+"/public-key",headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
		public_key=public_key_request.json()
		
		#github secretsの作成　TODO: エラー処理
		data={}
		data["encrypted_value"]=self.encrypt(public_key['key'], secrets_value)
		data["key_id"]=public_key["key_id"]
		secrets_put=requests.put(base_url+"/"+secrets_name, headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token),data=json.dumps(data))

	def exec_github_actions(self, workflows_name):
		"""
		exec_github_actionsは、指定されたgithub actionsを実行します。

		"""
		base_url="https://api.github.com/repos/"+self.repos_owner+"/"+self.repos_name+"/actions/workflows"		
		headers={'accept': 'application/vnd.github.v3+json'}
		list_workflows_request=requests.get(base_url,headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
		list_workflows=list_workflows_request.json()

		# workflows_nameに一致するworkflow_idを見つける
		workflows_id=0
		for workflows in list_workflows["workflows"]:
			if workflows["name"]==workflows_name:
				workflows_id=workflows["id"]
		if workflows_id==0:
			raise ValueError("ワークフロー"+workflows_name+"は存在しません。")
		
		# workflow_idを用いて、dispatch_eventを発生させる(github actionsを実行)
		data={}
		data["ref"]="main"
		data["inputs"]={"artifact_name": self.work_id}
		status_workflow_dispatch=requests.post(base_url+"/"+str(workflows_id)+"/dispatches", headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token),data=json.dumps(data))
		
		if status_workflow_dispatch.status_code!=204:
			raise ValueError("GitHub Actionsを正しく開始することができませんでした。メッセージ："+status_workflow_dispatch.text)

	def download_github_artifacts(self, artifact_name, times=10, interval=5, output_dir="tmp"):
		"""
		interval秒ごとに指定されたartifactのダウンロードを試みる。times回失敗するとエラーを送出する。
		artifactはartifact_nameで指定する。
		"""
		artifact_id=-1
		artifact_url=""
		for _ in range(times):
			time.sleep(interval)
			base_url="https://api.github.com/repos/"+self.repos_owner+"/"+self.repos_name+"/actions/artifacts"		
			headers={'accept': 'application/vnd.github.v3+json'}
			artifact_list_request=requests.get(base_url, headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
			if artifact_list_request.status_code!=200:
				raise ValueError("GitHub artifactsの一覧を取得できません。メッセージ："+artifact_list_request.text)
			artifact_list=artifact_list_request.json()
			for artifact in artifact_list["artifacts"]:
				if artifact["name"]==artifact_name:
					artifact_id=artifact["id"]
					artifact_url=artifact["archive_download_url"]
					break
			if artifact_id!=-1:
				break
		
		if artifact_id==-1:
			raise ValueError("artifact"+artifact_name+"は、ダウンロードできませんでした。")
		
		# artifactのダウンロード
		artifact_request=requests.get(artifact_url,headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
		if artifact_request.status_code!=200:
			raise ValueError("artifacts"+artifact_url+"を取得できません。メッセージ："+artifact_request.text)
		artifact=artifact_request.content
		# artifactの保存
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		with open(output_dir+"/"+artifact_name+".zip",'wb') as f:
			f.write(artifact)
		
		delete_request=requests.delete(base_url+"/"+str(artifact_id),headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
		if delete_request.status_code!=204:
			print("Warn: Artifact deletion fail. Artifact remain.")



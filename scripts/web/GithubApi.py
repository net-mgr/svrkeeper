import requests
from requests.auth import HTTPBasicAuth
import json
from base64 import b64encode
from nacl import encoding, public
class GithubApi:
	def __init__(self, github_user, github_token):
		self.github_user=github_user
		self.github_token=github_token
	
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

	def make_github_secrets(self, repos_owner, repos_name, secrets_name, secrets_value):
		"""
		指定されたレポジトリにSecretを作成する。
		アクセス先：https://api.github.com/repos/{repos_owner}/{repos_name}/actions/secrets
		secrets_name: secretsの名前
		secrets_value: 機密情報
		"""
		base_url="https://api.github.com/repos/"+repos_owner+"/"+repos_name+"/actions/secrets"		
		headers={'accept': 'application/vnd.github.v3+json'}

		# public keyの取得 TODO: エラー処理
		public_key_request=requests.get(base_url+"/public-key",headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token))
		public_key=public_key_request.json()
		
		#github secretsの作成　TODO: エラー処理
		data={}
		data["encrypted_value"]=self.encrypt(public_key['key'], secrets_value)
		data["key_id"]=public_key["key_id"]
		secrets_put=requests.put(base_url+"/"+secrets_name, headers=headers, auth=HTTPBasicAuth(self.github_user, self.github_token),data=json.dumps(data))

		
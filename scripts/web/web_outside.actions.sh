#!/usr/bin/bash
# GitHub Actionsで実行するシェルスクリプト
# web_outside.jsonファイルからjsonを読み込み、
# それぞれのURLにアクセスし、ステータスコードが一致するか確認
# 結果はresult.txtに書き込む

# 区切り文字を改行文字のみに変更
IFS=$'\n'
i=1
for item in $(cat web_outside.json|jq -c '.[]');do
	URL=`echo $item|jq '.url'`
	STATUS=`echo $item|jq '.status'`
	#echo "curl $URL"|bash
	WEB=`echo "curl $URL -o /dev/null -w '%{http_code}' "|bash`
	echo $WEB
	if [ $WEB -ne $STATUS ];then
		echo $i >> result.txt
	fi
	i=$(expr $i + 1)
done

# エラーがなかった場合に空のファイルを作る
touch result.txt

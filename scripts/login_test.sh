#/usr/bin/bash
#
# login に関するテストを実行
# 
# 返り値
# テストで合格または、設定ファイルや環境変数が無くテストを実施しない場合：0
# テスト自体に問題が発生した場合：-1
# テストで不合格: 1
# 

# 2020/2/6 added by Yuuki Okuda
login_test(){
	local num=$1
	local msg=$2
	local expect=$3
	local rsa_key=$4
	local host=$5
	local cmd=$6

	echo "##################################################"
	echo "# Number $num: $msg"
	echo "# Expectation: $expect"
	echo "# Attempting: ssh -p 22 -i $rsa_key $host $cmd"
	ssh -p 22 -i $rsa_key $host $cmd
	local result=$?
	if [ "$expect" = "Login succeed." ]; then
		if [ $result -eq 0 ]; then
			echo -e "=> Passed.\n"
			return 0
		else
			echo -e "=> Failed.\n"
			return 1
		fi
	elif [ "$expect" = "Login failed." ]; then
		if [ $result -eq 0 ]; then
			echo -e "=> Failed.\n"
			return 1
		else
			echo -e "=> Passed.\n"
			return 0
		fi
	fi
}

DIR=$(cd $(dirname $0); pwd)
DIR=$(pwd)

# テストに必要な設定があるか
test_login_exec=1

# test_login.jsonの確認
if [ ! -e $DIR/../config/test_login.env ]; then
  test_login_exec=0
fi

# 設定ファイルがあるテストの実行:
TEST_LOGIN_RESULT=0

if [ $test_login_exec -eq 1 ]; then
  source $DIR/../config/test_login.env
  for((i=1;i<=${NUM_OF_HOSTS};i++)); do
    login_host=HOST${i}
    ssh_key=HOST${i}_SSH_KEY
    msg=TEST_MSG${i}
    expect=EXPECT${i}
    cmd=CMD${i}
    login_test ${i} ${!msg} "${!expect}" ${!ssh_key} ${!login_host} ${!cmd} || TEST_LOGIN_RESULT=1
  done
else
  echo "No login test executed."
fi

exit $TEST_LOGIN_RESULT

exit 0

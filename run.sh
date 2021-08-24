#!/usr/bin/bash

SCRIPTS_DIR=$(cd $(dirname $0); pwd)

# Setting for driving tests
setting_file_sec=${SCRIPTS_DIR}/config/setting.sec.sh
setting_file=${SCRIPTS_DIR}/config/setting.sh

# if setting_file does not exist,
# create it by decrypting setting.sec.sh
if [ ! -e $setting_file ]; then
	read -sp "# Input setting file password: " setting_pass
	tty -s && echo
	openssl enc -d -aes256 -pbkdf2 -in $setting_file_sec -out $setting_file -k $setting_pass
	if [ $? -ne 0 ]; then
		rm -f $setting_file
		echo "# Decryption of 'setting.sec.sh' was failed."
		exit 1
	fi
fi

# include setting.sh
. $setting_file
rm $setting_file

# There is no need to decrypt setting.sec.sh again
#  in mail_test.sh and web_test.sh
export SETTING_FILE_INCLUDED=1

#####################################################################################
# テストの実行 (並列) 。バックグラウンドで実行し、waitで待つ

mkdir -p $SCRIPTS_DIR/results/
$SCRIPTS_DIR/scripts/web_test.sh >$SCRIPTS_DIR/results/web_test.log 2>&1   &
WEB_TEST_PID=$!


wait $WEB_TEST_PID
web_test_passed=$?

#####################################################################################
# テスト結果の出力

all_tests_passed=0 # for checking all tests ware passed. 0:passed, 1: not passed

print_result(){
	local msg=$1
	local passed_flag=$2 # 0 or 1
	echo $msg
	if [ $passed_flag -eq 0 ]; then
		echo "# => All tests were passed."
	elif [ $passed_flag -eq 1 ]; then
		echo "# => Some tests were not passed. Check results."
		all_tests_passed=1
	else
		echo "# => Some tests has error. Check results."
		all_tests_passed=1
	fi
}

echo "##################################################"
echo "# Results of each category"

#print_result "# Category 1: Login test"        $login_test_passed
#print_result "# Category 2: Mail test"         $mail_test_passed
print_result "# Category 3: Web test"          $web_test_passed
#print_result "# Category 4: File editing test" $edit_file_test_passed
#print_result "# Category 5: Backup test"       $backup_test_passed
#print_result "# Category 6: DNS test"          $dns_test_passed
#print_result "# Category 7: Access point test" $access_point_test_passed

echo "##################################################"
print_result "# Total result" $all_tests_passed

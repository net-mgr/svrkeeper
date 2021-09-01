#!/usr/bin/bash

SCRIPTS_DIR=$(cd $(dirname $0); pwd)


# テスト対象を選択
login_test_select=1
mail_test_select=1
web_test_select=1
edit_file_test_select=1
backup_test_select=1
dns_test_select=1
access_point_test_select=1
if [ $# -eq 1 ]; then
	if [ "$1" != "login" ];then
		login_test_select=0
	fi
	if [ "$1" != "mail" ];then
		mail_test_select=0
	fi
	if [ "$1" != "web" ];then
		web_test_select=0
	fi
	if [ "$1" != "edit" ];then
		edit_file_test_select=0
	fi
	if [ "$1" != "backup" ];then
		backup_test_select=0
	fi
	if [ "$1" != "dns" ];then
		dns_test_select=0
	fi
	if [ "$1" != "access" ];then
		access_point_test_select=0
	fi
fi
	

# Setting for driving tests
setting_file_sec=${SCRIPTS_DIR}/config/setting.sec.sh
setting_file=${SCRIPTS_DIR}/config/setting.sh

# if setting_file_sec exist,
# include setting
if [ -e $setting_file_sec ]; then
	read -sp "# Input setting file password: " setting_pass
	tty -s && echo
	openssl enc -d -aes256 -pbkdf2 -in $setting_file_sec -out $setting_file -k $setting_pass
	if [ $? -ne 0 ]; then
		rm -f $setting_file
		echo "# Decryption of 'setting.sec.sh' was failed."
		exit 1
	fi
	# include setting.sh
	. $setting_file
	rm $setting_file
fi



#####################################################################################
# テストの実行 (並列) 。バックグラウンドで実行し、waitで待つ

mkdir -p $SCRIPTS_DIR/results/

if [ $login_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/login_test.sh >$SCRIPTS_DIR/results/login_test.log 2>&1   &
	LOGIN_TEST_PID=$!
fi
if [ $mail_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/mail_test.sh >$SCRIPTS_DIR/results/mail_test.log 2>&1   &
	MAIL_TEST_PID=$!
fi
if [ $web_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/web_test.sh >$SCRIPTS_DIR/results/web_test.log 2>&1   &
	WEB_TEST_PID=$!
fi
if [ $edit_file_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/edit_file_test.sh >$SCRIPTS_DIR/results/edit_file_test.log 2>&1   &
	EDIT_TEST_PID=$!
fi
if [ $backup_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/backup_test.sh >$SCRIPTS_DIR/results/backup_test.log 2>&1   &
	BACKUP_TEST_PID=$!
fi
if [ $dns_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/dns_test.sh >$SCRIPTS_DIR/results/dns_test.log 2>&1   &
	DNS_TEST_PID=$!
fi
if [ $access_point_test_select -eq 1 ];then
	$SCRIPTS_DIR/scripts/access_point_test.sh >$SCRIPTS_DIR/results/access_point_test.log 2>&1   &
	ACCESS_TEST_PID=$!
fi


if [ $login_test_select -eq 1 ];then
	wait $LOGIN_TEST_PID
	login_test_passed=$?
fi
if [ $mail_test_select -eq 1 ];then
	wait $MAIL_TEST_PID
	mail_test_passed=$?
fi
if [ $web_test_select -eq 1 ];then
	wait $WEB_TEST_PID
	web_test_passed=$?
fi
if [ $edit_file_test_select -eq 1 ];then
	wait $EDIT_TEST_PID
	edit_file_test_passed=$?
fi
if [ $backup_test_select -eq 1 ];then
	wait $BACKUP_TEST_PID
	backup_test_passed=$?
fi
if [ $dns_test_select -eq 1 ];then
	wait $DNS_TEST_PID
	dns_test_passed=$?
fi
if [ $access_point_test_select -eq 1 ];then
	wait $ACCESS_TEST_PID
	access_point_test_passed=$?
fi
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

if [ $login_test_select -eq 1 ];then
	print_result "# Category 1: Login test"        $login_test_passed
fi
if [ $mail_test_select -eq 1 ];then
	print_result "# Category 2: Mail test"         $mail_test_passed
fi
if [ $web_test_select -eq 1 ];then
	print_result "# Category 3: Web test"          $web_test_passed
fi
if [ $edit_file_test_select -eq 1 ];then
	print_result "# Category 4: File editing test" $edit_file_test_passed
fi
if [ $backup_test_select -eq 1 ];then
	print_result "# Category 5: Backup test"       $backup_test_passed
fi
if [ $dns_test_select -eq 1 ];then
	print_result "# Category 6: DNS test"          $dns_test_passed
fi
if [ $access_point_test_select -eq 1 ];then
	print_result "# Category 7: Access point test" $access_point_test_passed
fi

echo "##################################################"
print_result "# Total result" $all_tests_passed

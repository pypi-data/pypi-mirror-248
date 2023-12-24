#!/bin/bash

git_bases=`find . -name .git`
#echo $git_bases

git_dirs=(${git_bases//.git/ })
repo="repo"
cmd=""

function help() {
	echo "eg: pyoc \"your command\""
	echo "    pyoc forall \"components/av components/av_cp\" \"your command\""
}

#for git_dir in ${git_dirs[@]}
#do
#	cd $git_dir
#	if [ -n "$(git status -s)" ];then
#	    #git add .
#	    git ci -a -m "update cpu usage"
#	    git push origin HEAD:refs/for/v7.4.y/ps
#	fi
#	cd - >/dev/null 2>&1
#done
#exit 0

if [[ $# -lt 1 ]]; then
	help
	exit 0
fi

if [[ $1 == "forall" ]]; then
	if [[ $# != 3 ]]; then
		help
		exit 0
	fi
	git_bases=$2
	git_dirs=(${git_bases// / })
	cmd=$3
else
	cmd=$1
fi

for git_dir in ${git_dirs[@]}
do
	if [[ "$git_dir" == *$repo* ]]; then
		echo "skip repo"
	else
		echo $git_dir
		cd $git_dir
		eval $cmd
		cd - >/dev/null 2>&1
	fi
done


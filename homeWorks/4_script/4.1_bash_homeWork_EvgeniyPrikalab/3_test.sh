#!/usr/bin/env bash

array_ip=("192.168.0.1" "173.194.222.113" "87.250.250.242")
port=80

for i in ${array_ip[@]}
do
	a=5
	while (($a > 0))
	do
	curl $i:$port
	echo $i $? >> curl.log
	let a-=1
	done
done
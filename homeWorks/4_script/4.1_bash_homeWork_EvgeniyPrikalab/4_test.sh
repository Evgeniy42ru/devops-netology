#!/usr/bin/env bash

array_ip=("192.168.0.1" "173.194.222.113" "87.250.250.242")
port=80
repeat=1

while (($repeat==1))
do
	for i in ${array_ip[@]}
	do
		a=5
		while (($a > 0 && $repeat==1))
		do
		curl $i:$port
		if (($? == 0))
		then
			echo $i $? >> curl.log
			let a-=1
		else
			echo $i $? >> error.log
			repeat=0
			a=0
		fi		
		done
		
	done
done
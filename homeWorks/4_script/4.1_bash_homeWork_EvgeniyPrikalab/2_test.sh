#!/usr/bin/env bash

while ((1==1))
do
	curl https://vk.com:443
	if (($? != 0))
	then
		date >> curl.log
                else
                                exit
	fi
done
#! /bin/bash

function start_server(){
	CDIR=$(pwd)
	cd TablutCompetition/Tablut
	#ant server &
	ant server &
	cd "$CDIR"
	sleep 3
}

function start_player(){
	ROLE=$1
	TIME=$2
	SERVER=$3
	termite -e "bash -c \"python src/client.py $ROLE $TIME $SERVER ; bash\"" &
	sleep 1
}

start_server
start_player WHITE 60 localhost
# start_player BLACK 60 localhost



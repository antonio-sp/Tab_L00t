#! /bin/bash

PROJECTS="~/Downloads/old_projects"
TIMEOUT=60
SERVER_IP=127.0.0.1
SERVER_DIR="~/Downloads/TablutCompetition/Tablut"
MYLAUNCHER=${1:-~/Documents/projects/Tab_L00t/src/launch.sh}

MYROLE=${2:-W}
OPPONENT_ROLE=$(echo WB | tr -d $MYROLE)

function compile_server(){
	OLD_CWD=$(pwd)
	cd $SERVER_DIR
	ant clean
	ant compile
	cd "$OLD_CWD"
}

function start_server(){
	OLD_CWD=$(pwd)
	cd $SERVER_DIR
	ant server
	cd "$OLD_CWD"
}

rm    wins.txt fails.txt
touch wins.txt fails.txt

compile_server
for DIR in "$PROJECTS/"*; do
	if [ -d "$DIR" -a -f "$DIR/launch.sh" ]; then
		start_server &
		$DIR/launch.sh $OPPONENT_ROLE $TIMEOUT $SERVER_IPA &
		$MYLAUNCHER    $OPPONENT_ROLE $TIMEOUT $SERVER_IP 2>&1 \
			| grep -q 'YOU WIN' && echo $DIR >> wins.txt \
								|| echo $DIR >> fails.txt
	fi
done

WINS=$(wc -l wins.txt)
FAILS=$(wc -l fails.txt)
GAMES=$((WINS + FAILS))

echo "WINS  = $WINS	$((GAMES / 100 * WINS))"
echo "FAILS = $FAILS	$((GAMES / 100 * FAILS))"


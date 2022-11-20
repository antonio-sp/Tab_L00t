#! /bin/sh

[ $USER == 'robi' ]    && TERMINAL="termite -e"
[ $USER == 'andry' ]   && TERMINAL="konsole -e"
[ $USER == 'antonio' ] && TERMINAL="konsole -e"


cd ..
DIR=$(pwd)

[ ! -d TablutCompetition ] \
	&& git clone https://github.com/AGalassi/TablutCompetition

cd TablutCompetition/Tablut
ant clean
ant compile
ant server &
sleep 2
cd "$DIR"
# TODO: my player vs others...
$TERMINAL "bash -c \"$DIR/src/client.py white 60 127.0.0.1 ; bash\"" &
$TERMINAL "bash -c \"$DIR/src/client.py black 60 127.0.0.1 ; bash\"" &

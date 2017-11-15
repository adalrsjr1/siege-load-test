#!/usr/bin/env bash

#CONCURRENT=${CONCURRENT:-1}
#REPS=${REPS:-1}
#SERVER=${SERVER:-10.66.66.32:30001}
#DELAY=${DELAY:-1}

CONCURRENT=$1
REPS=$2
SERVER=$3
DELAY=$4

curl -s -c cookies.txt -H 'Authorization: Basic dXNlcjpwYXNzd29yZA==' \
  $SERVER/login > /dev/null

logdn=$(cat cookies.txt | tail -n 2 | head -n 1 | awk '{print $6"="$7}')
mdsid=$(cat cookies.txt | tail -n 1 | awk '{print $6"="$7}')
cookie="Cookie: $logdn; $mdsid"

siege -c $CONCURRENT -r $REPS $OPTS -d $DELAY\
  -H "$cookie" \
  "http://$SERVER/orders POST {}"

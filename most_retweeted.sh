#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 twits_file" >&2
  exit 1
fi

if ! [ -e "$1" ]; then
  echo "$1 not found" >&2
  exit 1
fi

cat $1 | grep retweeted_status | py -x --ji "'@' + x['retweeted_status']['user']['screen_name'] + ': ' + x['retweeted_status']['text']" | sort | uniq -c | sort -nr | head -n10

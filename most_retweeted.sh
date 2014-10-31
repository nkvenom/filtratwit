#!/bin/bash
cat $1 | grep retweeted_status | py -x --ji "'@' + x['retweeted_status']['user']['screen_name'] + ': ' + x['retweeted_status']['text']" | sort | uniq -c | sort -nr | head -n10
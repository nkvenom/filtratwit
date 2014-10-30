#!/bin/bash

cat  $1  | head -n-1 |
py --ji -x "x['text']" |
./emoji_names -s '\n' | 
sort | uniq -c | sort -nr | head -n11

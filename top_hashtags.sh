#!/bin/bash

cat  $1  | head -n-1 |
py --ji -x "x['text']" |
py -x "x if '#' in x else None" | 
py -x "'\n'.join([j.lower() for j in x.split() if j.startswith('#')])" | 
py -x "'#'+''.join(ch for ch in x if ch.isalnum())" | 
sort | uniq -c | sort -nr

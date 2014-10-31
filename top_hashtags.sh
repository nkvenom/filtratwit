#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 twits_file" >&2
  exit 1
fi

if ! [ -e "$1" ]; then
  echo "$1 not found" >&2
  exit 1
fi

cat  $1  | head -n-1 |
py --ji -x "x['text']" |
py -x "x if '#' in x else None" | 
py -x "'\n'.join([j.lower() for j in x.split() if j.startswith('#')])" | 
py -x "'#'+''.join(ch for ch in x if ch.isalnum())" | 
sort | uniq -c | sort -nr | head -n11

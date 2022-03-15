#!/bin/bash
index=$3

for old in `ls -F $1 | grep -v /`; do
  index=$(expr $index + 1)
  in="$1/$old"
  out="$2/$(printf "%03d\n" "${index}").jpeg"
  echo "mv $in $out"
  mv $in $out
done

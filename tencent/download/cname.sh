#!/bin/bash
index=$3

filecount=`ls -F $1 | grep -v / | wc -l`
if [ ${filecount} -gt 10 ] ; then
  echo "filecount is large than 10"
  mkdir $1/temp
  mv $1/0\([1-9][0-9]\) $1/temp
fi

for old in `ls -F $1 | grep -v /`; do
  index=$(expr $index + 1)
  in="$1/$old"
  out="$2/$(printf "%03d\n" "${index}").jpg"
  echo "mv $in $out"
  mv $in $out
done

if [ ${filecount} -gt 10 ] ; then
  for old in `ls -F $1/temp | grep -v /`; do
    index=$(expr $index + 1)
    in="$1/temp/$old"
    out="$2/$(printf "%03d\n" "${index}").jpg"
    echo "mv $in $out"
    mv $in $out
  done
  rm $1/temp -rf
fi
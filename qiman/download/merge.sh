#!/bin/bash

dst=$1
fileCount=0
for loop in {0..4}
do
  src=$(expr $dst + $loop)
  echo  "./cname.sh $src $dst $fileCount"
  ./cname.sh $src $dst $fileCount
  fileCount=`ls $dst|wc -l`
  srcCount=`ls $src|wc -l`
  if [ $srcCount -eq 0 ]; then
    echo "rm $src -rf"
    rm $src -rf
  fi
done
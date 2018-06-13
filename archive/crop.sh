#!/bin/bash
base=$1

l=`identify -format "%w %h" $base`
f=${base%.*}
e=${base##*.}

set -- $l
width=$1
height=$2

if test $height -lt $width; then
    n=$(($width/2))
    convert -crop $n"x"$height+$n+0 "$base" crop/$f"-0."$e
    convert -crop $n"x"$height+0+0 "$base" crop/$f"-1."$e
else
    cp $base crop/
fi

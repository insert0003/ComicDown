#!/bin/bash
index=221
for old in `ls -d */`; do
echo $old
new=${old:5:3}
mv $old $new
done


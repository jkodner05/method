#!/bin/bash

for file in cocasamples/*.txt
do
   grep -P "ing\t" "$file" > singsang/"$(basename $file)"
done

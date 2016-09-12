#!/usr/bin/env bash

find images/ -type f|grep -iE jpg|while read fname
do
  echo "loading $fname"
  curl -T "$fname" "http://localhost:8080/$fname"

done

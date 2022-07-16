#!/bin/bash

zgrep -E "^/type/(?:edition|work)" "$1" | pv | gzip > "filtered_$1"
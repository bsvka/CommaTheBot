#!/bin/bash

sort "$1" | uniq --count | sort -nr > "$1.sorted"
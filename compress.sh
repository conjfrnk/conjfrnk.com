#!/usr/local/bin/bash

gzip -9fk style.css
gzip -9fk *.html
find assets/ -type f -not -name "*.gz" -exec gzip -5fk "{}" \;

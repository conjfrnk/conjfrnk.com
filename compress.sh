#!/usr/local/bin/bash

gzip -5fk style.css
gzip -5fk euler/euler.css

gzip -7fk *.html
gzip -7fk euler/*.html
gzip -7fk reading/*.html

find assets/ -type f -not -name "*.gz" -exec gzip -4fk "{}" \;

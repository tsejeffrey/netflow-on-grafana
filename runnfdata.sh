#!/bin/sh

last=$(date +%Y/%m/%d.%H)
nfdump  -R /var/cache/nfdump/ -B -6 -s record/bytes -n 50 -o json -t $last | egrep "{|}|_port|_addr|in_bytes" | sed  '/bytes/s/\,//' | sed 's/src[46]/src/' | sed 's/}/},/' | sed '1s/{/[{/;$s/\,/]/' | sed 's/{/[/;s/}/]/' | sed 's/.*\:\ //' > outf.json
/root/js-lab1/graconvert.py outf.json nf.json series.json

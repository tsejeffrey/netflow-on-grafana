#!/usr/bin/python
import json
import sys
import time
import subprocess
def processdata(nfout_path):
    data = []
    rows = {}
    throughput = 0
    with open(nfout_path, 'r') as outf:
            data = json.load(outf)
    x = 0
    for i in data:
        if len(i) == 3:
            data[x].insert(2,0)
            data[x].insert(2,0)
        throughput += i[4]
        print data[x][0]
        ori = findIPinfo(data[x][0])
        data[x].insert(1,ori[-1])
        data[x].insert(1,ori[-2])
        data[x].insert(1,ori[-3])
        data[x].insert(1,ori[-4])
        print data[x][5]
        ori = findIPinfo(data[x][5])
        data[x].insert(6,ori[-1])
        data[x].insert(6,ori[-2])
        data[x].insert(6,ori[-3])
        data[x].insert(6,ori[-4])
        print data[x]
        x += 1
    rows['rows'] = data
    createtable(rows)
    createthroughput(throughput)
def findIPinfo(ip):
     cmd = "curl https://json.geoiplookup.io/" + ip  + " | jq \".org, .country_name, .city, .asn_number\""
     ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
     ori = ps.communicate()[0].splitlines()
     return ori

def createtable(rows):
    table = {}
    table['columns'] = [ {'text': 'SrcIP', 'type': 'string'}, {'text': 'SrcOrigin', 'type': 'string'}, {'text': 'SrcCity', 'type': 'string'}, {'text': 'SrcCountry', 'type': 'string'}, {'text': 'SrcASN', 'type': 'number'}, {'text': 'DstIP', 'type': 'string'}, {'text': 'DstOrigin', 'type': 'string'},{'text': 'DstCity', 'type': 'string'}, {'text': 'DstCountry', 'type': 'string'}, {'text': 'DstASN', 'type': 'number'}, {'text': 'SrcPort', 'type': 'string'}, {'text': 'DstPort', 'type': 'string'}, {'text': 'Bytes', 'type': 'number'}]
    table.update(rows)
    with open(json_path, 'w') as jsonf:
        jsonf.write(json.dumps(table, indent=4))

def createthroughput(throughput):
    current = int(time.time()) * 1000
    datapoints = {}
    current_stat = [ throughput, current]
  #  f = open(series_path)
  #  data = json.load(f)
  #  f.close()
    with open(series_path, 'r') as lf:
        data = json.load(lf)
    for target in data:
        if target['target'] == 'throughput':
            target['datapoints'].append(current_stat)
    with open(series_path, 'w') as df:
        json.dump(data, df)

series_path = sys.argv[3]
json_path = sys.argv[2]
nfout_path = sys.argv[1]
processdata(nfout_path)

#!/usr/bin/python
# @author: Colan Biemer

import json

file = "test.json"

f = open(file, 'r')
data = json.loads(f.readlines()[0])
f.close()

start = "startTime"
end   = "endTime"

time = 0
for d in data['data']:
	time += float(d[end]) - float(d[start])
	print(float(d[end]) - float(d[start]), time)


print("totalTime: ",  time / 1000)
print("average:", (time / 1000) / len(data['data']))
print("expected:", len(data['data']) * 2.0)
# coding:utf-8
import subprocess

body = ""
false = "false"
obj = subprocess.Popen(("curl -sXGET http://192.168.2.101:9200/_cluster/health?pretty=true"),shell=True,stdout=subprocess.PIPE)
result = obj.stdout.read()
data = eval(result)
elk_status = data.get('status')

if elk_status == 'green':
	print "正常"
else:
	print "异常"
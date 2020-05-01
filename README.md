# my-elk

##### elasticsearch6.6.0 + elasticsearch-head +  logstash6.6.0 + kibana6.6.0 + filebeat-6.6.0 + nginx + redis5+ tomcat + mysql

##### https://www.elastic.co/guide/index.html

##### software: https://pan.baidu.com/s/1JN0pDRfhRuGSxl767b9bOQ       3llm

##### 192.168.2.103  node.name: node-101

##### 192.168.2.104   node.name: node-104

### 1. jdk installation

```json
# https://pan.baidu.com/s/1UrMBBD_08YArZwahLzDp_w  bri8 
yum install jdk-8u241-linux-x64.rpm -y
vim /etc/profile
	export JAVA_HOME=/usr/java/jdk1.8.0_241-amd64/
	export JRE_HOME=$JAVA_HOME/jre
	export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
	export PATH=$JAVA_HOME/bin:$PATH
source /etc/profile

 # update time
  yum install ntpdate -y
  ntpdate time1.aliyun.com
```

### 2. elasticsearch6.6.0 installation

```json
yum install elasticsearch-6.6.0.rpm -y
# configuration
vim /etc/elasticsearch/elasticsearch.yml
	cluster.name: elk-cluster1
    node.name: elk-node-1
	# node.name: elk-node-2
    path.data: /var/lib/elasticsearch
    path.logs: /var/log/elasticsearch
    network.host: 192.168.2.104
    http.port: 9200
	discovery.zen.ping.unicast.hosts: ["192.168.2.104", "192.168.2.101"]
     
    # write in the end
	http.cors.enabled: true 
	http.cors.allow-origin: "*"

vim /etc/elasticsearch/jvm.options
    -Xms512m
    -Xmx512m
systemctl daemon-reload
systemctl enable elasticsearch.service
systemctl start elasticsearch.service

# test is success
netstat -lntup|grep 9200

curl 192.168.2.104:9200
{
  "name" : "node-1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "PPzevLOiT769QFVgv6Bkug",
  "version" : {
    "number" : "6.6.0",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "a9861f4",
    "build_date" : "2019-01-24T11:27:09.439740Z",
    "build_snapshot" : false,
    "lucene_version" : "7.6.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}

```

### 3. node/npm installation

```json
wget https://nodejs.org/dist/v10.13.0/node-v10.13.0-linux-x64.tar.xz
xz -d node-v10.13.0-linux-x64.tar.xz
tar -xf node-v10.13.0-linux-x64.tar
ln -s ~/node-v10.13.0-linux-x64/bin/node /usr/bin/node
ln -s ~/node-v10.13.0-linux-x64/bin/npm /usr/bin/npm
node -v
npm -v
npm install -g cnpm --registry=https://registry.npm.taobao.org
ln -s /usr/local/node-v10.13.0-linux-x64/bin/cnpm /usr/bin/cnpm
```

### 4.  elasticsearch-head installation

```json
git://github.com/mobz/elasticsearch-head.git
unzip elasticsearch-head-master.zip
mv elasticsearch-head-master ./elasticsearch-head
cd elasticsearch-head
npm install grunt -save
npm install 
npm run start &

```

### 5.  re_modify elasticsearch.yml

```json
# append config in the end
http.cors.enabled: true 
http.cors.allow-origin: "*"

systemctl restart elasticsearch.service
```

### 6. tips of elasticsearch start failed

```json
https://www.elastic.co/guide/en/elasticsearch/reference/6.4/setup-configuration-memory.html
https://www.elastic.co/guide/en/elasticsearch/reference/6.4/setting-system-settings.html#sysconfig

vim /usr/lib/systemd/system/elasticsearch.service
### append config
[Service]
LimitMEMLOCK=infinity
### restart
systemctl daemon-reload
systemctl restart elasticsearch
```

### 7.  查看集群状态信息

```json
curl -- sXGET http://192.168.2.101:9200/_cluster/health?pretty=true

# result is below
curl: (6) Could not resolve host: sXGET; Name or service not known
{
  "cluster_name" : "elk-cluster1",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 2,
  "number_of_data_nodes" : 2,
  "active_primary_shards" : 5,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

```

### 8. 

```json

```

### 9. 

```json

```

### 10. 

```json

```

### 11. 

```json

```

### 12. 

```json

```

### 13. 

```json

```

### 14. 

```json

```

### 15. 

```json

```

### 16. 

```json

```

### 17. 

```json

```

### 18. 

```json

```

### 19. 

```json

```

### 20. 

```json
# jsonify nginx-access-log to json format
log_format main '{ 
        "time_local": "$time_local", '
        '"remote_addr": "$remote_addr", '
        '"referer": "$http_referer", '
        '"request": "$request", '
        '"status": $status, '
        '"bytes": $body_bytes_sent, '
        '"agent": "$http_user_agent", '
        '"x_forwarded": "$http_x_forwarded_for", '
        '"up_addr": "$upstream_addr",'
        '"up_host": "$upstream_http_host",'
        '"upstream_time": "$upstream_response_time",'
        '"request_time": "$request_time"'
  ' }';
access_log  logs/access.log  main;
```

### 21. 

```json

```

### 22. 

```json

```

### 23. 

```json

```

### 24. 

```json

```

### 25. 

```json

```

### 26. 

```json

```

### 27. 

```json

```

### 28. 

```json

```

### 29. 

```json

```

### 30. 

```json

```

### 31. 

```json

```

### 32. 

```json

```












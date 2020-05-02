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

### 8. elk_status monitor python script

```python
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
```

### 9.  logstash installation & collect systemlog

```json
# on 192.168.2.104
yum install logstash-6.6.0.rpm -y 
# /usr/share/logstash/bin/logstash --help
# collect system log
vim /etc/logstash/conf.d/systemlog.conf
input {
  file {
     type => "systemlog-104"
     path => "/var/log/messages"
     start_position => "beginning"
     stat_interval => "3"
   }
}

output {
   elasticsearch {
     hosts => ["192.168.2.101:9200"]
     index => "logstash-system-log-104-%{+YYYY.MM.dd}"
  }
   file {
     path => "/tmp/123.txt"
  }
}

# test config file
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/systemlog.conf -t
# chmod 644 /var/log/logstash/
systemctl start loggstash
```

### 10. kibana installation

```json
# on 192.168.2.101
yum install kibana-6.6.0-x86_64.rpm -y
vim /etc/kibana/kibana.yml
    server.port: 5601
    server.host: "192.168.2.101"
    elasticsearch.hosts: ["http://192.168.2.104:9200"]

systemctl start kibana

http://192.168.2.101:5601/
Management->Index Patterns->create Index
```

### 11.  nginx installation & proxy kibana

```json
# on 192.168.2.101
# yum install pcre openssl openssl-devel zlib zlib-devel pcre-devel
wget http://nginx.org/download/nginx-1.15.12.tar.gz
tar zxvf nginx-1.15.12.tar.gz
cd nginx-1.15.12
./configure --prefix=/usr/local/nginx --with-http_sub_module --with-http_ssl_module 
make & make install

# vim /usr/local/nginx//conf/nginx.conf
	 worker_processes  auto; # CPU
# mkdir /usr/local/nginx/conf/conf.d
	include /usr/local/nginx/conf/conf.d/*.conf;

# add 127.0.0.0 proxy kibana
vim usr/local/nginx/conf/conf.d/kibana101.conf;
upstream kibana_server {
   server 127.0.0.1:5601 weight=1 max_fails=3 fail_timeout=60;
}

server {
   listen 80;
   server_name www.kibana101.com;
   auth_basic "Restricted Access";
   auth_basic_user_file /usr/local/nginx/htppass.txt;
   
   location / {
       proxy_pass http://kibana_server;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection 'upgrade';
       proxy_set_header Host $host;
       proxy_cache_bypass $http_upgrade;
   }
}


# yum install httpd-tools
# add kibana user and password auth
htpasswd -bc /usr/local/nginx/htppass.txt kibana 123456
#
```

### 12.  jsonify nginx log

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

#--------------------------------------------------------------------------

log_format access_json '{
    "@timestamp":"$time_iso8601",'
    '"host":"$server_addr"',
    '"clientip":"$remote_addr"',
    '"size":$body_bytes_sent',
    '"responsetime":$request_time',
    '"upstreamtime":"$upstream_response_time"',
    '"upstreamhost":"$upstream_addr"',
    '"http_host":"$host"',
    '"url":"$uri"',
    '"domain":"$host"',
    '"xff":"$http_x_forwarded_for"',
    '"referer":"$http_referer"',
    '"status":"$status"'
}';
access_log  /var/log/nginx/access.log  access_json;
```

### 13. collect ngixn log

```json
# on  192.168.2.101
yum install logstash-6.6.0.rpm -y
vim /etc/logstash/conf.d/nginx.conf
input {
    file {
       path => "/usr/local/nginx/logs/access.log"
       type => "nginx-access-log-101"
       start_position => "beginning"
       stat_interval => "5"
       codec => "json"
	}
    file {
       path => "/var/log/messages"
       type => "system-log-101"
       start_position => "beginning"
       stat_interval => "5" 
    }
}

output {
    if [type] == "nginx-access-log-101" {
        elasticsearch {
             hosts => ["192.168.2.101:9200"]
			 index => "logstash-nginx-accesslog-101-%{+YYYY.MM.dd}"
    	}
    }
    if [type] == "system-log-101" {
        elasticsearch {
             hosts => ["192.168.2.101:9200"]
             index => "logstash-system-log-101-%{+YYYY.MM.dd}"
   	    }
    }
}

# test config file
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/nginx.conf -t
systemctl start logstash

# add nginx-access-log-101 to kibana
```

### 14.  tomcat installation

```json
# 192.168.2.101
# yum install tomcat tomcat-webapps tomcat-admin-webapps tomcat-docs-webapp tomcat-javadoc -y
# /apps
wget https://mirror.bit.edu.cn/apache/tomcat/tomcat-7/v7.0.103/bin/apache-tomcat-7.0.103.zip
apache-tomcat-7.0.103.zip
ln -sv /apps/apache-tomcat-7.0.103 /apps/tomcat
chmod a+x ./bin/*.sh
./bin/catalina.sh start
# ./bin/startup.sh
./bin/shutdown.sh
```

### 15. jsonify tomcat log

```json
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" prefix="localhost_access_log." suffix=".txt"
pattern="{&quot;clientip&quot;:&quot;%h&quot;,&quot;ClientUser&quot;:&quot;%l&quot;,&quot;authenticated&quot;:&quot;%u&quot;,&quot;AccessTime&quot;:&quot;%t&quot;,&quot;method&quot;:&quot;%r&quot;,&quot;status&quot;:&quot;%s&quot;,&quot;SendBytes&quot;:&quot;%b&quot;,&quot;Query?string&quot;:&quot;%q&quot;,&quot;partner&quot;:&quot;%{Referer}i&quot;,&quot;AgentVersion&quot;:&quot;%{User-Agent}i&quot;}"/>
```

### 16. add tomcat log to logstash

```json

input {
    file {
      path => "/apps/tomcat/logs/tomcat_access_log.*.log"
      type => "tomcat-access-log-101"
      start_position => "beginning"
      stat_interval => "2"
      codec => "json"
   }
}

output {
    elasticsearch {
       hosts => ["192.168.2.101:9200"]
       index => "logstash-tomcat-access-log-101-%{++YYYY.MM.dd}"
    }
    file {
        path => "/tmp/tomcat.txt"
    }
}
```

### 17. mariadb installation

```json
yum install mariadb-server
systemctl enable mariadb
systemctl start mariadb
grant all privileges on elk.* to  elk@'%' identified by '123456';
FLUSH PRIVILEGES;


# mysql-connnect-java
https://dev.mysql.com/downloads/connector

mkdir -pv /usr/share/logstash/vendor/jar/jbdc
# mysql-connector-java-5.1.45.tar.gz
tar -xvf mysql-connector-java-5.1.45.tar.gz
cd mysql-connector-java-5.1.45
mv mysql-connector-java-5.1.45/mysql-connector-java-5.1.45-bin.jar  /usr/share/logstash/vendor/jar/jbdc


/usr/share/logstash/bin/logstash-plugin list


input {
    file {
       path => "/usr/local/nginx/logs/access.log"
       type => "nginx-access-log-101"
       start_position => "beginning"
       stat_interval => "5"
       codec => "json"
	}
    file {
       path => "/var/log/messages"
       type => "system-log-101"
       start_position => "beginning"
       stat_interval => "5" 
    }
}

output {
    if [type] == "nginx-access-log-101" {
        elasticsearch {
             hosts => ["192.168.2.101:9200"]
			 index => "logstash-nginx-accesslog-101-%{+YYYY.MM.dd}"
    	}
		file {
            path => "/tmp/nginx-json-log.txt"
        }
		jdbc {
            connection_string => "jdbc:mysql://192.168.2.101/elk/?user=elk&password=123456&useUnicode=true&characterEncoding=UTF8"
            statement => ["insert into elklog(host,url,clienip,responsetime,upstreamtime) values(?,?,?,?,?)","host","url","clientip","responsetime","upstreamtime"]
        }
    }
    
}
```

### 18. 

```json

```

### 19. 

```json

```

### 20. 

```json


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












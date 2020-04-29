# my-elk

##### elasticsearch6.6.0 + elasticsearch-head +  logstash7.6.2 + kibana7.6.2 + nginx + redis5+ tomcat + mysql

### 1. elasticsearch installation

```json

```

### 2. 

```json

```

### 3. 

```json

```

### 4. 

```json

```

### 5. 

```json

```

### 6. 

```json

```

### 7. 

```json

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
# 修改nginx日志json格式

log_format main '{ "time_local": "$time_local", '
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












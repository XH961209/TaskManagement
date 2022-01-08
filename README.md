# TaskManagement
## 环境
python3.8
## 怎样运行系统并通过rest api进行调用？
### 1 下载、安装、运行redis和kafka
#### redis
redis下载链接:  
https://download.redis.io/releases/redis-6.2.6.tar.gz  
下载后，运行以下命令解压:  
`tar -zxvf redis-6.2.6.tar.gz`  
解压后进入redis-6.2.6目录，执行以下命令编译:  
`make`  
编译完成后，执行以下命令验证编译是否成功:  
`make test`  
验证成功后，执行以下命令运行redis:  
`./src/redis-server ./redis.conf`  
#### kafka
kafka下载链接:  
https://www.apache.org/dyn/closer.cgi?path=/kafka/3.0.0/kafka_2.13-3.0.0.tgz  
下载后，运行以下命令解压:  
`tar -zxvf kafka_2.13-3.0.0.tgz`  
解压后进入kafka_2.13-3.0.0目录，先运行zookeeper:  
`./bin/zookeeper-server-start.sh`  
再启动kafka server:  
`./bin/kafka-server-start.sh`
### 2 运行任务管理系统
任务管理系统不需要下发Topic，只需要接受Topic即可。
#### 运行员工管理系统
拉下员工管理系统的代码之后，执行以下命令以运行系统:  
`python task.py`  
#### 通过rest api调用任务管理系统的任务统计报表功能
`curl -i -H "Content-Type: application/json" -X POST http://127.0.0.1:5002/task/api/get_report`

该api调用会查询获取部门任务完成情况统计报表

若用户不存在，会提示`该用户不存在！`；若密码错误，会提示`密码错误！`；登录成功会提示`登录成功！`。

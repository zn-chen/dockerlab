# Docker连接器需求文档

**DockerLab：** v2.0

统一返回数据类型格式：

```
{
  "meta": {
    "code": 200, //200为返回请求正常，503请求超时
    "message": "错误信息"
  }, 
  "data": {
 	//返回数据内容
  }
}
```

## 容器相关

### POST /contianer/{contianerId}

- [ ] **创建虚拟机实验环境（设置默认销毁时间，限制内存和CPU使用上限）**

  传入参数示例：

  ```
   {
       "option":"create"
       "params": {
       		"imageList":["webgoat/webgoat-8.0:latest","dvwa:latest"]
        }
   }
  ```

  返回容器信息相关数据，示例：

  ```
  {
    //返回头信息已在文档起始处说明，此处不再赘述，以下为所需的返回数据内容
    "data": {
      "containerId": "d8001a2c7e5b",
      "hostIP": "101.71.29.5",
      "username": "admin",//WEB服务无需返回账号密码
      "password": "12345678",//随机密码
      "containerPort": {
         {
           "HostIp": "101.71.29.5",
           "HostPort": "32771"
         }
      }
      "destroyTime": 1545481374
      "contianerState":runnig|created|deleted
    }
  }
  ```

- [ ] **启动容器**

  传入参数示例：

  ```
    {
      "operation": "start" ,
       "params": {
        }
    }
  ```

  返回信息：

  ```
   {
      //返回头信息已在文档起始处说明，此处不再赘述，以下为所需的返回数据内容
      "data": {
      "containerId": "d8001a2c7e5b",
      "hostIP": "101.71.29.5",
      "username": "admin",//WEB服务无需返回账号密码
      "password": "12345678",//随机密码
      "containerPort": {
         {
           "HostIp": "101.71.29.5",
           "HostPort": "32771"
         }
      }
      "destroyTime": 1545481374
      "contianerState":runnig|created|deleted
    }
    }
  ```
- [ ] 删除容器

  ```
   {
       "option":"delete"
       "params": {
        }
   }
  ```

  ```
    {
      //省略返回头信息
      "data": {
      "containerId": "d8001a2c7e5b",
      "hostIP": "101.71.29.5",
      "username": "admin",//WEB服务无需返回账号密码
      "password": "12345678",//随机密码
      "containerPort": {
         {
           "HostIp": "101.71.29.5",
           "HostPort": "32771"
         }
      }
      "destroyTime": 1545481374
      "contianerState":runnig|created|deleted
    }
  ```

- [ ] 查询容器信息

  ```
   {
       "option":"query"
       "params": {
        }
   }
  ```

  ```
    {
      //省略返回头信息
      "data": {
      "containerId": "d8001a2c7e5b",
      "hostIP": "101.71.29.5",
      "username": "admin",//WEB服务无需返回账号密码
      "password": "12345678",//随机密码
      "containerPort": {
         {
           "HostIp": "101.71.29.5",
           "HostPort": "32771"
         }
      }
      "destroyTime": 1545481374
      "contianerState":runnig|created|deleted
    }
  ```

- [ ] 暂停容器 // TODO:暂不做实现
- [ ] **申请延时**

  传入参数示例：

  ```
  {
    "option":"delay"
    "paramList": {
        "destroyTime": 1545481374
    }
  }
  ```

  ```
    {
      //省略返回头信息
      "data": {
      "containerId": "d8001a2c7e5b",
      "hostIP": "101.71.29.5",
      "username": "admin",//WEB服务无需返回账号密码
      "password": "12345678",//随机密码
      "containerPort": {
         {
           "HostIp": "101.71.29.5",
           "HostPort": "32771"
         }
      }
      "destroyTime": 1545481374
      "contianerState":runnig|created|deleted
    }
  ```

### GET /contianers

- [ ] 查询所有容器信息(简要信息)

  返回格式示例:

  ```
    {
      //省略返回头信息
      "data": {
        "containerId": "d8001a2c7e5b",
        "image": "mysql",
        "command": "/start.sh",
        "created": "3 days ago",
        "status": "Created",
        "ports": "22/tcp, 0.0.0.0:80->8080/tcp"
        }
    }
  ```

##  镜像相关

### tips: 后续补充


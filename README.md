# DockerLab V1.0

#### 关于本项目的碎碎念:
>不争气的阿弟表示没有时间做docker控制那部分了。于是帮阿弟写一个中间件使得docker的remote api 调用起来可以无脑一点，
可以不用管集群，容器的增删改查可以更加的便利。(其实直接调用docker的remote api 也差不多 =.= !).使用tornado+aiodocker+motor借用docker 的 swarm 做一个对集群
内容器的简单增删改查.(如果后来这个项目要继续的话只能看那个学弟要接锅了，咕咕咕咕....)\
2019-2-13\
姑且算是v1.0版本了.嗯怎么说呢,订需求时就存在很多问题.以下是关于配置文件和部分模块说明,api的接口文档参考同一目录下的
"Docker连接器需求文档.md".

#### 配置文件说明

##### [Log]
>
> * level = debug
>   >日志等级

##### [MongoDB]
>
> * IP = 127.0.0.1
>   >mongo的hostIP, 默认127.0.0.1
> * port = 27017
>   >mongo的端口默认27017

##### [DockerRemote]
>
> * IP = 127.0.0.1
>   >Docker remote api 的地址,必须手动指定
> * port = 27017
>   >Docker remote api 的端口,必须手动指定

##### [DockerSettings]
>
> * default_life = 3600
>   > 容器的默认存活时间单位秒


#### 模块说明
> ps:结锅者请详细阅读.

> 日志模块直接使用了tornado自己带的日志,tornado自己的日志就封装的不错.(吐槽下,异步的tornado自带的
日志尽然是同步的).嗯,如果有空的话可以研究下异步的日志来代替tornado自己的日志.

> controller部分没啥说的,初始化对应的server后往里面一丢就行了.嗯由于采用事件触发的方式如果后续想要改成
HttpSocket很方便

> service由于只有这点需求我只玩成了container的部分,吧对应的报文投入execute方法,根据报文中的option
投入到对应的handle中进行处理,对于已知的错误请使用base.py中定义的错误类型,方便返回异常描述是可以自动去取
描述.

> module部分, 其实同一对象有两个模型,一个是对应的docker_remote_api的,一个是对应mongo的,remote_api
那边aiodocker已经封装好了,我就不添油加醋了,主要工作就在mongo那一块,由于只有定时删除过期容器这一需求module
处就写的特别简化(捂脸,其实是懒),如果有后续请扩充.

> scheduled定时任务部分.吧任务写好然后丢进tornado的PeriodicCallback方法中就行了,没啥好说的.


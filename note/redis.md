数据库分类
        |-关系型数据库：MySQL、Oracle、sqlserver、postgresql
数据库 -|
        |-非关系型数据库：Redis、memcache、MongoDB
---------------------------------------------------------------------------------------------------------------------------
Redis数据库
                |-remote directory server
                |-C语言编写，开源软件
        |-介绍 -|-高性能的KV分布式内存数据库
        |       |-支持数据存储化，把数据存放到硬盘
        |       |-支持list、hash、set、zset等类型
        |       |-支持master-slave的数据备份模式
        |
        |       |-默认支持16个数据库，编号0-15
        |       |-key值不能重复，重复即覆盖
Redis  -|-使用 -|-set、get、del、ttl、flushall、type
        |       |-默认数据类型是string
        |
        |-安装 -|-PREFIX=安装路径
        |
        |               |-程序管理redis-server redis.conf
        |-服务管理方式 -| 
        |               |-脚本管理（脚本有问题，需要自己修改）
        |
        |           |-volatile-lru：最近最少使用，针对已设置ttl的key
        |           |-allkeys-lru：最少使用
        |           |-volatile-random：随机删除，针对已设置ttl的key
        |-内存管理 -|
        |           |-allkeys-random：随机删除
        |           |-volatile-ttl：移除最近过期的key
        |           |-noeviction：不删除key，写满时报错
        |
        |           |-目标：防止单点故障，减轻单个redis服务器压力（32G），应对高并发（10w+）
        |           |
        |           |           |-redis占用的内存：配置文件的maxmemory
        |           |           |-redis能存储多少key：官网给出大约2.5亿个
        |           |-常见问题 -|-哈希槽的值是多少：0-16383,默认16384个，可以通过修改ruby脚本调整哈希槽的数量（3个）
        |           |           |-key最大是多少：512M
        |           |           |-推算：32G内存--1K每个key--存3200w个，每个哈希槽大约2000个
        |           |           |-横向扩容redis集群时，手动迁移一定数量的哈希槽到新的机器上，仅仅是迁移了槽位，原来槽位上的数据不会随之迁移
        |           |
        |           |                               |-无中心节点
        |           |                               |-数据按照slot存储分布在多个redis实例上
        |           |                       |-优点 -|-平滑的扩容、缩容
        |           |                       |       |-故障自动转移（节点之间通过gossip协议交换通信状态，通过投票完成S到M角色转换
        |           |                       |       |-运维成本低，提高了系统的可扩展性和高可用性
        |           |       |-官方cluster  -|
        |           |       |               |       |-严重依赖外部redis-trub
        |           |       |               |       |-缺乏监控管理
        |           |       |               |       |-需要依赖Smart Client（连接维护、缓存路由表、MultiOp 和 Pipeline 支持）
        |           |       |               |-缺点 -|-Failover节点检查过慢，不容中心节点zookeeper速度快
        |           |       |                       |-Gossip消息的带宽开销
        |           |       |                       |-无法根据统计区分冷热数据
        |           |       |                       |-Slave是冷备，不能缓解读压力
        |           |       |
        |           |       |                   |-运维成本低
        |           |       |           |-优点 -|-业务方不用关心后台redis实例，跟操作redis一样
        |           |       |           |       |-Proxy的逻辑跟存储的逻辑是隔离的
        |           |       |-twemproxy-|
        |           |       |           |       |-代理层多了一次转发，性能耗损
        |           |       |           |-缺点 -|-进行扩容、缩容时部分数据失效，需要手动迁移，难以做到平滑的扩容、缩容
        |           |       |                   |-出现故障时不能自动转移，运维性差
        |           |       |
        |           |       |           |-redis高可用方案，一主多从结构
        |           |-方案 -|-哨兵模式 -|-监视在线主服务器状态，一旦主服务器掉线，在从服务器中选择一个提升为主
        |           |       |           |-故障自动切换
        |           |       |
        |           |       |       |-redis分布式存储方案，豌豆荚开源
        |           |       |-codis-|-代理后端redis，把数据均衡存储到后台总
        |           |       |       |-用户相对透明，感觉在操作一个redis
        |           |       |
        |           |       |                   |-不是用中间件
        |           |       |                   |-实现方法和代码可自己掌握并随时调整
        |           |       |           |-优点 -|-比是用代理的性能好，因为少了分发环节
        |           |       |           |       |-分发压力在客户端
        |           |       |           |       |-服务的无压力增加
        |-redis集群-|       |-客户端分片|
        |           |                   |       |-不能平滑的水平扩容
        |           |                   |-缺点 -|-扩容、缩容时需要手动调整分片程序规则
        |           |                           |-出现故障时不能自动转移
        |           |
        |           |                           |-所有的节点彼此互联，内部使用二进制协议优化传输速度和带宽
        |           |                           |-节点fail是集群中半数以上节点检测失效时才生效
        |           |               |-结构特点 -|-client直接连接任意节点，不需要proxy
        |           |               |           |-把所有物理节点映射到16384个slot上
        |           |               |           |-根据CRC算法对key进行16384取余，决定将该key存储在哪一个节点
        |           |               |
        |           |               |           |-redis集群没有采用一致性哈希，而是采用hash slots概念
        |           |               |           |-预先定义了16384个slot，对存入集群的key取余，决定放到哪一节点
        |           |-redis-cluster-|-哈希槽   -|-算法时CRC16算法，作者自己定义的
        |                           |           |-便于增删节点，分配或者收回对应节点的hash slot即可
        |                           |           |-每一个slot可以存储多个key-value
        |                           |
        |                           |           |-一个主节点挂掉后，他的从升级成主
        |                           |           |-挂掉的节点恢复后，会自动成为原来从的从，并且自动同步数据（启服务方式一致）
        |                           |-集群管理 -|-一主一从结构中如果主从同时宕机，则集群不再提供服务
        |                           |           |                                   |-redis-trib.rb add-node(节点添加进集群，默认为主节点)
        |                           |           |                       |-添加主节点|
        |                           |           |                       |           |-redis-trib.rb reshard(重新对哈希槽进行分片)
        |                           |           |           |-添加节点 -|
        |                           |           |           |           |           |-redis-trib.rb add-node --slave --master-id(添加从节点)
        |                           |           |           |           |-添加从节点|-如果不指定，自动识别从库最少的主节点
        |                           |           |           |                       |-如果现有主的从数量一致，则随机选择
        |                           |           |-节点管理 -|
        |                           |           |           |                       |-redis-trib.rb del-node(任意主节点+从节点id)
        |                           |           |           |           |-移除从节点|-从节点移除集群后会被停止服务，重启服务依旧显示为从节点
        |                           |           |           |           |           |-但在集群中已经查不到该节点信息
        |                           |           |           |-删除节点 -|
        |                           |           |                       |           |-不能直接移除主节点，需要先释放哈希槽
        |                           |           |                       |-移除主节点|-移除哈希槽注意先是接受点，后是移除点
        |                           |           |                       |           |-移除后主节点服务停止，重启后有集群信息，但是不在集群内
        |
        |                           |-一主一从
        |               |-结构模式 -|-一主多从
        |               |           |-主从从
        |               |
        |               |           |-salve向master发送sync命令
        |-redis主从同步-|           |-master启动后台存盘进程，并收集所有修改数据命令
        |               |-工作原理 -|-master完成存盘后，发送整个数据文件到slave
        |               |           |-slave接收数据文件，加载到内存中完成首次完全同步
        |               |           |-后续有新数据产生时，master继续将新的修改数据的命令发送到slave，完成同步
        |               |
        |               |       |-系统繁忙 -|
        |               |-缺点 -|           |-造成数据同步延时问题
        |               |       |-网络繁忙 -|
        |               |
        |               |                   |-开启：slaveof host port
        |               |       |-临时配置 -|
        |               |       |           |-关闭：slaveof no one
        |               |-配置 -|
        |                       |           |-slaveof masterip masterport
        |                       |-永久配置 -|
        |                                   |-masterauth（主库设置了密码）
        |
        |                       |-sentinel monitor mymaster 127.0.0.1 6379 1：监控的master
        |                       |-sentinel down-after-milliseconds mymaster 60000：监控master回复ping的最大时间，超过后判定主观下线
        |           |-最少配置 -|-sentinel auth-pass mymaster password：如果手动的master有密码认证，启用该配置项
        |           |           |-sentinel failover-timeout mymaster 180000：一次故障切换的最大时间，超过则认为故障切换失败
        |           |           |-sentinel parallel-syncs mymaster 1：执行故障切换时，最多有多少个slave对新的master进行同步
        |           |           |-（该数字越小，完成failover的时间越长）
        |           |
        |           |               |-监控，不断检查master和slave的工作状态
        |           |-哨兵进程作用 -|-提醒，当某一个节点出现问题是通过api发送到其他节点
        |           |               |-故障自动切换，master宕机后，投票选一个slave升成master，其他slave同步新的master，哨兵监视新的master
        |           |   
        |           |           |-主观下线：SDOWN，单个sentinel实例对master做出下线判定
        |-redis哨兵-|-判定标准 -|
        |           |           |-客观下线：ODOWN，多个sentinel实例对master做出下线判定，（多个sentinel实例进行协商后，统一结果）
        |           |
        |           |           |-每个sentinel实例以每秒一次的频率向集群中的master、slave和其他的sentinel发送ping命令
        |           |           |-如果一个实例距离最后一次有效回复ping命令的时间超过down-after-milliseconds的值，该实例被标记为主观下线
        |           |           |-如果一个master被一个sentinel判定为主观下线，则其他sentinel以每秒一次的频率确认该master是否主观下线
        |           |-工作过程 -|-当有足够数量的sentinel（配置文件指定）认为该master主观下线，则该master被判定为客观下线
        |           |           |-一般情况下sentinel会以每10s一次的频率向集群中的slave发送info命令
        |           |           |-当sentinel判定了一个master为客观下线以后，发送info命令的频率改为每秒一次，并投票出一个新的master
        |           |           |-若没有足够的sentinel对该master做出主观下线判定，则移除客观下线结果，
        |           |           |-若master重新有效回复sentinel的ping，移除主观下线结果
        |           |
        |           |                   |-基于redis主从同步，所有主从同步的有点，哨兵模式都有
        |           |           |-优点 -|-主从可切换，故障自动迁移，系统可用性更好（修复的宕机master会自动加入集群成为slave
        |           |           |       |-主从模式的升级版，系统更健壮
        |           |-方案分析 -|
        |           |           |-缺点 -|-在线横向扩容操作复杂，对硬件要求高
        |
        |                           |-Redis DataBase
        |                           |-数据持久化的方式之一
        |                   |-概述 -|-一定时间间隔，将内存内的数据集快照写入磁盘
        |                   |       |-术语叫SnapShot
        |                   |       |-数据恢复时直接讲磁盘快照内的数据读入内存
        |                   |
        |                   |                   |-save 900 1:900s内1个key变化
        |                   |           |-自动 -|-save 300 10:300s内10个key变化
        |                   |           |       |-save 60 10000:60s内10000个key变化
        |                   |           |
        |                   |           |       |-redis内部所有的rdb动作都是通过bgsave执行的，废弃save
        |                   |           |       |-达到内部save的配置
        |                   |-触发机制 -|-时机 -|-从节点执行全量复制操作，主节点执行rdb过程并将文件发送给从节点
        |                   |           |       |-执行debug reload命令重新加载redis时
        |                   |           |       |-执行shutdown命令时
        |                   |           |
        |                   |           |       |-save：阻塞当前redis服务，直到rdb过程完成，对于内存较大的实例不建议使用
        |                   |           |-手动 -|
        |                   |                   |-bgsave：主进程fork一个子进程执行rdb过程，完成后子进程自动结束，阻塞只发生在fork的一瞬间
        |           |-RDB  -|
        |           |       |               |-执行命令时，redis主进程判断是否存在子进程，如存在直接返回
        |           |       |               |-主进程执行fork操作，创建子进程，fork动作时主进程阻塞，微秒级
        |           |       |-bgsave流程   -|-fork动作完成后，主进程结束阻塞
        |           |       |               |-子进程创建rdb文件，根据主进程在内存的临时快照，完成后替换原有rdb文件
        |           |       |               |-子进程完成后发送信号给主进程，主进程统计更新信息
        |           |       |
        |           |       |               |-高性能的存储化实现
        |           |       |       |-优点 -|（创建一个子进程来执行持久化，先把数据写入临时文件，到临界点时用临时文件替换上个持久化文件，该过程中主进程不进行任何IO操作）
        |           |       |       |       |-大规模数据恢复且对数据完整性要求不高
        |           |       |-优劣 -|
        |           |               |       |-意外宕机时，最后一次持久化的数据丢失
        |           |               |-缺点 -|
        |           |                       |-不能完成实时持久化
        |-存储持久化|
        |           |               |-APPEND ONLY FILE
        |           |               |-只做追加操作的文件
        |           |       |-概述 -|-记录redis服务的所有写操作
        |           |       |       |-不断的将新的写操作追加到文件末尾
        |           |       |       |-使用cat命令可以查看文件内容
        |           |       |
        |           |       |           |-文本协议具有很好的兼容性
        |           |       |-文本格式 -|-所有命令采用追加方式，直接采用协议格式，避免二次开销
        |           |       |           |-可读性好，便于调试和修改
        |           |-AOF  -|
        |                   |                                           |-redis是单进程程序，不用缓冲区相当于直接写磁盘，性能低下
        |                   |       |-所有的写入命令追加到aof_buf缓冲区-|
        |                   |       |                                   |-从aof_buf到磁盘有多种策略选择（appendfsync）
        |                   |       |                                       |-always：总是同步，相当于不用aof_buf，性能低下
        |                   |       |-AOF缓冲区根据策略将缓存数据写入磁盘  -|-everysec：每秒，建议策略
        |                   |       |                                       |-no：不写入磁盘（废物策略）
        |                   |-流程 -|
        |                   |       |-随着aof文件越来越大，需要定期对aof文件进行重写
        |                   |       |-重启redis服务，加载aof文件恢复数据
        |                   |
        |                   |               |-可以灵活的设置持久化的方式
        |                   |       |-优点 -|
        |                   |       |       |-出现意外宕机是仅可能丢失1s的数据
        |                   |-优劣 -|
        |                           |       |-持久化文件体积通常大于rdb模式
        |                           |-缺点 -|
        |                                   |-执行fsync策略的速度比rdb慢
        |
        |                       |-set key values [s] [ms] [NX|XX]  -|-定义变量  key values 秒  毫秒 [变量存在则不赋值|变量不存在则不赋值]
        |                       |-setrange -|-替换已有变量的内容，下标从0开始
        |                       |-strlen   -|-查看value长度
        |           |-string   -|-append   -|-存在则追加，不存则创建
        |           |           |-setbit   -|-以位的方式存储数据（节约空间）
        |           |           |-decr     -|-自减
        |           |           |-incr     -|-自增
        |           |
        |           |           |-对比与栈结构（先进后出）
        |           |           |-lpush、lrange
        |-数据类型 -|-list     -|-lpop、llen
                    |           |-lindex、lset
                    |           |-rpush、rpop
                    |
                    |           |-定义的变量可以存储多组key/values
                    |           |-hset、hget
                    |-hash     -|-hmset、hmget、hkeys、hvals
                                |-hgetall
                                |-hdel
import rediscluster

nodes = [
    {"host": "172.16.44.142", "port": 7000},
    {"host": "172.16.44.142", "port": 7001},
    {"host": "172.16.44.142", "port": 7002},
    {"host": "172.16.44.142", "port": 7003},
    {"host": "172.16.44.142", "port": 7004},
    {"host": "172.16.44.142", "port": 7005}
]
cluster = rediscluster.RedisCluster(startup_nodes=nodes, decode_responses=True)
# print(cluster.get('name'))
print(cluster.set('name', 'test'))

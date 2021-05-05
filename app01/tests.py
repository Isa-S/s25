from django.test import TestCase
import redis

conn = redis.Redis(
    host='192.168.10.7',
    port=6379,
    password='52Shanshan.',
    encoding='utf-8'
)

# 设置键值对为13533640423="9999"， 且超时时间为10s（值写入到redis会自动转字符串转字节）
conn.set('13533640423', 9999, ex=10)

# 根据键获取值，如果存在，返回的是字节类型的数据，不存在则返回None
value = conn.get('13533640423')
print(value)
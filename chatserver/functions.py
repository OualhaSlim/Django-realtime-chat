from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher


def publish_message(user, message,humor):
    welcome = RedisMessage("{} {}: {}".format(humor,user.username.capitalize(), message))
    RedisPublisher(facility='foobar', broadcast=True).publish_message(welcome)

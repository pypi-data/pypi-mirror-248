from viso_sdk.constants import PREFIX


def gen_redis_key_local(node_id, port):
    return f"{PREFIX.REDIS.LOCAL}_{node_id}_{port}"

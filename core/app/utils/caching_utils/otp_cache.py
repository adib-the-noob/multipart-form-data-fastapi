import os
import redis
import requests
import config


# Create a Redis client
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_otp(user_id: int):
    try:
        otp = redis_client.get(user_id)
        if otp:
            return int(otp)
        return None
    except Exception as e:
        print(e)
        return None


def generate_otp(user_id: int, otp: int):
    try:
        # load all previus otps
        redis_client.delete(user_id)
        otp_obj = redis_client.setex(user_id, time=300, value=otp)
        get_otp(user_id)
        if otp_obj:
            print(f"OTP saved, {otp}")
            return True
        return False
    except Exception as e:
        print(e)
        return False




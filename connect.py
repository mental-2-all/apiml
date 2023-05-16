import redis
import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()
key = os.getenv("KEY")


def giveAClient():
    host = "redis-13465.c85.us-east-1-2.ec2.cloud.redislabs.com"
    port = "13465"
    username = "default"
    password = key

    pool = redis.ConnectionPool(
        host=host,
        port=port,
        username=username,
        password=password,
    )

    redis_client = redis.Redis(connection_pool=pool)
    return redis_client

def sendemail(email, body, firstName):
    auth = os.getenv("AUTH")
    temp = os.getenv("template")

    client = Courier(auth_token=auth)

    resp = client.send_message(
        message={
            "to": {
                "email": email,
            },
            "template": f"{temp}",
            "data":{
                "body":body,
                "firstName":firstName
            }
        }
    )

    print(resp['requestId'])


# redis = giveAClient()
# redis.delete("Carghai88#1468healthkit")
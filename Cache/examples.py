from datetime import datetime
from time import sleep
from redis import StrictRedis
from random import random
import pandas as pd
from Cache import Cache

### Comment this section if you don't have redis instance ###
redis = StrictRedis(decode_responses=True)
cache = Cache(redis)

#############################################################

###### Comment this section if you are using redis ##########
# cache = Cache()
#############################################################

# Example: cache string return

@cache.ttl(300)
def pseudo_calc():
    sleep(1)
    print("Computation in progress")
    return str(datetime.now())


for i in range(10):
    print(pseudo_calc())


@cache.ttl(123)
def another():
    return "hello"


# Example: cache pandas Dataframe

@cache.df(12)
def return_a_df(*args, **kwargs):
    sleep(1)
    print("Computation in progress")
    return pd.DataFrame({"time": [str(datetime.now()) for _ in range(5)], "foo": list(range(5))})


for i in range(5):
    print(return_a_df(1, 5))


# Example: cache dict

@cache.dict(60)
def return_a_dict(*args, **kwargs):
    sleep(1)
    print("Computation in progress")
    return {"now": str(datetime.now())}


for i in range(5):
    print(return_a_dict())


# Example: cache float number


@cache.float(60)
def return_a_float(*args, **kwargs):
    return random()


for i in range(5):
    print(return_a_float())

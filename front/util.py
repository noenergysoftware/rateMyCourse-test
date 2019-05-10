import random
from time import sleep, time

def rs(min=1, max=5):
    '''randomly sleep for some time
    '''
    sleep_time = random.uniform(min, max)
    sleep(sleep_time)
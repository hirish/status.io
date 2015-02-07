import requests
from redis import Redis
from rq import Queue
from workerfunctions import count_words_at_url, is_free
import time

r = Redis()
q = Queue(connection=r)
# job = q.enqueue(count_words_at_url, 'http://nvie.com')
job = q.enqueue(is_free, 3, 0, 0, 0, 0, 0)

print job.result
time.sleep(10)
print job.result
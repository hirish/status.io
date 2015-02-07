import requests
from redis import Redis
from rq import Queue
from workerfunctions import count_words_at_url
import time

q = Queue(connection=Redis())
job = q.enqueue(count_words_at_url, 'http://nvie.com')

print job.result
time.sleep(10)
print job.result

import time # need this for time key
import couchdb # need this for couchDB connection
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer (bootstrap_servers="129.114.26.34:30001")

consumer.subscribe (topics=["utilizations"])

couch = couchdb.Server('http://admin:password@129.114.26.247:30002/')


if "pa3" in couch:
    database = couch["pa3"]
else:
    database = couch.create("pa3")

# we keep reading and printing
for msg in consumer:
    current_milli_time = int(round(time.time() * 1000))
    content = str(msg.value, 'ascii')
    entry = {current_milli_time : content}
    database.save(entry)

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
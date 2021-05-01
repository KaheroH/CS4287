import os   # need this for popen
import time # for sleep
import json
import csv
from kafka import KafkaProducer  # producer of events

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.26.34:30001", 
                                          acks=1, 
                                          value_serializer=lambda v:json.dumps(v).encode('utf-8'))  # wait for leader to write to log
                                          
toAdd = ["id", "timestamp", "value", "property", "plug_id", "household_id", "house_id"]
with open('energy_part1.csv', "r") as infile:
    reader = list(csv.reader(infile))
    reader.insert(0, toAdd)

with open('energy_part1.csv', "w") as outfile:
    writer = csv.writer(outfile)
    for line in reader:
        writer.writerow(line)  

# create a dictionary

     
# Open a csv reader called DictReader
with open('energy_part1.csv', encoding='utf-8') as csvf:
    csvReader = csv.DictReader(csvf)
         
    # Convert each row into a dictionary
    # and add it to data
    for x in range(500):
        data = {}
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['id']
            data[key] = rows
            if(len(data)>= 1000):
                toSend = json.dumps(data, indent=4)
                producer.send ("utilizations", {'content' : data})
                producer.flush ()   # try to empty the sending buffer
                time.sleep (0.2)
                break                        
        
producer.close ()
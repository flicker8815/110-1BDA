#!/usr/bin/env python
# coding: utf-8

# In[2]:


# <user_id, user_id>
edges_path = "Brightkite_edges.txt"
# <user_id, checkin_time, latitude, longitude, location_id>
totalCheckins_path = "Brightkite_totalCheckins.txt"


# In[3]:


from pyspark import SparkContext
import numpy as np
import re
import time
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))
sc = SparkContext("local", "HW4_1")

# load file from path
text_file = sc.textFile(totalCheckins_path)

# word count
counts = text_file.map( lambda line: (line.lower().split("\t")[4],1) )             .reduceByKey( lambda a, b: a + b )             .sortBy( lambda x: x[1], False )
output = counts.collect()

for (locat, count) in output:
    print( f'({locat}, {count})' )
# Stopping Spark Context
sc.stop()
print("--- %s seconds ---" % (time.time() - start_time))


# In[4]:


from pyspark import SparkContext
import time
import numpy as np
import re
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))
sc = SparkContext("local", "HW4_2")

# load file from path
text_file = sc.textFile(totalCheckins_path)

# word count
counts = text_file.map( lambda line: (line.lower().split("\t")[0],1) )             .reduceByKey( lambda m, n: m + n)             .sortBy( lambda x: x[1], False )
output = counts.collect()

for (locat, count) in output:
    print( f'({locat}, {count})' )
# Stopping Spark Context
sc.stop()
print("--- %s seconds ---" % (time.time() - start_time))


# In[5]:


def computeTimeInterval(line):
    try:
        import datetime
        text = line.split("\t")[1]
        element = datetime.datetime.strptime(text,"%Y-%m-%dT%H:%M:%SZ")

        timeStart = str(element.hour).rjust(2,"0") + ":00"
        timeEnd = ("00" if element.hour+1 == 24 else str(element.hour+1).rjust(2,"0")) +":00"
        return (f"{timeStart}-{timeEnd}",1)
    except:
        return ("Error",1)

from pyspark import SparkContext
import time
import numpy as np
import re
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))
sc = SparkContext("local", "HW4_3")

# load file from path
text_file = sc.textFile(totalCheckins_path)

# word count
counts = text_file.map(computeTimeInterval)             .reduceByKey( lambda m, n: m + n )             .sortBy( lambda x: x[1], False )
output = counts.collect()

for (time_interval, count) in output:
    print( f'({time_interval}, {count})' )
# Stopping Spark Context
sc.stop()
print("--- %s seconds ---" % (time.time() - start_time))


# In[ ]:





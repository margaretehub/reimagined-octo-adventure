## the pymongo module



```Python
from pymongo import MongoClient

client = MongoClient()
# connection with a default host and port
# to open a connection to a specified host:
client = MongoClient('localhost', 27017)
# there is also a the option to us the MongoDB URI format:
client = MongoClient('momgodb://localhost:27017')


```


A instance of MongoDB can support multiple Mongo-databases. You can access in two ways to the data in the separate database:

```Python

db = client.test_collection   # attribute style access
db = client['test-collection'] # dictionary style access

```
Getting a collection ( The 'tables' in Mongo ) have the same syntax:

```python

collection = db.test_collection
# or:
collection = db['test_collection']

```

Collections and databases are created when the first document is inserted into them.
Documents can contain native Python types (like **datetime.datetime** instances) which will be automatically converted to and from the appropriate BSON types.

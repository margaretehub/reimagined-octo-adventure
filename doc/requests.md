## Retrieve and push data with the python module requests

The python [**request**](https://docs.python-requests.org/en/master/) is a easy way to retrieve and push data to REST-applications:

```python3
import requests
api_url = 'http://127.0.0.1:8000/'
response = requests.get(api_url)
print(response.json())
```

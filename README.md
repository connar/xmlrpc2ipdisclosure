# xmlrpc2ipdisclosure
A simple script for mass searching websites with pingback enabled in xmlrpc.php plugin. This allows for server ip disclosure.  

Can be also customized to search for other methods enabled by changing the following:
```py
def is_pingback_enabled(response_text):
    return "[can be customized]" in response_text
```

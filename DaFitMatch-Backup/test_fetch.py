import urllib.request
try:
    response = urllib.request.urlopen('http://127.0.0.1:8082/images/try-on/casual/casual-01.jpg')
    print("Status:", response.status)
    print("Content-Type:", response.getheader('Content-Type'))
    print("Content-Length:", response.getheader('Content-Length'))
except Exception as e:
    print("Error:", e)

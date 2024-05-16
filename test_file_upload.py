import urllib3

# Create a PoolManager
http = urllib3.PoolManager()

# Specify the file and URL
file_path = 'test.txt'
upload_url = 'http://127.0.0.1:8000/users/filelead'

# Prepare the multipart/form-data payload
fields = {
    'name': 'string',  
    'email': 'userA@example.com',
    'file': ('filename.txt', open(file_path, 'rb').read(), 'text/plain')
}

# Make the POST request
response = http.request('POST', upload_url, fields=fields)

# Receive and print the response
print(response.data.decode('utf-8'))
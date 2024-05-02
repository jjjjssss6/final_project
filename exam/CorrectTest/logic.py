import pycurl

def EasyCurl(content, url, method):
    print(url)
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    if method == 'GET':
        c.setopt(c.HTTPGET, 1)
    elif method == 'POST':
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, content)
    c.setopt(c.HTTPHEADER, ["Content-Type:application/json"])
    data = []

    def collect_data(chunk):
        data.append(chunk)

    c.setopt(c.WRITEFUNCTION, collect_data)
    c.perform()
    c.close()
    response = b''.join(data)
    response = response.decode('utf-8')
    return response
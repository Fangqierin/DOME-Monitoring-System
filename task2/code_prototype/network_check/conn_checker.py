import urllib.request


def check():
    try:
        url = "https://www.google.com"
        urllib.request.urlopen(url)
        status = "Connected"
    except Exception as e:
        print(e)
        status = "Not connected"
    print(status)
    if status == "Connected":
        pass


def run():
    check()


if __name__ == '__main__':
    check()

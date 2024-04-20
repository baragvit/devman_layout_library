import requests
def download_book():
    response = requests.get('https://tululu.org/txt.php?id=32168')
    response.raise_for_status()
    with open('book.txt', 'w') as b:
        b.write(response.text)


if __name__ == '__main__':
    download_book()
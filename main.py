import os

import requests


def download_books():
    os.makedirs('books', exist_ok=True)
    for i in range(1, 11):
        response = requests.get('https://tululu.org/txt.php', params={"id": i})
        response.raise_for_status()
        with open(f'books/id{i}.txt', 'w') as book:
            book.write(response.text)


if __name__ == '__main__':
    download_books()


# https://tululu.org/txt.php?id=32168
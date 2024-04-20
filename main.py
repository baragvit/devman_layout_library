import os

import requests
from bs4 import BeautifulSoup


def check_for_redirect(response):
    for history_response in response.history:
        if history_response.is_redirect:
            raise requests.exceptions.HTTPError()


def download_book(book_id):
    response = requests.get("https://tululu.org/txt.php", params={"id": book_id})
    response.raise_for_status()
    check_for_redirect(response)
    return response.text


def download_books(books_download_directory, book_start_id, book_end_id):
    for book_id in range(book_start_id, book_end_id + 1):
        try:
            book_text = download_book(book_id)
        except requests.exceptions.HTTPError:
            continue
        with open(f'{books_download_directory}/id{book_id}.txt', 'w') as book_file:
            book_file.write(book_text)


def print_book_title(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find('h1')
    name, author = [title.strip() for title in title_tag.text.split('::')]
    print(f"Заголовок: {name}")
    print(f"Автор: {author}")


if __name__ == '__main__':
    # os.makedirs('books', exist_ok=True)
    # download_books('books', 1, 10)
    print_book_title(1)
import os

import requests


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


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    download_books('books', 1, 10)

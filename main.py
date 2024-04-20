import os
import logging

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
logger = logging.getLogger(__name__)


def check_for_redirect(response):
    for history_response in response.history:
        if history_response.is_redirect:
            raise requests.exceptions.HTTPError()


def get_book_author_and_title(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find('h1')
    return (title.strip() for title in title_tag.text.split('::'))


def download_txt(book_url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(filename)
    book_file_path = os.path.join(folder, filename + '.txt')
    with open(book_file_path, 'w') as book_file:
        book_file.write(response.text)


def download_books(books_download_directory, book_start_id, book_end_id):
    for book_id in range(book_start_id, book_end_id + 1):
        try:
            book_title, _ = get_book_author_and_title(book_id)
            book_url = f"https://tululu.org/txt.php?id={book_id}"
            download_txt(book_url, f"{book_id}. {book_title}", books_download_directory)
        except requests.exceptions.HTTPError:
            logger.warning(f"Failed to download book with id={book_id}")
            continue


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    download_books('books', 1, 10)

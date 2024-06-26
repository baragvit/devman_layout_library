import requests
from bs4 import BeautifulSoup

url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
title_tag = soup.find('main').find('header').find('h1')
picture_tag = soup.find("img", class_="attachment-post-image")
content = soup.find("div", class_="entry-content").text

print(title_tag.text)
print(picture_tag['src'])
print(content)

from bs4 import BeautifulSoup
import requests
import csv

def check_access(url):
    """
    Checks if access to the given URL is denied
    Returns True if access is denied, False otherwise
    """
    response = requests.get(url)
    if response.status_code == 403:
        print("Access Denied")
        return True
    return False

# Print separator line
print('==========================================================')

# Prompt the user for the URL to scrape
url = input('Enter the URL to scrape: ')

# Check if access to the URL is denied
if check_access(url):
    exit()

# Send a request to the website and extract the content using BeautifulSoup with default html.parser
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# finds the title element
title_element = soup.select_one('h1')
title = title_element.text if title_element else ""

# Extract the body of the webpage
body_element = soup.select_one('body')
body = body_element.text if body_element else ""

# Find all heading tags and their text
heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
headings = [tag.text.strip() for tag in heading_tags]

# Find all links and their URLs
link_tags = soup.find_all('a')
link_urls = [tag.get('href') for tag in link_tags]

# Find all links with class names that start with "social"
social_tags = soup.find_all('a', class_=lambda x: x and x.startswith('social'))

# Extract the social media links
social_urls = [tag.get('href') for tag in social_tags]

# Find all image tags and their source URLs
image_tags = soup.find_all('img')
image_urls = [tag['src'] for tag in image_tags]

# Find all iframe tags and their source URLs
iframe_tags = soup.find_all('iframe')
iframe_urls = [tag['src'] for tag in iframe_tags]

# Find all video tags and their source URLs
video_tags = soup.find_all('video')
video_urls = [tag['src'] for tag in video_tags]

# Find all audio tags and their source URLs
audio_tags = soup.find_all('audio')
audio_urls = [tag['src'] for tag in audio_tags]

# Prompt the user for the output file name
output_file = input('Enter the name of the output file: ')

# Write the data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'body', 'link_url', 'image_url', 'embedded_media_url'])
    for url in link_urls:
        writer.writerow([title, body, url, "", ""])

    for url in image_urls:
        writer.writerow([title, body, "", url, ""])

    for url in social_urls:
        writer.writerow([title, body, "", "", url])

    for url in iframe_urls:
        writer.writerow([title, body, "", "", url])

    for url in video_urls:
        writer.writerow([title, body, "", "", url])

    for url in audio_urls:
        writer.writerow([title, body, "", "", url, ""])

# Print separator line
print('==========================================================')
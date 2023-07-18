import os
import requests
from bs4 import BeautifulSoup

# Function to replace multiple newlines with double newlines
def replace_newlines(text):
    return '\n\n'.join(paragraph.strip() for paragraph in text.split('\n\n') if paragraph.strip())

# Function to check if a paragraph has less than 5 words
def is_valid_paragraph(paragraph):
    return len(paragraph.split()) >= 5

# Function to find the biggest paragraph and drop paragraphs that are 50% of its length
def filter_paragraphs(paragraphs):
    if not paragraphs:
        return paragraphs
    
    # Find the biggest paragraph
    biggest_paragraph = max(paragraphs, key=len)

    # Calculate the length threshold for dropping paragraphs
    length_threshold = len(biggest_paragraph) * 0.3

    # Drop paragraphs that are 50% of the length of the biggest paragraph
    filtered_paragraphs = [p for p in paragraphs if len(p) >= length_threshold]

    return filtered_paragraphs

# Create scraped_content directory
if not os.path.exists('scraped_content'):
    os.makedirs('scraped_content')

# Open URL list
with open('urls.txt') as f:
    urls = f.read().splitlines()

for url in urls:

    # Get HTML
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    
    else:
        print(f'Failed to scrape {url}, status {response.status_code}')
        continue

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get headings
    headings = [tag.text for tag in soup.find_all('h1')]

    # Get paragraphs and filter out paragraphs with less than 5 words
    paragraphs = [p.text for p in soup.find_all('p') if is_valid_paragraph(p.text)]

    # Filter paragraphs based on length
    paragraphs = filter_paragraphs(paragraphs)

    # Join content
    content = '\n\n'.join(headings + paragraphs)

    # Replace multiple newlines with double newlines
    content = replace_newlines(content)

    # Create filename
    filename = url.split('/')[-1] + '.txt'

    # Write file
    with open(os.path.join('scraped_content', filename), 'w', encoding='utf-8') as f:
        f.write(content)

print('Scraping complete!')

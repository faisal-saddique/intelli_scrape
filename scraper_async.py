import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
import re
from utils.get_results_from_GPT import gpt_completion

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

# Function to get the response from ChatGPT
async def get_final_outline(url,scraped_content):
    template = f"""
Please make a short description (about 60 words) and also bullet-point highlights (one short sentence on feature) of the site: {url}, without any content from previous text generated. Here's the scraped content from this site:

SCRAPED CONTENT:
{scraped_content}

ANSWER (SHORT DESCRIPTION OF 60 WORDS + A BULLET-POINT HIGHLIGHTS LIST IN MARKDOWN FORMAT):
"""
    # Use the function
    result = await gpt_completion(template, max_tokens=2000)
    return result

async def scrape_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
            else:
                print(f'Failed to scrape {url}, status {response.status}')
                return

    soup = BeautifulSoup(html, 'html.parser')

    headings = [tag.text for tag in soup.find_all('h1')]

    paragraphs = [p.text for p in soup.find_all('p') if is_valid_paragraph(p.text)]

    paragraphs = filter_paragraphs(paragraphs)

    content = '\n\n'.join(headings + paragraphs)

    content = replace_newlines(content)
    
    filename = url.replace('.', '_').replace(' ', '_').replace('/', '_').replace(':',' ') + '.txt'

    desired_outline = await get_final_outline(url=url,scraped_content=content)

    async with aiofiles.open(os.path.join('scraped_content', filename), 'w', encoding='utf-8') as f:
        await f.write(content)
    
    async with aiofiles.open(os.path.join('scraped_content', "fetched_outline_" + filename), 'w', encoding='utf-8') as f:
        await f.write(desired_outline)

async def main():
    # Create scraped_content directory
    if not os.path.exists('scraped_content'):
        os.makedirs('scraped_content')

    # Open URL list
    with open('urls.txt') as f:
        urls = f.read().splitlines()

    tasks = [scrape_url(url) for url in urls]

    await asyncio.gather(*tasks)

    print('Scraping complete!')

# Run the main function
asyncio.run(main())
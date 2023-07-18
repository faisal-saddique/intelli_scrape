import os
import requests
import streamlit as st
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
def get_final_outline(url, scraped_content):
    template = f"""
Please make a short description (about 60 words) and also bullet-point highlights (one short sentence on feature) of the site: {url}, without any content from previous text generated. Here's the scraped content from this site:

SCRAPED CONTENT:
{scraped_content}

ANSWER (SHORT DESCRIPTION OF 60 WORDS + A BULLET-POINT HIGHLIGHTS LIST IN MARKDOWN FORMAT):
"""
    # Use the function
    result = gpt_completion(template, max_tokens=2000)
    return result

def scrape_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        st.error(f'Failed to scrape {url}, status {response.status_code}')
        return

    soup = BeautifulSoup(html, 'html.parser')

    headings = [tag.text for tag in soup.find_all('h1')]

    paragraphs = [p.text for p in soup.find_all('p') if is_valid_paragraph(p.text)]

    paragraphs = filter_paragraphs(paragraphs)

    content = '\n\n'.join(headings + paragraphs)

    content = replace_newlines(content)

    desired_outline = get_final_outline(url=url, scraped_content=content)

    st.success(f'SUCCESS! Url {url} is processed.')

    with st.expander(f"See results"):
        # Display the scraped content and desired outline
        st.subheader("Scraped Content:")
        st.write(content)

        st.subheader("Desired Outline:")
        st.write(desired_outline)

def main():
    # Create scraped_content directory
    if not os.path.exists('scraped_content'):
        os.makedirs('scraped_content')

    st.title("Compose Blog Outline")

    # Get URLs from user input
    urls_input = st.text_area("Enter the URLs (one URL per line):", height=200)
    urls = urls_input.splitlines()

    if st.button("Scrape URLs and Create Outline"):
        for url in urls:
            scrape_url(url)

    

if __name__ == "__main__":
    main()

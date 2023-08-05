import requests
from bs4 import BeautifulSoup
import re

def find_sitemap(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the sitemap link in the HTML
    sitemap_link = None
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and 'sitemap' in href:
            sitemap_link = href
            break

    # If no sitemap link was found, check for a robots.txt file
    if sitemap_link is None:
        robots_txt_url = url + '/robots.txt'
        robots_response = requests.get(robots_txt_url)
        robots_content = robots_response.text

        # Look for the sitemap directive in robots.txt
        sitemap_directive = 'sitemap:'
        if sitemap_directive in robots_content:
            sitemap_line = [line for line in robots_content.split('\n') if sitemap_directive in line.lower()][0]
            sitemap_link = sitemap_line.split(sitemap_directive, 1)[1].strip()

    # If still no sitemap link was found, check for common sitemap URLs
    if sitemap_link is None:
        common_sitemap_urls = [
            url + '/sitemap.xml',
            url + '/sitemap.php',
            url + '/sitemap.txt',
            url + '/sitemap-index.xml',
            url + '/sitemap/',
            url + '/sitemap/sitemap.xml',
            url + '/sitemap_index.xml',
            url + '/sitemap.xml.gz',
            url + '/sitemap_index.xml.gz',
            url + '/wp-sitemap.xml'
        ]
        for sitemap_url in common_sitemap_urls:
            sitemap_response = requests.head(sitemap_url)
            if sitemap_response.status_code == 200:
                sitemap_link = sitemap_url
                break

    # If still no sitemap link was found, check for sitemap references in the HTML
    if sitemap_link is None:
        sitemap_regex = re.compile(r'<loc>(.*?)</loc>')
        sitemap_matches = sitemap_regex.findall(response.text)
        if sitemap_matches:
            sitemap_link = sitemap_matches[0]

    return sitemap_link

# Example usage
url = 'https://www.magazinzahrada.cz'
sitemap = find_sitemap(url)
if sitemap:
    print(f"The sitemap for {url} is: {sitemap}")
else:
    print(f"No sitemap found {url}")

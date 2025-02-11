#!/usr/bin/env python3

"""
Docket: Advanced OSINT Tool

This script searches for publicly available information about an individual
using multiple search engines, extracts useful data, and stores the results
in a structured text file.

Features:
- Searches Google, Bing, DuckDuckGo, and Yandex.
- Extracts emails, phone numbers, and social media profiles.
- Checks email addresses against Have I Been Pwned (HIBP).
- Saves results in a structured text file.
- Reports whether any information was found.
"""

import sys
import time
import re
import requests
from bs4 import BeautifulSoup

# ----------------------
# API Keys (Set These)
# ----------------------
GOOGLE_API_KEY = "YOUR_GOOGLE_CUSTOM_SEARCH_API_KEY"
GOOGLE_CSE_ID = "YOUR_GOOGLE_CUSTOM_SEARCH_ENGINE_ID"
BING_API_KEY = "YOUR_BING_SEARCH_API_KEY"
HIBP_API_KEY = "YOUR_HIBP_API_KEY"

# Rate Limits
SEARCH_PAUSE = 2.0
PAGE_FETCH_DELAY = 3.0

# User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Docket-OSINT/2.0; +https://example.com)"
}

# Regex Patterns
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.\-]+", re.IGNORECASE)
PHONE_REGEX = re.compile(r"\+?\d{1,3}[\s-]?\(?\d{2,3}\)?[\s-]?\d{3,4}[\s-]?\d{4}", re.IGNORECASE)
SOCIAL_REGEX = {
    "twitter": re.compile(r"https?://(www\.)?twitter\.com/(\w+)", re.IGNORECASE),
    "linkedin": re.compile(r"https?://(www\.)?linkedin\.com/in/([\w\-]+)", re.IGNORECASE),
    "facebook": re.compile(r"https?://(www\.)?facebook\.com/([\w\-\.]+)", re.IGNORECASE),
    "instagram": re.compile(r"https?://(www\.)?instagram\.com/([\w\.\-]+)", re.IGNORECASE),
}

# ------------------------------
# OSINT Search Functions
# ------------------------------
def google_search(query):
    """Uses Google Custom Search API to get search results."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return [item['link'] for item in response.json().get("items", [])]
    return []

def bing_search(query):
    """Uses Bing Search API to get results."""
    url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [entry['url'] for entry in response.json().get("webPages", {}).get("value", [])]
    return []

def duckduckgo_search(query):
    """Uses DuckDuckGo for web search (scrapes results)."""
    url = f"https://html.duckduckgo.com/html/?q={query}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return ["https://duckduckgo.com" + a['href'] for a in soup.find_all("a", class_="result__url")]
    return []

def yandex_search(query):
    """Uses Yandex Search (scrapes results)."""
    url = f"https://yandex.com/search/?text={query}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return [a['href'] for a in soup.find_all("a", class_="link organic__url")]
    return []

def fetch_page_content(url):
    """Fetches a webpage and returns its text."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.text if response.status_code == 200 else None
    except:
        return None

def extract_info(text):
    """Extracts emails, phone numbers, and social media links from text."""
    return {
        "emails": list(set(re.findall(EMAIL_REGEX, text))),
        "phones": list(set(re.findall(PHONE_REGEX, text))),
        "social": {site: list(set(re.findall(regex, text))) for site, regex in SOCIAL_REGEX.items()}
    }

def check_hibp(email):
    """Checks Have I Been Pwned (HIBP) for breaches."""
    headers = {"hibp-api-key": HIBP_API_KEY, "User-Agent": "Docket-OSINT/2.0"}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

# ------------------------------
# OSINT Execution
# ------------------------------
def docket_search(last, first, middle=None):
    """Performs an OSINT search across multiple sources."""
    query = f"{last} {first} {middle}" if middle else f"{last} {first}"
    urls = set()
    urls.update(google_search(query))
    time.sleep(SEARCH_PAUSE)
    urls.update(bing_search(query))
    time.sleep(SEARCH_PAUSE)
    urls.update(duckduckgo_search(query))
    time.sleep(SEARCH_PAUSE)
    urls.update(yandex_search(query))

    results = []
    for idx, url in enumerate(urls):
        print(f"[+] Fetching {idx+1}/{len(urls)}: {url}")
        content = fetch_page_content(url)
        if content:
            data = extract_info(content)
            data["url"] = url
            for email in data["emails"]:
                data["hibp"] = check_hibp(email)
            results.append(data)
        time.sleep(PAGE_FETCH_DELAY)
    
    return results

# ------------------------------
# Output Formatting
# ------------------------------
def save_results(data, output_file):
    """Saves results in a formatted text file."""
    with open(output_file, "w") as file:
        if not data:
            file.write("No relevant information was found.\n")
            print("[!] No relevant information was found.")
            return

        for result in data:
            file.write(f"URL: {result['url']}\n")
            file.write(f"Emails: {', '.join(result['emails']) if result['emails'] else 'None'}\n")
            file.write(f"Phone Numbers: {', '.join(result['phones']) if result['phones'] else 'None'}\n")
            file.write("Social Media:\n")
            for site, profiles in result["social"].items():
                if profiles:
                    file.write(f"  - {site}: {', '.join(profiles)}\n")
            file.write("\n")

    print(f"[+] Results saved in {output_file}")

# ------------------------------
# Main Execution
# ------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python docket.py <LastName> <FirstName> [MiddleNameOrInitial]")
        sys.exit(1)
    
    output_filename = input("Enter output file name (with .txt extension): ").strip()
    if not output_filename.endswith(".txt"):
        output_filename += ".txt"

    results = docket_search(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    save_results(results, output_filename)

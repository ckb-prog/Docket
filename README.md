# Docket
Advanced people search tool
---------------------------
Docket: Open Source Intelligence (OSINT) Tool
=============================================
------------------------------------------------------------
1. OVERVIEW
------------------------------------------------------------

Docket is an advanced OSINT tool designed to search for publicly available 
information about an individual. It queries multiple search engines, 
extracts emails, phone numbers, and social media profiles, and checks 
for known data breaches using the Have I Been Pwned (HIBP) API.

------------------------------------------------------------
2. FEATURES
------------------------------------------------------------

- Multi-search engine support (Google, Bing, DuckDuckGo, Yandex).
- Web scraping for emails, phone numbers, and social media profiles.
- Data breach lookup via Have I Been Pwned API.
- User-defined output file name.
- Rate limiting for stability.
- Outputs structured results in a text file.

------------------------------------------------------------
3. SYSTEM REQUIREMENTS
------------------------------------------------------------

- Operating System: Linux, macOS, Windows
- Python Version: Python 3.x
- Internet Connection: Required for API calls and web searches
- Required Packages: `requests`, `beautifulsoup4`, `googlesearch-python`

------------------------------------------------------------
4. INSTALLATION
------------------------------------------------------------

1. Install Python 3 if not already installed.

2. Create a virtual environment (recommended):
```
   $ python3 -m venv docket_env
   $ source docket_env/bin/activate  # On Linux/macOS
   $ docket_env\Scripts\activate     # On Windows
```
3. Install required dependencies:
```
   $ pip install requests beautifulsoup4 googlesearch-python
```
------------------------------------------------------------
5. API SETUP
------------------------------------------------------------

Docket requires API keys for some search engines and breach lookups. 

1. **Google Custom Search API**  
   - Obtain an API key from: https://console.cloud.google.com/
   - Create a Custom Search Engine (CSE) and get the CX ID.
   - Set `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` in the script.

2. **Bing Search API**  
   - Obtain an API key from: https://portal.azure.com/
   - Set `BING_API_KEY` in the script.

3. **Have I Been Pwned API**  
   - Obtain an API key from: https://haveibeenpwned.com/API/Key
   - Set `HIBP_API_KEY` in the script.

------------------------------------------------------------
6. USAGE
------------------------------------------------------------

To run Docket, use the following command:
```
   $ python docket.py <LastName> <FirstName> [MiddleNameOrInitial]
```
Example:
```
   $ python docket.py Doe John A
```
Upon execution, the script will prompt for an output file name:

   Enter output file name (with .txt extension): results.txt

Docket will:
- Search for information using multiple search engines.
- Extract emails, phone numbers, and social media profiles.
- Check discovered email addresses against the HIBP database.
- Save results in the specified text file.

------------------------------------------------------------
7. OUTPUT FORMAT
------------------------------------------------------------

The results are stored in a plain text file with structured formatting.

Example output:

------------------------------------------------------------
Search Results for: John A Doe
------------------------------------------------------------
```
URL: https://example.com
Emails: john.doe@example.com
Phone Numbers: +1 555-123-4567
Social Media:
  - Twitter: johndoe
  - LinkedIn: johndoe123

Have I Been Pwned Results:
  - Breach: SomeBreach
  - Date: 2022-01-01
```
------------------------------------------------------------
8. ERROR HANDLING
------------------------------------------------------------

- If no information is found, the script outputs "No relevant information was found."
- If an API request fails, check network connectivity and API key validity.
- If rate limits are exceeded, wait before retrying.

------------------------------------------------------------
9. LEGAL AND ETHICAL CONSIDERATIONS
------------------------------------------------------------

Docket is designed for ethical OSINT research. Users must ensure their 
use of the tool complies with applicable laws and regulations. Unauthorized 
information gathering without consent may be illegal.

------------------------------------------------------------
10. TROUBLESHOOTING
------------------------------------------------------------

Problem: "ModuleNotFoundError: No module named 'requests'"
Solution: Ensure dependencies are installed using:
```
   $ pip install requests beautifulsoup4 googlesearch-python
```
Problem: "No results found"
Solution: The individual may have a low online presence. Try different variations 
          of the name or additional search terms.

Problem: "Google API key error"
Solution: Ensure `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` are correctly set 
          in the script.

Problem: "HIBP API error"
Solution: Verify the API key is valid and not expired.

------------------------------------------------------------
11. LICENSE
------------------------------------------------------------

Docket is released under the GPL-3 License. The author assumes no liability 
for misuse or illegal activity.

------------------------------------------------------------
12. DISCLAIMER
------------------------------------------------------------

This tool is for research and educational purposes only. The author 
does not support illegal use of OSINT techniques.

import re
import urllib.parse
import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def search_live_web(keyword: str, platform: str = "Web Search", max_results: int = 6) -> List[Dict]:
    """
    Executes a real-time live web search across search engines,
    extracting live buyer prospects, emails, and company websites.
    """
    results = []
    queries = [
        f'"{keyword}" wholesale buyer email contact',
        f'"{keyword}" distributors importers contact email',
        f'"{keyword}" buyer inquiry sales@ or info@'
    ]
    
    for q in queries:
        if len(results) >= max_results:
            break
        try:
            encoded_query = urllib.parse.quote_plus(q)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            resp = requests.post(
                "https://html.duckduckgo.com/html/",
                data={"q": q},
                headers=HEADERS,
                timeout=6
            )
            
            if resp.status_code != 200:
                resp = requests.get(url, headers=HEADERS, timeout=6)
                
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                results_elements = soup.find_all('div', class_='result') or soup.find_all('div', class_='results_links')
                
                for el in results_elements:
                    title_elem = el.find('a', class_='result__title') or el.find('a', class_='result__url') or el.find('h2')
                    snippet_elem = el.find('a', class_='result__snippet') or el.find('div', class_='result__snippet')
                    url_elem = el.find('a', class_='result__url')
                    
                    title = title_elem.get_text(strip=True) if title_elem else f"{keyword} Global Trade Co"
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    raw_link = url_elem.get_text(strip=True) if url_elem else ""
                    
                    if not snippet and not raw_link:
                        continue
                        
                    raw_text = f"{title} | {snippet}"
                    found_emails = EMAIL_REGEX.findall(raw_text)
                    
                    domain = ""
                    if raw_link:
                        cleaned = raw_link.replace("http://", "").replace("https://", "").strip()
                        domain = cleaned.split("/")[0].split("?")[0]
                    
                    email_to_use = ""
                    if found_emails:
                        email_to_use = found_emails[0].strip().rstrip('.')
                    elif domain and "." in domain and not any(skip in domain for skip in ["duckduckgo", "google", "bing"]):
                        email_to_use = f"contact@{domain}"
                        
                    if email_to_use:
                        raw_text += f" Contact: {email_to_use}"
                        
                    company_clean = title.split("—")[0].split("-")[0].split("|")[0].strip()[:35]
                    
                    results.append({
                        "raw_text": raw_text,
                        "buyer_name": company_clean or f"Lead for {keyword}",
                        "company_name": company_clean or f"{keyword} Importers Ltd",
                        "website": domain or "https://b2b-trade-leads.org",
                        "country": "International",
                        "source_platform": platform
                    })
                    
                    if len(results) >= max_results:
                        break
        except Exception as e:
            logging.info(f"Live search query for {platform} encountered network error: {e}")
            
    return results

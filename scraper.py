import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# আপনার টার্গেট ইউআরএল
TARGET_URL = "https://bongobd.com/" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def fetch_links():
    extracted_data = []
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # পেজের সমস্ত এঙ্কর (<a href="...">) ট্যাগ বের করা
            for a_tag in soup.find_all('a', href=True):
                title = a_tag.get_text(strip=True)
                link = a_tag['href']
                
                # শুধু কাজের লিংকগুলো ফিল্টার করা
                if title and link.startswith('http'):
                    extracted_data.append({
                        "title": title,
                        "url": link
                    })

    except Exception as e:
        print("Scraping error:", e)

    return {
        "status": "success",
        "last_updated": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        "total_links": len(extracted_data),
        "links": extracted_data
    }

if __name__ == "__main__":
    data = fetch_links()
    
    # links.json ফাইলে আউটপুট সেভ
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Update complete. Saved {data['total_links']} links.")

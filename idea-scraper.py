from bs4 import BeautifulSoup # type: ignore
import requests
import sys
from datetime import datetime
import csv
import os

file_path = 'ideas.csv'

# Check if the file already exists
file_exists = os.path.isfile(file_path)

sys.stdout.reconfigure(encoding='utf-8')


scraped_data = {
    # Basic Info
    'date': "",
    'title': "",
    'tags': "",
    
    # Description & Content
    'description': "",
    
    # Market Analysis (A.C.P. Framework)
    'audience_score': "",
    'community_score': "",
    'product_score': "",
    
    # Business Model
    'categorization': {},
    "offer": "",

    'why_now_reason': "",
    'proof_signals': "",
    'market_gap': "",
    
    # Execution
    'execution_plan': "",
    
    # Metadata
    'scraped_at': "",
}

def to_text_list(tags):
    text_list = []
    try:
        for tag in tags:
            text_list.append(tag.text)

        return text_list
    except Exception as e:
        print(f"Error in to_text_list: {e}")
        return "null"

try:
    data = requests.get(f"https://www.ideabrowser.com/idea-of-the-day")
    data.raise_for_status()
    if data.status_code == 200:
        soup = BeautifulSoup(data.text, "lxml")
        date = soup.find("nav", class_="__className_dea3b2").find_all("a")[1].find("span").text
        scraped_data["date"] = date or None

        title = soup.find("h1", class_="__className_127ae0").text
        scraped_data["title"] = title or None

        tags = to_text_list(soup.select(".hidden.sm\\:flex.sm\\:flex-wrap.sm\\:gap-2 > div"))
        scraped_data["tags"] = tags or None

        description = soup.find("p", class_="__className_257321 text-lg text-gray-600 whitespace-pre-wrap").text
        scraped_data["description"] = description or None

        acp = to_text_list(soup.find_all("span", class_="__className_257321 font-semibold text-green-600"))
        scraped_data["audience_score"] = acp[0].split("/")[0] or None
        scraped_data["community_score"] = acp[1].split("/")[0] or None
        scraped_data["product_score"] = acp[2].split("/")[0] or None

        categorization = soup.select(".grid.grid-cols-2.gap-4 > div")
        cat = {}
        for el in categorization:
            c_key = el.select("div > p")[0].text or None
            c_val = el.select("div > p")[1].text or None
            cat[c_key] = c_val
        
        trend_analysis = soup.find("p", string="Trend Analysis").next_sibling.text
        cat["trend_analysis"] = trend_analysis
        scraped_data["categorization"] = cat or None

        offer = soup.select(".__className_257321.text-2xl.font-semibold.tracking-tight.mb-4")[0].next_sibling.text
        scraped_data["offer"] = offer or None

        why_now = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(2) > p")[0].text
        scraped_data["why_now_reason"] = why_now or None

        proof = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(3) > p")[0].text
        scraped_data["proof_signals"] = proof or None

        mgap = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(4) > p")[0].text
        scraped_data["market_gap"] = mgap or None
        
        execution = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(5) > p")[0].text
        scraped_data["execution_plans"] = execution or None

        scraped_data["scraped_at"] = datetime.now().isoformat()

        print("scraped")

        with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=scraped_data.keys())

            if not file_exists:
                print("creating ideas.csv")
                writer.writeheader()

            writer.writerow(scraped_data)
            print("written to ideas.csv")


    else:
        print("fetch unsuccessful with status", data.status_code)

except Exception as e:
    print(f"Error processing: {e}")
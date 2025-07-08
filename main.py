from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

app = Flask(__name__)

def to_text_list(tags):
    text_list = []
    try:
        for tag in tags:
            text_list.append(tag.text)
        return text_list
    except Exception as e:
        print(f"Error in to_text_list: {e}")
        return []

@app.route('/scrape', methods=['GET'])
def scrape_idea():
    scraped_data = {
        'date': "",
        'title': "",
        'tags': "",
        'description': "",
        'audience_score': "",
        'community_score': "",
        'product_score': "",
        'categorization': {},
        "offer": "",
        'why_now_reason': "",
        'proof_signals': "",
        'market_gap': "",
        'execution_plan': "",
        'scraped_at': "",
    }

    try:
        data = requests.get("https://www.ideabrowser.com/idea-of-the-day")
        data.raise_for_status()
        if data.status_code == 200:
            soup = BeautifulSoup(data.text, "lxml")

            nav = soup.find("nav", class_="__className_dea3b2")
            a_tags = nav.find_all("a") if nav else []
            if len(a_tags) > 1 and a_tags[1].find("span"):
                scraped_data["date"] = a_tags[1].find("span").text
            else:
                scraped_data["date"] = ""

            title_tag = soup.find("h1", class_="__className_127ae0")
            scraped_data["title"] = title_tag.text if title_tag else ""

            tags_divs = soup.select(".hidden.sm\\:flex.sm\\:flex-wrap.sm\\:gap-2 > div")
            scraped_data["tags"] = ", ".join(to_text_list(tags_divs)) if tags_divs else ""

            desc_tag = soup.find("p", class_="__className_257321 text-lg text-gray-600 whitespace-pre-wrap")
            scraped_data["description"] = desc_tag.text if desc_tag else ""

            acp = to_text_list(soup.find_all("span", class_="__className_257321 font-semibold text-green-600"))
            scraped_data["audience_score"] = acp[0].split("/")[0] if len(acp) > 0 and "/" in acp[0] else ""
            scraped_data["community_score"] = acp[1].split("/")[0] if len(acp) > 1 and "/" in acp[1] else ""
            scraped_data["product_score"] = acp[2].split("/")[0] if len(acp) > 2 and "/" in acp[2] else ""

            cat = {}
            for el in soup.select(".grid.grid-cols-2.gap-4 > div"):
                c_key_val = el.select("div > p")
                if len(c_key_val) > 1:
                    c_key = c_key_val[0].text
                    c_val = c_key_val[1].text
                    cat[c_key] = c_val
            trend_tag = soup.find("p", string="Trend Analysis")
            if trend_tag and trend_tag.next_sibling:
                trend_analysis = trend_tag.next_sibling.text
                cat["trend_analysis"] = trend_analysis
            scraped_data["categorization"] = json.dumps(cat)

            offer_sel = soup.select(".__className_257321.text-2xl.font-semibold.tracking-tight.mb-4")
            scraped_data["offer"] = offer_sel[0].next_sibling.text if offer_sel and offer_sel[0].next_sibling else ""

            why_sel = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(2) > p")
            scraped_data["why_now_reason"] = why_sel[0].text if why_sel else ""
            proof_sel = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(3) > p")
            scraped_data["proof_signals"] = proof_sel[0].text if proof_sel else ""
            market_sel = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(4) > p")
            scraped_data["market_gap"] = market_sel[0].text if market_sel else ""
            exec_sel = soup.select(".hidden.md\\:flex.md\\:flex-col.gap-12.p-8.border.rounded-xl.shadow > div:nth-of-type(5) > p")
            scraped_data["execution_plan"] = exec_sel[0].text if exec_sel else ""
            scraped_data["scraped_at"] = datetime.now().isoformat()

            return jsonify(scraped_data)
        else:
            return jsonify({"error": f"Status code {data.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)

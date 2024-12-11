from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to perform Google Custom Search
def google_search(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"items": []}

# Function to fetch the full content of a page
def full_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join([para.get_text() for para in paragraphs])
    except:
        return "Content not available."

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            # Your Google API key and Custom Search Engine ID
            api_key = "AIzaSyCtVEgWJu89j8fqolEBvL9Bmz54v7Eo8Dw"
            cse_id = "c1eca2c1a015649ec"

            # Fetch search results
            search_results = google_search(query, api_key, cse_id)

            # Process search results
            for item in search_results.get("items", []):
                content_preview = full_content(item["link"])[:300]
                results.append({
                    "title": item["title"],
                    "link": item["link"],
                    "content_preview": content_preview
                })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

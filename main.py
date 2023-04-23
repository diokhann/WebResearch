import requests
from bs4 import BeautifulSoup
from googlesearch import search as GoogleSearch
from transformers import pipeline
from tqdm import tqdm
from flask import Flask, send_file

def google_search(query, num_results):
    search_results = [url for url in GoogleSearch(query, num_results=num_results)]
    return search_results

def extract_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        print(f"Error while fetching the content from {url}: {e}")
        return ""

def summarize_articles(queries, num_results, output_file="summary.txt"):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
    max_length = 1024

    with open(output_file, "w") as f:
        for query in tqdm(queries, desc="Queries"):
            try:
                search_results = google_search(query, num_results)
            except Exception as e:
                print(f"Error while searching for '{query}': {e}")
                continue

            for url in tqdm(search_results, desc="URLs", leave=False):
                text = extract_text(url)
                if text:
                    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]

                    summaries = []
                    for chunk in chunks:
                        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
                        summaries.append(summary.strip())

                    if summaries:
                        f.write(f"Query: {query}\n")
                        f.write(f"URL: {url}\n")
                        f.write("Summary:\n")
                        for summary in summaries:
                            f.write(f"{summary}\n")
                        f.write("\n")
                    else:
                        print(f"Couldn't generate a summary for {url}")

def remove_duplicate_urls(lines):
    unique_lines = []
    urls = set()

    for line in lines:
        if line.startswith("URL:"):
            url = line.strip()[4:].strip()
            if url in urls:
                continue
            urls.add(url)
        unique_lines.append(line)

    return unique_lines

def generate_html(input_file="summary.txt", output_file="summary.html"):
    with open(input_file, "r") as f:
        lines = f.readlines()

    lines = remove_duplicate_urls(lines)

    with open(output_file, "w") as f:
        f.write("<html>\n<head>\n<title>Articles Summaries</title>\n</head>\n<body>\n")
        f.write("<h1>Articles Summaries</h1>\n")
        for line in lines:
            if line.startswith("Query:"):
                f.write(f"<h2>{line.strip()}</h2>\n")
            elif line.startswith("URL:"):
                url = line.strip()[4:].strip()
                f.write(f'<p><a href="{url}" target="_blank">{url}</a></p>\n')
            elif line.startswith("Summary:"):
                f.write("<ul>\n")
            elif line.strip() == "":
                f.write("</ul>\n")
            else:
                f.write(f"<li>{line.strip()}</li>\n")
        f.write("</body>\n</html>\n")

app = Flask(__name__)

@app.route("/")
def serve_summaries():
    return send_file("summary.html")

if __name__ == "__main__":
    queries = []
    while True:
        query = input("Enter a query (type 'end' to finish): ").strip()
        if query.lower() == "end":
            break
        queries.append(query)

    num_results = int(input("Enter the number of search results to consider for each query: "))

    summarize_articles(queries, num_results)
    generate_html()

    app.run()

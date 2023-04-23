# WebResearch

This Python script takes a list of queries, searches for articles related to those queries using Google Search, and then scrapes the content of the articles. It summarizes the scraped content using the Hugging Face Transformers library and generates an HTML page with the summaries. Finally, it serves the HTML page using a Flask web server.

## Prerequisites

To run this script, you need the following libraries installed:

- requests
- beautifulsoup4
- googlesearch-python
- transformers
- tqdm
- Flask

## Installation

To install the required libraries, open a terminal and run the following command:

```bash
pip install requests beautifulsoup4 googlesearch-python transformers tqdm Flask
```

## Running the Script

1. Open a terminal and navigate to the directory where the script is located.
2. Run the script using the command:

```bash
python main.py
```

3. Enter the queries one by one. To finish entering queries, type 'end' and press enter.

4. Enter the number of search results to consider for each query.

5. Wait for the script to fetch and summarize the articles. Once done, it will generate an HTML file called `summary.html` in the same directory as the script.

6. The script will start a Flask web server to serve the HTML file. Access the summarized articles by opening a web browser and navigating to the following address:

```
http://127.0.0.1:5000/
```

## Results

The generated `summary.html` file contains the summarized articles, organized by query and URL. Each summary is presented as a list item, and the original article URL is provided as a hyperlink.

The Flask web server serves the `summary.html` file, allowing you to access the summarized articles through a web browser.

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3). This means that you are free to use, modify, and distribute this code, but any modifications or derivative works must also be licensed under the GPLv3. By using or contributing to this project, you agree to abide by the terms of the GPLv3.

I am grateful for your interest in this project, and any suggestions or contributions are always welcome. If you have any ideas for improvements or encounter any issues, please feel free to open an issue or submit a pull request on GitHub.

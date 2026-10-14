import streamlit as st 
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import time
# if u see this hello there :3 

class LinkAndTitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._in_title_tag = False
        self._title_chunks = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
                self._in_title_tag = True
        
        if tag == "a":
            for attr, value in attrs:
                if attr == "href" and value.strip():
                    self.links.append(value.strip())
    # this bad boy looks for the links and title ^

    # this one gets the text in the tags 
    def handle_data(self, data):
        if self._in_title_tag:
            self._title_chunks.append(data)
    
    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title_tag = False
    
    @property
    def title(self):
        return "".join(self._title_chunks).strip()

def crawl_web(start_url, max_pages = 10):
    target_domain = urlparse(start_url).netloc
    to_visit = [start_url]
    visited = set()
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    while to_visit and len(visited) < max_pages:
        progress_ratio = len(visited) / max_pages
        progress_bar.progress(min(progress_ratio, 1.0))

        url = to_visit.pop(0)
        if url in visited: 
            continue

        status_text.text(f"Our spiders are on the case! : {url}")

        try:
            response = requests.get(url, timeout=10, headers={"User-Agent":"WordOnTheStreetCrawler/1.0"})
            visited.add(url)

            if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type",""):
                continue
                
            parser = LinkAndTitleParser()
            parser.feed(response.text)

            page_title = parser.title if parser.title else "No Title Found"
            results.append({"url": url, "title": page_title})

            for link in parser.links:
                absolute_url = urljoin(url, link)
                absolute_url = absolute_url.split('#')[0]

                if urlparse(absolute_url).netloc == target_domain:
                    if absolute_url not in visited and absolute_url not in to_visit:
                        to_visit.append(absolute_url)
                    
            time.sleep(0.1)

        except Exception:
            continue

    progress_bar.progress(1.0)
    status_text.text("Investigation complete!")
    return results

st.set_page_config(page_title="WORD ON THE STREET WEB CRAWLER", layout = "centered")
st.title("WORD ON THE STREET: A CRAWL SUBMISSION")
st.write("Worry not, our spiders are here to investigate the web for you with this web crawler! :D")
st. image("spydoor.png")

st.sidebar.header("Settings")
max_pages = st.sidebar.slider("Maximum pages to crawl", min_value = 1, max_value = 50, value = 10)

start_url = st.text_input("Starting URL:", placeholder = "https://www.google.com/")

if st.button("Start investigation", type = "primary"):
    if not start_url:
        st.error("Please enter a valid URL!")
    elif not (start_url.startswith("http://") or start_url.startswith("https://")):
        st.error("URL must start with http:// or https:// !!")
    else:
        with st.spinner("Our spiders are on the case!"):
            crawl_data = crawl_web(start_url, max_pages)
        if crawl_data:
            st.success(f"Investigation complete! {len(crawl_data)} pages crawled.")
            st.dataframe(crawl_data)
        else:
            st.error("Could not start investigation :(")

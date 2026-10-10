from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

#staticmethod gets html from site, turns it into string, so it could be parsed
class Spider:

    #var for all spiders
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

#makes it so that first spider does prepares the queue and crawled file and what not
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

#makes it so that when after it crawles, its put in the crawled file
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + 'crawling' + page_url)
            print('Queue' + str(len(Spider.queue)) + '| Crawled' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

#when it crawls a page, it shows links
    @staticmethod 
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html': #makes sure its at a webpage
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string) #parses
        except:
            print('Error: can not crawl page')
            return()
        return finder.page_links() 

    @staticmethod
    def add_links_to_queue(links):
        for url in links: #checks links
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url: #makes so that it only crawls the website u want xd
                continue 
            Spider.queue.add(url)

    @staticmethod
    def update_files(): #converts set to file
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


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
        Spider.crawled_file = Spider.crawled_file + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

#makes it so that first spider does prepares the queue and crawled file and what not
    @staticmethod
    def boot(self):
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
            Spider.add_links_to_queue(Spider.gather_link(page_url))
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
                html_string = html_bytes.decode("utf-8")\
            finder = LinkFinder(Spider.base_url, page_url)

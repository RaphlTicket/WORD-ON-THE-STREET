import os

#makes new folder, makes sure it doesnt override when one already exists
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('creating project' + directory)
        os.makedirs(directory)

#queue and crawled files, checks if it was already crawled or not
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

#create new file.. fix error here
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

create_data_files('wikipedia', 'https://en.wikipedia.org/wiki/Main_Page')

#add data onto file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

#delete content of file

def delete_file_contents(path):
    with open(path, 'w'):
        pass

def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(links,  file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)
        
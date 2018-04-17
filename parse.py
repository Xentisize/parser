import bs4
from bs4 import BeautifulSoup
import re

posts = {}
writer_pattern = re.compile(r'by ([A-Za-z\s]+) on')


def extract_text(element, writer):
    text = ""
    while element.name != 'script':
        if isinstance(element, bs4.element.NavigableString):
            element = element.next_sibling
        else:
            if len(element.contents) == 0:
                element = element.next_sibling
            else:
                contents = element.contents
                for str in contents:
                    if str.string is not None:
                        text += str.string.rstrip()
                element = element.next_sibling
    return text


with open('html/135013.htm') as fh:
    soup = BeautifulSoup(fh, 'lxml')

    line_breaks = soup.find_all('hr')  # <hr> divides every post by students
    line_breaks = line_breaks[:-1]  # The last <hr> has no post

    for hr in line_breaks:
        heading = hr.select('+ h3')[0]
        heading_text = heading.string
        writer = re.search(writer_pattern, heading_text)[1]
        content = extract_text(heading.next_sibling, writer)
        posts[writer] = content

with open('135013.txt', 'w') as fh:
    fh.write("Name|Comments|Characters|Words\n")
    for k, v in posts.items():
        fh.write("{}|{}|{}|{}\n".format(k, v, len(v), len(v.split(' '))))
        # fh.write("{}:\n{}\n".format(k, v))
        # fh.write("\nCharaters including space: {}\n".format(len(v)))
        # fh.write("Word count: {}\n\n".format(len(v.split(' '))))

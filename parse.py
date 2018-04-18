import bs4
from bs4 import BeautifulSoup
import re
import output_excel
import freq_word

# posts = {}
writer_pattern = re.compile(r'by ([A-Za-z\s]+) on')

def check_if_reference(str):
    reference_pattern = re.compile(r'^(supply|of) \bsources?|references?\b', re.I)
    return reference_pattern.search(str)

def extract_text(element, writer):
    text = ""
    while element.name != 'script':
        if isinstance(element, bs4.element.NavigableString):
            if len(element) <= 1:
                element = element.next_sibling
            else:
                text += element.string
                element = element.next_sibling
        else:
            if len(element.contents) == 0:
                element = element.next_sibling
            else:
                contents = element.contents
                for str in contents:
                    if str.string is not None:
                        if check_if_reference(str.string):
                            return text
                        text += str.string.rstrip()
                element = element.next_sibling
    return text



def positive_feedback_from_richard(div):
    positive_feedback = 0
    if 'Richard CHEUNG' in div.get_text():
        content = ''.join([para.string.lower() for para in div.find_all('p') if para.string is not None])
        # print("From Richard:" + content)
        positive_feedback += content.count('yes') + content.count('agree') + content.count('good')
    return positive_feedback

def extract_data(course):
    html_file = 'html/' + course + '.htm'
    txt_file = course + '.txt'

    with open(html_file) as fh:
        soup = BeautifulSoup(fh, 'lxml')
        full_text = soup.get_text()

        line_breaks = soup.find_all('hr')  # <hr> divides every post by students
        line_breaks = line_breaks[:-1]  # The last <hr> has no post

        for hr in line_breaks:
            heading = hr.select('+ h3')[0]
            heading_text = heading.string
            writer = re.search(writer_pattern, heading_text)[1]
            content = extract_text(heading.next_sibling, writer)
            if re.search(r'Source:https', content):
                content = content[:re.search(r'Source:https', content).start()]
            characters_with_spaces = len(content)
            total_words = len(content.split(' '))
            total_questions = content.count('?')
            total_responses = full_text.count(writer) - 1
            postive_feedback = 0

            divs = heading.select('~ div')

            for div in divs:
                if div.h3 is None:
                    continue
                if 'Richard CHEUNG' in div.h3.string:
                    positive_feedback = positive_feedback_from_richard(div)
                    break
                else:
                    continue

            if posts.get(writer) is None:
                posts[writer] = [content, characters_with_spaces, total_words, total_questions, total_responses, positive_feedback]
            else:
                posts[writer][0] += " " + content
                posts[writer][1] += characters_with_spaces
                posts[writer][2] += total_words
                posts[writer][3] += total_questions
                posts[writer][5] += positive_feedback


    with open(txt_file, 'w') as fh:
        fh.write("Name|Comments|Characters|Words|Questions Raised|Replies|Positive Feedback\n")
        for k, v in posts.items():
            fh.write(f"{k}|{v[0]}|{v[1]}|{v[2]}|{v[3]}|{v[4]}|{v[5]}\n")


if __name__ == '__main__':
    courses = ['135013', '135026']
    for course in courses:
        posts = {}
        extract_data(course)
        output_excel.write_to_excel(course)
        freq_word.counting_words(course)
    freq_word.sorted_dict()
    freq_word.write_to_excel(freq_word.sorted_word_counts)
    # print(freq_word.sorted_word_counts)

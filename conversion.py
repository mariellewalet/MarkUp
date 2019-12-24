""" GOAL OF PROJECT:
Make a mark down converter to html (based on stackedit online editor for MarkDown

Done so far :
    - can convert bold and italic correcly
    - mutlitple blockquote
    - links
    - titles
    - open file in browser

TO DO:
* add the table
* lists
* comment everything and sanity check
"""

import webbrowser


def convert(file):
    text_file = open(file, 'r')
    text_lines = text_file.readlines()
    text_file.close()
    string_output = '<html>\n'

    for para in text_lines:
        html_tags = ['div']
        if len(para) > 3 and para[0] == ' ' and para[1] == ' '  and para[2] == ' ' and para[3] == ' ':
            para = para.strip()
            html_tags.append('pre')
            html_tags.append('code')
            string_output += add_tags(html_tags, para)
            continue

        para = para.strip()
        if para == '':
            continue

        if para == '___':
            html_tags.append('hr')
            string_output += add_tags(html_tags, para)
            continue

        para = remove_special(para)

        if count_quote(para):
            for i in range(count_quote(para)):
                html_tags.append('blockquote')
            para = para[count_quote(para):].strip()

        if count_hashtag(para):
            count = count_hashtag(para)
            html_tags.append('h'+str(count))
            para = para[count:].strip()

        if len(html_tags) == 1:
            html_tags.append('p')

        string_output += add_tags(html_tags, para)

    string_output = string_output + '</html>'
    print(string_output)


    f = "converted_file.html"
    myfile = open(f, 'w')
    myfile.write(string_output)
    myfile.close()

    filename = 'file:///Users/marielle/Desktop/Projects/' + 'converted_file.html'
    webbrowser.open_new_tab(filename)


# Add the tags assimilated to that paragraph
def add_tags(html_tags, para):
    html_tags.reverse()
    for tag in html_tags:
        if tag == 'hr':
            para = '<hr>'
        else:
            para = '<' + tag + '>\n' + para + '</' + tag + '>\n'
    return para


def remove_special(string):
    while True:
        new_string = remove_link(string)
        if string == new_string:
            break
        string = new_string

    while True:
        new_string = replace_special_sub(string, 0)
        if new_string is None:
            return string
        string = new_string


def remove_link(string):
    index_left_b = -1
    index_right_b = -1
    index_left_para = -1
    index_right_para = -1

    for i in range(len(string)):
        if i<len(string) and string[i] == '[' and string[i+1] != ' ':
            index_left_b = i
        if index_left_b > -1 and index_right_b == -1 and string[i] == ']' and string[i-1] != ' ' and string[i+1] == '(':
            index_right_b = i
            index_left_para = i+1
        if index_left_para>-1 and string[i] == ')':
            index_right_para = i
            break

    if index_right_b > -1 and index_right_para > -1:
        string = string[:index_left_b] + '<a href="' + string[index_left_para+1:index_right_para].strip() + '">' + \
                 string[index_left_b+1:index_right_b] + '</a>' + string[index_right_para+1:]

    return string


# find the closest star from that index
def find_star(string, index):
    for i in range(index, len(string)):
        if string[i] == '*':
            return i
    return -1


def replace_special_sub(string, index):
    index_first_star = find_star(string, index)

    if index_first_star == -1:
        return None

    count_left = 0
    count_right = 0
    for i in range(index_first_star, len(string)):
        if i<len(string)-1 and string[i]=='*' and string[i+1] != ' ':
            count_left += 1
        else:
            break

    index_last_star = -1
    star = False
    for i in range(index_first_star+count_left+1, len(string)):
        if not star and string[i] != '*':
            continue
        elif string[i] == '*':
            star = True
            count_right += 1
        else:
            if count_right > 0:
                index_last_star = i
            break

    if count_right>0 and index_last_star == -1:
        index_last_star = len(string)

    count = min(count_right, count_left)

    if not count:
        return None

    sub = string[index_first_star+count:index_last_star-count]
    if count == 1 :
        return string[:index_first_star] + '<em>' + sub + '</em>' +string[index_last_star:]
    if count%2 == 0:
        return string[:index_first_star] + '<strong>' + sub + '</strong>' + string[index_last_star:]
    if count%2 == 1:
        return string[:index_first_star] + '<strong><em>' + sub + '</em></strong>' + string[index_last_star:]


def count_hashtag(string):
    count = 0
    for char in string:
        if char == '#':
            count+=1
        elif count>6:
            return 0
        else:
            return count


def count_quote(string):
    count = 0
    for char in string:
        if char == '>':
            count+=1
        else:
            return count


def special_char(string):
    if string[0] == '-' or string[0] =='#' or string[0] =='>':
        return True
    return False


if __name__ == '__main__':
    convert('text.txt')








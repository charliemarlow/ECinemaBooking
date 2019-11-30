import os

change_log = []
log = {
    'wrong' : '',
    'right' : '',
    'index' : 0,
}
curr_line = 0

html_map = {
    'index' : '/',
    'category' : '/search',
    'account' : '/account',
    'previousorders' : '/previous_orders',
    'make_showroom' : '/create_showroom',
    'make_showtime' : '/create_showtime',
    'manage_movies' : '/manage_movies',
    'single-product': '/',
    'make_movie' : '/create_movie',
    'manage_Showrooms' : '/manage_showrooms',
    'editprofile' : '/editprofile',
    'manage_showtimes' : '/manage_showtime',
    'forgot' : '/forgot',
    'reset' : '/reset',
    'edit_showroom' : '/edit_showroom',
}

def create_log(wrong, right, index):
    log = {
        'wrong' : wrong,
        'right' : right,
        'index' : index,
    }
    return dict(log)

def get_quoted(word, stop_char='\"'):
    quote_start = False
    current_word = ''
    for char in word:

        if quote_start:
            current_word = current_word + char

        if char == stop_char:
            quote_start = False if quote_start else True

    return current_word[0:-1]

def add_slash(word):
    current_word = get_quoted(word)

    if 'window.location' in current_word:
        current_word = get_quoted(current_word, stop_char="\'")
    elif '#' in current_word:
        change_log.append(create_log(current_word, "", curr_line))
        return

    if current_word:
        change_log.append(create_log(current_word, "/" + current_word, curr_line))

def fix_html(word):
    current_word = get_quoted(word)
    word = current_word[0:-5]
    change_log.append( create_log(word + ".html", html_map[word], curr_line))

def parse_single_line(line):
    for word in line.split(" "):
        if ('href' in word and
            ('/' not in word or 'html' in word)):
            if 'html' not in word and '/' not in word:
                add_slash(word)
            elif 'html' in word:
                fix_html(word)
    return

def has_link(line):
    return 'href=' in line and 'href=\"{{' not in line

def read_file(filename):
    start_reading = False
    with open(filename, "r") as file:
        global curr_line
        curr_line = 0
        for line in file:
            if "block content" in line:
                start_reading = True

            if start_reading and has_link(line):
                parse_single_line(line)

            if "endblock" in line:
                start_reading = False

            curr_line = curr_line + 1

    with open(filename, "r+") as file:
        filedata = file.read().split('\n')
        # basically for each item in change log
        for log in change_log:
            index = int(log['index'])

            # index into, replace what was wrong with whats right
            filedata[index] = filedata[index].replace(log['wrong'], log['right'])
        # then write it all back
        filedata = "\n".join(filedata)
        file.seek(0)
        file.write(filedata)
        file.truncate()
    change_log.clear()
    return

directory = "../ecinema/templates"
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        read_file(os.path.join(directory, filename))

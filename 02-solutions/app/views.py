from app import app
from flask import render_template, request


# 读取缩写文件并生成缩写和原始字符串的对
def read_abbreviations_file():
    abbreviations = []

    with app.open_resource('data/en-abbreviations.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#'):
                abbreviation, full_string = line.split(maxsplit=1)
                abbreviations.append((abbreviation, full_string))
    return abbreviations


# 首页，显示文件中前 10 个缩写和原始字符串的对
@app.route('/')
@app.route('/header')
def show_abbrev():
    abbreviations = read_abbreviations_file()[:10]
    return render_template('header.html', abbreviations=abbreviations)


# 搜索页面，列出文件中前 10 个以参数为前缀的缩写和原始字符串的对
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':  # POST Request Handling: it means the form on the page was submitted

        prefix = request.form['prefix']
        abbreviations = read_abbreviations_file()
        filtered_abbreviations = [(abbr, full) for abbr, full in abbreviations if abbr.lower().startswith(prefix.lower())][:10]
        return render_template('search.html', title='Search', prefix=prefix, abbreviations=filtered_abbreviations)
    return render_template('search.html')  # GET Request Handling: when the page is first loaded

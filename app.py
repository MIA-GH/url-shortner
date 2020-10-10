from flask import Flask, render_template, request
from flask import redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename
from flask import session

app = Flask(__name__)
app.secret_key = 'musahlovey2k'


@app.route('/')
def index():
    return render_template('index.html', codes=session.keys())


@app.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'POST':
        code = request.form['code']
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash('This short name has been taken, take a new one', 'info')
            return redirect(url_for('index'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            file = request.files['file']
            full_name = request.form['code'] + secure_filename(file.filename)
            file.save(
                'C:/Users/BABS/VSCodeProjects/Flask/flask-essential-training/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=code)
    else:
        return redirect(url_for('index'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return(redirect(url_for('static', filename='user_files/' + urls[code]['file'])))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/api')
def session_api():
    data = (session.keys())
    return render_template('api.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

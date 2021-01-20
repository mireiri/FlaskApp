from flask import Flask, render_template, session, request, redirect, url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import send_from_directory
from reg_graph import reg_graph
from pred_file import pred_file
from select_merge import select_merge

#インスタンスの作成
app = Flask(__name__)

#暗号鍵の作成
key = os.urandom(21)
app.secret_key = key

#idとパスワードの設定
id_pwd = {'Conan': 'Heiji'}

#データベース設定
URI = 'postgresql://postgres:mireiri@localhost/flasktest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

#テーブル内容の設定
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
    file_path = db.Column(db.String(64), index=True, unique=True)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.now)

#テーブルの初期化
@app.cli.command('initdb')
def initdb():
    db.create_all()

#メイン
@app.route('/')
def index():
    if not session.get('login'):
        return redirect(url_for('login'))
    else:
        data = Data.query.all()
        return render_template('index.html', data=data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logincheck', methods=['POST'])
def logincheck():
    user_id = request.form['user_id']
    password = request.form['password']

    if user_id in id_pwd:
        if password == id_pwd[user_id]:
            session['login'] = True
        else:
            session['login'] = False
    else:
        session['login'] = False

    if session['login']:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))

#ファイルアップロード
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/register', methods=['POST'])
def register():
    title = request.form['title']
    f = request.files['file']
    file_path = 'static/' + secure_filename(f.filename)
    f.save(file_path)

    registered_file = Data(title=title, file_path=file_path)
    db.session.add(registered_file)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    data = Data.query.get(id)
    delete_file = data.file_path
    db.session.delete(data)
    db.session.commit()
    os.remove(delete_file)
    return redirect(url_for('index'))

#単回帰グラフ
@app.route('/regression')
def regression():
    data = Data.query.all()
    return render_template('regression_select.html', data=data)

@app.route('/regression_graph/<int:id>', methods=['GET'])
def regression_graph(id):
    data = Data.query.get(id)
    file_path = data.file_path
    graph_path = reg_graph(file_path)
    return send_from_directory('download', graph_path, as_attachment=True)

#単回帰予測
@app.route('/predict')
def predict():
    data = Data.query.all()
    return render_template('predict_select.html', data=data)

@app.route('/predict_file', methods=['POST'])
def predict_file():
    file_id = request.form.getlist('select_files')
    files = []
    for i in file_id:
        data = Data.query.get(i)
        files.append(data.file_path)

    predict_file_path = pred_file(files)
    return send_from_directory('download', predict_file_path,
                                as_attachment=True)

#ファイル結合
@app.route('/merge')
def merge():
    data = Data.query.all()
    return render_template('select_file_merge.html', data=data)

@app.route('/file_merge', methods=['POST'])
def file_merge():
    file_num = request.form.getlist('select_files')
    files = []
    for i in file_num:
        data = Data.query.get(i)
        files.append(data.file_path)

    merge_file_path = select_merge(files)
    return send_from_directory('download', merge_file_path, as_attachment=True)

#ダウンロードファイル一覧
@app.route('/download')
def download():
    files = os.listdir('download')
    return render_template('download_files.html', files=files)

@app.route('/file_download/<file_path>', methods=['get'])
def file_download(file_path):
    return send_from_directory('download', file_path, as_attachment=True)

@app.route('/file_delete/<file_path>', methods=['get'])
def file_delete(file_path):
    file_path = 'download/' + file_path
    os.remove(file_path)
    return redirect(url_for('index'))

#使い方
@app.route('/description')
def description():
    return render_template('howtouse.html', title='HowToUse')


if __name__ == '__main__':
    app.run(debug=True)
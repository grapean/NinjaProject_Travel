from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import datetime

@app.route('/')
def home():
    return render_template('index_home.html')

@app.route('/create')
def create():
    return render_template('index_create.html')


@app.route('/create', methods=['POST'])
def test_create():
    title_receive = request.form['title_give']
    season_receive = request.form['season_give']
    area_receive = request.form['area_give']
    keywords_receive = request.form['keywords_give']
    review_text_receive = request.form['review_text_give']

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)


    doc = {
        'title': title_receive,
        'season': season_receive,
        'area': area_receive,
        'keywords': keywords_receive,
        'review_text': review_text_receive,
        'file': f'{filename}.{extension}',
        'data': mytime
    }
    db.travelreview.insert_one(doc)

    return jsonify({'msg': '리뷰 등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




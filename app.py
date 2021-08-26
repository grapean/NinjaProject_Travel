from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import datetime


@app.route('/')
def home():
    return render_template('index_home.html')

@app.route('/page')
def page():
    return render_template('index_page.html')

@app.route('/create')
def create():
    return render_template('index_create.html')

@app.route('/comment', methods=['GET'])
def read_reviews():
    comments = list(db.travel.find({}, {'_id': False}))
    return jsonify({'all_comments': comments})


@app.route('/page', methods=['POST'])
def test_post():
   user_name_receive = request.form['user_name_give']
   comment_receive = request.form['comment_give']

   today = datetime.now()
   mytime = today.strftime('%Y.%m.%d %H:%M')

   doc = {
       'user_name': user_name_receive,
       'comment': comment_receive,
       'data': mytime
   }

   db.travel.insert_one(doc)

   return jsonify({'msg': '댓글 작성 완료!'})


@app.route('/create', methods=['POST'])
def test_create():
    title_receive = request.form['title_give']
    season_receive = request.form['season_give']
    area_receive = request.form['area_give']
    keywords_receive = request.form['keywords_give']
    review_text_receive = request.form['review_text_give']

    today = datetime.now()
    subdata = today.strftime('%Y.%m.%d %H:%M')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{subdata}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'season': season_receive,
        'area': area_receive,
        'keywords': keywords_receive,
        'review_text': review_text_receive,
        'data': subdata,
        'file': f'{filename}.{extension}'
    }

    db.travelreview.insert_one(doc)

    return jsonify({'msg': '리뷰 등록 완료!'})


@app.route('/page', methods=['GET'])
def view_reviews():
    reviews = list(db.travelreview.find({}, {'_id': False}))
    return jsonify({'all_reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




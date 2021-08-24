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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




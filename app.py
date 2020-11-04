from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.traveldb


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('HTML.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])

def write_review():
    country_receive = request.form['country_give']
    city_receive = request.form['city_give']
    place_receive = request.form['place_give']
    address_receive=request.form['address_give']
    category_receive=request.form['category_give']
    comment_receive = request.form['comment_give']
    url_receive = request.form['url_give']

    # DB에 삽입할 review 만들기
    review = {
        'country': country_receive,
        'city': city_receive,
        'place' : place_receive,
        'address' : address_receive,
        'category' : category_receive,
        'comment': comment_receive,
        'url' : url_receive
    }

    # reviews에 review 저장하기
    db.reviews.insert_one(review)

    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '포스가 성공적으로 작성되었습니다.'})


@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
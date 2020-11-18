from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@54.180.85.97', 27017)
db = client.traveldb


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


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
        'ctegory' : category_receive,
        'comment': comment_receive,
        'url' : url_receive
    }

    db.reviews.insert_one(review)
    return jsonify({'result': 'success', 'msg': '포스트가 성공적으로 작성되었습니다.'})


@app.route('/review', methods=['GET'])
def read_reviews():
    reviews = list(db.reviews.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'reviews': reviews})


# 조회할 나라 정보 받아오고 조회하기.
@app.route('/search', methods=['GET'])
def search_reviews():
    country_receive = request.args.get('country_searched')
    print(country_receive)
    same_country = list(db.reviews.find({'country' : country_receive}, {'_id': 0}))

    return jsonify({'result': 'success', 'reviews': same_country})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
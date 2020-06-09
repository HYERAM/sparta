from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_order():
    # 1. 클라이언트가 준 name, size, qty, address, phone 가져오기.
    # 1-1. name_receive로 클라이언트가 준 name 가져오기
    name_receive = request.form['name_give']
    # 1-2. size_receive로 클라이언트가 준 size 가져오기
    size_receive = request.form['size_give']
    # 1-3. qty_receive로 클라이언트가 준 qty 가져오기
    qty_receive = request.form['qty_give']
    # 1-4. address_receive로 클라이언트가 준 address 가져오기
    address_receive = request.form['address_give']
    # 1-4. phone_receive로 클라이언트가 준 phone 가져오기
    phone_receive = request.form['phone_give']

    # 2. DB에 정보 삽입하기
    # 2-1. DB에 삽입할 order 만들기
    order = {
        'name' : name_receive,
        'size' : size_receive,
        'qty' : qty_receive,
        'address' : address_receive,
        'phone' : phone_receive
    }
    # 2-2. orders에 order 저장하기
    db.orders.insert_one(order)

	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result':'success', 'msg': '주문완료~! :)'})


@app.route('/orders', methods=['GET'])
def read_orders():
    # 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.orders.find({},{'_id':False}))
	# 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
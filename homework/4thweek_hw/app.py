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
    name_receive = request.form['name_give']
    size_receive = request.form['size_give']
    qty_receive = request.form['qty_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

# 2. DB에 정보 삽입하기
    # 2-1. 삽입할 dict 만들기
    doc = {
        'name' : name_receive,
        'size' : size_receive,
        'qty' : qty_receive,
        'address' : address_receive,
        'phone' : phone_receive
    }
    # 2-2. db에 삽입하기
    db.order.insert_one(doc)

    # 3. 성공여부 & 성공 메세지 반환하기
    return jsonify({'result':'success', 'msg': '주문완료!'})



@app.route('/orders', methods=['GET'])
def read_orders():
    orders = list(db.order.find({},{'_id':False}))
    return jsonify({'result':'success', 'orderlist': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
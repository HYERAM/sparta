from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


from datetime import datetime, timedelta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/tna/list', methods=['GET']) #스케쥴을 찾아 돌려준다.
def tna_list():
    # 1. tna 전체 목록을 검색. id 제외하고 date가 빠른 순으로 정렬하기.
    tna = list(db.justice_tna.find({},{'_id':False}).sort('due_date',1)) ## .sort() 부분 정리필요
    # 2. 성공하면 success 메시지와 함께 tna 목록을 클라이언트에 전달.
    return jsonify({'result': 'success','tna_list':tna})


@app.route('/tna/add', methods=['POST']) #스타일 넘버, 납기(ex-fty date)를 받아와서 6가지 스케쥴을 계산해서 DB에 추가 & 성공 메시지를 돌려준다.
def add_tna():
    # s_number_receive로 클라이언트가 준 title 가져오기
    s_number_receive = request.form['s_number_give']
    # ex_date_receive로 클라이언트가 준 author 가져오기
    ex_date_receive = request.form['ex_date_give']

    # 입력한 ex_date 기준으로 due 계산하기
    # 하나의 input으로 6가지 db를 저장해야하는데...
    # justice_tna에 tna 저장하기
    ExDate = datetime.strptime(ex_date_receive,'%Y-%m-%d')

    fit_due_receive = ExDate + timedelta(weeks=-8)
    tna1 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'FIT APPROVAL DUE',
    'due_date' : fit_due_receive
    }
    db.justice_tna.insert_one(tna1)

    thread_due_receive = ExDate + timedelta(days=-52)
    tna2 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'THREAD COLOR CFM DUE',
    'due_date' : thread_due_receive
    }
    db.justice_tna.insert_one(tna2)

    qc_due_receive = ExDate + timedelta(weeks=-7)
    tna3 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'QC FILE SENDING DUE',
    'due_date' : qc_due_receive
    } 
    db.justice_tna.insert_one(tna3)

    cut_date_receive = ExDate + timedelta(weeks=-5)
    tna4 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'CUT DATE',
    'due_date' : cut_date_receive
    } 
    db.justice_tna.insert_one(tna4)    

    top_due_receive = ExDate + timedelta(weeks=-2)
    tna5 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'TOP SAMPLE SENDING DUE',
    'due_date' : top_due_receive
    } 
    db.justice_tna.insert_one(tna5)

    test_due_receive = ExDate + timedelta(days=-10)
    tna6 = {
    's_number': s_number_receive,
    'ex_date': ex_date_receive,
    'schedule' : 'TEST SAMPLE SENDING',
    'due_date' : test_due_receive
    } 
    db.justice_tna.insert_one(tna6)
    
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': 'tna가 성공적으로 추가되었습니다.'})

@app.route('/tna/finish', methods=['POST']) #스타일 넘버, 스케쥴(due)을 받아와서 삭제 후 성공 메시지를 돌려 준다.
def delete_tna():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    s_number_receive = request.form['s_number_give']
    schedule_receive = request.form['schedule_give']

    # 2. mystar 목록에서 delete_one으로 s_number & schedule이 s_number_receive & schedule_receive와 일치하는 항목을 제거합니다.
    db.justice_tna.delete_one({'s_number':s_number_receive, 'schedule':schedule_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
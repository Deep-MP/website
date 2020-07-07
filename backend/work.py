#coding=utf-8
from flask import Flask,make_response,request,render_template,redirect,url_for, send_from_directory, send_file, jsonify
import requests
import pymysql
import json
from flask_cors import CORS
app = Flask(__name__)
db = pymysql.connect(host='localhost', user='root', password='975481DING!', db='deepmp', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
@app.route('/')
def index():
    return "Hello World"

@app.route('/get_data', methods=['get', 'post'])
def get_data():
    page = request.args.get('page', 1)
    page = int(page)
    venue = request.args.get('venue', 'NIPS').upper()
    sql = 'select arxiv_id, authors, citationVelocity, citations, fields, influence, paper_abstract, paper_title, topic, venue, year from semantic where venue like "%%{}%%" limit {}, 20'.format(venue, page * 20)
    cursor.execute(sql)
    data = []
    for line in cursor.fetchall():
        tmp_dic = {}
        tmp_dic["venue"] = line["venue"]
        tmp_dic["title"] = line["paper_title"]
        tmp_dic["abstract"] = line["paper_abstract"]
        tmp_dic["arxiv_id"] = line["arxiv_id"]
        tmp_dic["citations"] = line["citations"]
        tmp_dic["authors"] = line["authors"]
        tmp_dic["fields"] = line["fields"]
        tmp_dic["influence"] = line["influence"]
        tmp_dic["year"] = line["year"]
        tmp_dic["topic"] = line["topic"]
        data.append(tmp_dic)
    return jsonify({"result": data})

@app.route('/get_code', methods=['get', 'post'])
def get_code():
    title = request.args.get("title", "Less is more: sampling chemical space with active learning")
    sql = 'select * from github where paper_title like "%%{}%%"'.format(title)
    cursor.execute(sql)
    data = []
    for line in cursor.fetchall():
        tmp_dic = {}
        tmp_dic["addr"] = line["address"]
        tmp_dic["frame"] = line["frame"]
        tmp_dic["size"] = line["size"]
        tmp_dic["star"] = line["star"]
        tmp_dic["fork"] = line["fork"]
        tmp_dic["watch"] = line["watch"]
        tmp_dic["language"] = line["language"]
        tmp_dic["created"] = line["created_at"]
        tmp_dic["updated"] = line["updated_at"]
        tmp_dic["pre"] = line["pretrained_model"]
        data.append(line)
    return jsonify({"result": data})

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=5050, debug=True)

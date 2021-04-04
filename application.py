import boto3
from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import redis
from elasticapm.contrib.flask import ElasticAPM

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'sparta'
app.config['MYSQL_DATABASE_HOST'] = 'database-1.cgbie0k3ndqh.ap-northeast-2.rds.amazonaws.com'
mysql.init_app(app)

#redis
db = redis.Redis('redis-sparta.8imnfo.0001.apn2.cache.amazonaws.com')

#elasticsearch
app.config['ELASTIC_APM'] = {
        'SERVER_URL': 'https://search-elasticsearch-sparta-tedvy7ev365r74opwxg2eumxn4.ap-northeast-2.es.amazonaws.com',
        'DEBUG': True
    }
apm = ElasticAPM(app, logging=True)

@app.route('/')
def main():
    apm.capture_message('hello, world!')
    return "Hello, Backend"

@app.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    s3 = boto3.client('s3')
    s3.put_object(
        ACL="public-read",
        Bucket="myspartabucket",
        Body=file,
        Key=file.filename,
        ContentType=file.content_type)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("insert into file(file_name) value('"+file.filename+"')")
    cursor.execute("SELECT count(*) AS COUNT from file")
    data = cursor.fetchone()
    db.set("fileCount", data['COUNT'])
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

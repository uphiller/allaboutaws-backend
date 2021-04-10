import boto3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from flaskext.mysql import MySQL
import redis
from elasticapm.contrib.flask import ElasticAPM

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})
config_name = os.getenv('APP_ENV')

# MySQL configurations
mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = os.environ["MYSQL_DATABASE_USER"]
application.config['MYSQL_DATABASE_PASSWORD'] = os.environ["MYSQL_DATABASE_PASSWORD"]
application.config['MYSQL_DATABASE_DB'] = os.environ["MYSQL_DATABASE_DB"]
application.config['MYSQL_DATABASE_HOST'] = os.environ["MYSQL_DATABASE_HOST"]

# application.config['MYSQL_DATABASE_USER'] = "admin"
# application.config['MYSQL_DATABASE_PASSWORD'] = "12345678"
# application.config['MYSQL_DATABASE_DB'] = "sparta"
# application.config['MYSQL_DATABASE_HOST'] = "database-1.cgbie0k3ndqh.ap-northeast-2.rds.amazonaws.com"
mysql.init_app(application)

#redis
# db = redis.Redis('redis-sparta.8imnfo.0001.apn2.cache.amazonaws.com')
#
# #elasticsearch
# app.config['ELASTIC_APM'] = {
#         'SERVER_URL': 'https://search-elasticsearch-sparta-tedvy7ev365r74opwxg2eumxn4.ap-northeast-2.es.amazonaws.com',
#         'DEBUG': True
#     }
# apm = ElasticAPM(app, logging=True)

@application.route('/')
def main():
    return render_template("index.html")

@application.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
                      )
    s3.put_object(
        ACL="public-read",
        Bucket="myspartabucket",
        Body=file,
        Key=file.filename,
        ContentType=file.content_type
    )
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("insert into file(file_name) value('"+file.filename+"')")
    conn.commit()
#     cursor.execute("SELECT count(*) AS COUNT from file")
#     data = cursor.fetchone()
#     db.set("fileCount", data['COUNT'])
    return jsonify({'result': 'success'})

if __name__ == '__main__':
#     application.run('0.0.0.0', port=5000, debug=True)
    application.debug = True
    application.run()
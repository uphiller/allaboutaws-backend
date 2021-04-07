from flask import Flask, render_template, request, jsonify

application = Flask(__name__)

@application.route('/')
def main():
    return render_template("index.html")

@application.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    s3 = boto3.client('s3')
    s3.put_object(
        ACL="public-read",
        Bucket="myspartabucket",
        Body=file,
        Key=file.filename,
        ContentType=file.content_type)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)

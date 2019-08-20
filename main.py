import time
from flask import Flask, jsonify, request
app = Flask(__name__)

# example documents
documents = [
    {
        'documentTitle': "Einstein",
        "revisions": [
            {"timeStamp": "13:30", "content": "He loves Physics."},
            {"timeStamp": "14:05", "content": "He loves Mathematics."}
        ]
    },
    {
        'documentTitle': 'Marie Curie',
        "revisions": [
            { "timeStamp": "07:04", "content": "She loves Physics."},
            { "timeStamp": "22:00", "content": "Lorem ipsum"},
            { "timeStamp": "23:23", "content": "She loves Chemistry."}
        ]
    }
]


def test():
    # TODO
    assert get_latest("Einstein") == ""
    assert get_latest("Marie Curie") == ""


def get_time():
    result = time.localtime(time.time())
    mytime = ""
    if result.tm_hour < 10:
        mytime = mytime + ("0")
    mytime = str(result.tm_hour) + (":")
    if result.tm_min < 10:
        mytime = mytime + ("0")
    mytime = mytime + str(result.tm_min)
    return mytime


def title_does_exist(title):
    titles = [doc['documentTitle'] for doc in documents]
    return title in titles


def find_with_title(title):
    for doc in documents:
        if doc['documentTitle'] == title:
            return doc

    return None


@app.route('/GET/documents', methods=['GET'])
def get_titles():
    titles = [doc['documentTitle'] for doc in documents]
    return jsonify({'documentTitles': titles})


@app.route('/GET/documents/<title>', methods=['GET'])
def get_document(title):
    if not title_does_exist(title):
        return "Document with given title doesn't exist"

    revisions = [doc['revisions'] for doc in documents if doc['documentTitle'] == title]
    return jsonify({'revisions': revisions})


@app.route('/GET/documents/<title>/latest', methods=['GET'])
def get_latest(title):
    if not title_does_exist(title):
        return "Document with given title doesn't exist"

    all_revisions = [doc['revisions'] for doc in documents if doc['documentTitle'] == title]
    result = max(all_revisions[0], key=lambda x: x['timeStamp'])
    return jsonify({'latest revision': result})


@app.route('/GET/documents/<title>/<timestamp>', methods=['GET'])
def get_document_at_time(title, timestamp):
    if not title_does_exist(title):
        return "Document with given title doesn't exist"

    # TODO check if given timestamp is legal ([01-24]:[00:59]) and not duplicate
    # remove the colon(:) from timestamp and convert it to int
    int_time_stamp = int(timestamp.replace(':', ''))

    # get all revisions of the document with given title
    all_revisions = [doc['revisions'] for doc in documents if doc['documentTitle'] == title]

    # get the revisions of the document that were posted before the given timestamp
    earlier_revisions = [revision for revision in all_revisions[0] if int_time_stamp >= int(revision['timeStamp'].replace(':', ''))]

    if len(earlier_revisions) <= 0:
        return "No revision at that time"

    result = max(earlier_revisions, key=lambda x: x['timeStamp'])
    return jsonify({'revision at time': result})


@app.route('/POST/documents/<title>', methods=['POST'])
def create_revision(title):
    # I used an application called Postman to test this functionality

    #TODO Error Handling

    document = find_with_title(title)
    if document is not None:
        # if document exists create a revision
        revision = request.get_json()
        if revision is None:
            revision={}
        revision['timeStamp'] = get_time()
        document['revisions'].append(revision)
    else:
        # if document does not exist create a document
        document = {
            "documentTitle": title,
            "revisions": []
        }
        revision = request.get_json()
        if revision is None:
            revision={}
        revision['timeStamp'] = get_time()
        document['revisions'].append(revision)
        documents.append(document)

    return jsonify({'document': document}), 201


@app.route("/")
def home():
    #test()
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
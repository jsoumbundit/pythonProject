import json
import os

from flask import Flask
from flask import request
from flask import make_response

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("it-law-goku-firebase-adminsdk-z9vu2-0d1cfe95fd.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)

    # Accessing the fields on the POST request body of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]

    if intent == 'แนะนำตัว':
        doc_ref = db.collection(u'introduces').document(u'6oQu4KBGqxB0puXBMLa6')
        doc = doc_ref.get().to_dict()
        fullname = doc['fullname']
        speech = f'เป็น {fullname}'

    else :
        doc_ref = db.collection(intent).document(u'detail')
        doc = doc_ref.get().to_dict()
        description = doc['desp']
        speech = f'{description}'.replace('\\n','\n')

    #else:
    #    speech = "ผมไม่เข้าใจ คุณต้องการอะไร"

    res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):
    return {
        "fulfillmentText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)

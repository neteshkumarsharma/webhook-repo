from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import dateutil.parser

# Flask application instance
app = Flask(__name__)




# MongoDB client setup
# NOTE: set a proper MongoDB URI in MongoClient('uri') for production
client = MongoClient('')
db = client['WebHook']
collection = db['events']

@app.route('/')
def index():
    """Serves the UI.

    Renders `templates/index.html` which the frontend polls to display
    recent webhook events and aggregated stats.
    """
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receives GitHub webhooks and stores them in MongoDB.

    Handles `push` and `pull_request` events; other events are ignored.
    """
    # Parse incoming JSON payload and GitHub event header
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Prepared document to persist to MongoDB
    document = {
        "request_id": None,
        "author": None,
        "action": None,
        "from_branch": None,
        "to_branch": None,
        "timestamp": None
    }

    try:
        if event_type == 'push':
            
            document['action'] = "PUSH"
            document['request_id'] = data['head_commit']['id'] 
            document['author'] = data['pusher']['name']
            document['to_branch'] = data['ref'].split('/')[-1] 
            
            dt = dateutil.parser.isoparse(data['head_commit']['timestamp'])
            document['timestamp'] = dt.strftime("%Y-%m-%d %H:%M:%S UTC")

        elif event_type == 'pull_request':
            
            if data['action'] == 'closed' and data['pull_request']['merged']:
                document['action'] = "MERGE"
                document['timestamp'] = dateutil.parser.isoparse(data['pull_request']['merged_at']).strftime("%Y-%m-%d %H:%M:%S UTC")
            
            
            elif data['action'] == 'opened':
                document['action'] = "PULL_REQUEST"
                document['timestamp'] = dateutil.parser.isoparse(data['pull_request']['created_at']).strftime("%Y-%m-%d %H:%M:%S UTC")
            
            else:
                return jsonify({"status": "ignored", "reason": "action not tracked"}), 200

            document['request_id'] = str(data['pull_request']['id'])
            document['author'] = data['pull_request']['user']['login']
            document['from_branch'] = data['pull_request']['head']['ref']
            document['to_branch'] = data['pull_request']['base']['ref']

        else:
            return jsonify({"status": "ignored", "reason": "event not tracked"}), 200

        collection.insert_one(document)
        return jsonify({"status": "success"}), 200

    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key: {str(e)}"}), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    """API for the UI to poll recent events.

    Returns a JSON list of stored events (most recent first). The MongoDB
    `_id` field is excluded to simplify frontend rendering.
    """
    events = list(collection.find({}, {'_id': 0}).sort('_id', -1))
    return jsonify(events)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API to get aggregated event statistics.

    Returns counts for total events and each tracked action type.
    """
    try:
        total_events = collection.count_documents({})
        push_count = collection.count_documents({'action': 'PUSH'})
        pr_count = collection.count_documents({'action': 'PULL_REQUEST'})
        merge_count = collection.count_documents({'action': 'MERGE'})

        return jsonify({
            'total': total_events,
            'push': push_count,
            'pull_request': pr_count,
            'merge': merge_count
        })
    except Exception as e:
        # Return a 500 with the error for debugging; consider logging in production
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Development server: debug enabled, listening on port 5000
    app.run(debug=True, port=5000)
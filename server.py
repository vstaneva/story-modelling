import flask
import glob
import json
import pprint

app = flask.Flask(__name__)

def get_all_filenames(dir_name):
    return glob.glob(dir_name+"/*.json")

def get_last_log():
    filenames = get_all_filenames("logs")
    tmstamps = [(i,name[5:-5]) for (i,name) in enumerate(filenames)]
    latest_tmst = max(tmstamps, key = lambda x:x[1])
    return filenames[latest_tmst[0]]

def get_tmst_from_log_name(log_name):
    return log_name[5:-5]
def get_log_name_from_tmst(tmst):
    return "logs/"+tmst+".json"

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/example')
def student():
    return "STUDENT"

@app.route('/printlog/<log_id>')
def display_log(log_id):
    log_name = get_log_name_from_tmst(log_id)
    with open(log_name) as log:
        json_data = json.load(log)
        # pretty_out = pprint.pformat(json.loads(json_data),indent=2,width=40)
        return flask.jsonify(json_data)

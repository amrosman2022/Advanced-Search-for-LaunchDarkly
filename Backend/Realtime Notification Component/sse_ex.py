from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__)
CORS(app)
global g_a_Messages
g_a_Messages = [['message','flag', 'env', 'proj', 'done', 'error', 'time'],['','0', '0', '0', 'False', 'False', '']] # please update note in es_pushSSE

@app.route('/update_status')
def func_updateMessages():
    try:
        sItemName = request.args.get("itemname")
        sValue = request.args.get("value")
        g_a_Messages[1][g_a_Messages[0].index(sItemName)] = sValue
        return  {"error": False}
    except:
        return {"error": True}

@app.route('/clear_status')
def func_clearMessages():
    global g_a_Messages
    g_a_Messages = [['message','flag', 'env', 'proj', 'done', 'error', 'time'],['','0', '0', '0', 'False', 'False', '']]
    return  {"error": False}

def func_getMessage():
    '''this could be any function that blocks until data is ready'''
    #time.sleep(1.0)
    try:
        if len(g_a_Messages) > 0:
            s_message = g_a_Messages[1][g_a_Messages[0].index('message')]
            n_prjStat = g_a_Messages[1][g_a_Messages[0].index('proj')]
            n_envStat = g_a_Messages[1][g_a_Messages[0].index('env')]
            n_ffStat = g_a_Messages[1][g_a_Messages[0].index('flag')]
            b_doneStat = g_a_Messages[1][g_a_Messages[0].index('done')]
            b_errStat = g_a_Messages[1][g_a_Messages[0].index('error')]
            s_nowTime = str(time.ctime())

            s_Stat = '{"proj": "%s", "env": "%s", "flag": "%s", "done": "%s", "error": "%s", "time": "%s", "message": "%s"}' %(n_prjStat, n_envStat, n_ffStat, b_doneStat, b_errStat,s_nowTime,s_message)
        else:
            s_Stat = {"error": True}
    except:
        s_Stat = {"error": True}
    return s_Stat

@app.route('/')
def root():
    return "index.html"

def generate_data():
    _data = format(func_getMessage())
    yield f"id: 1\ndata: {_data}\nevent: status\n\n"

#@app.route('/stream_status')
#def stream():
 #   def eventStream():
 #       _data = format(func_getMessage())
 #       yield f"id: 1\ndata: {_data}\nevent: status\n\n"
    
 #   return Response(eventStream(), mimetype="text/event-stream")


@app.route('/events')
def events():
    return Response(generate_data(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=False,port=5050, host='0.0.0.0')
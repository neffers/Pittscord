# imports
from quart import Quart, render_template, session, request, redirect, url_for, abort
import grpc
import json
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2

from config import grpc_address

app = Quart(__name__)

app.secret_key = "secret"

# try/catch helper method to get the json from the Discord server
async def get_json_from_server(admin_name):
    try:
        async with grpc.aio.insecure_channel(grpc_address) as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.GetJSON(Pittscord_ipc_pb2.JSONRequest(admin_name=admin_name))
        return response.json
    except grpc.aio.AioRpcError as e:
        print(e)
        return None

# show login screen
@app.route('/', methods=['GET', 'POST'])
async def default():
    session.clear()
    if request.method == 'POST':
        form = await request.form
        # assign session admin to the username entered into the form
        session['admin'] = form['username']
        # go to config ui
        return redirect(url_for('ui'))
    # show login screen
    return await render_template('login.html')

# show config ui
@app.route("/ui")
async def ui():
    if not session.get('admin'):
        # show login
        return redirect(url_for('default'))
    # show config ui
    return await render_template("ui.html")

# try to recieve the config admin created
@app.route("/config", methods=["POST"])
async def recv_config():
    config = await request.json
    config['admin'] = session['admin']
    try:
        async with grpc.aio.insecure_channel(grpc_address) as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.SendConfig(Pittscord_ipc_pb2.ConfigRequest(config=json.dumps(config)))
        return [response.code]
    except grpc.aio.AioRpcError as e:
        print(e)
        return abort(500)

# get the json from the Discord server
@app.route("/get_server_json")
async def get_json():
    ret = await get_json_from_server(session['admin'])
    if ret:
        return json.loads(ret)
    else:
        return abort(500)

# send cleanup request to Discord bot (so bot can delete all the channels it has made off of the server)
@app.route("/cleanup", methods=["DELETE"])
async def cleanup():
    try:
        async with grpc.aio.insecure_channel(grpc_address) as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.Cleanup(Pittscord_ipc_pb2.CleanupRequest(admin_name=session['admin']))
        return [response.code]
    except grpc.aio.AioRpcError as e:
        print(e)
        return abort(500)

# display Discord icon
@app.route("/favicon.ico")
async def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

# run website (main method)
if __name__ == "__main__":
    app.run()

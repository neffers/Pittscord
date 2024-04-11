from quart import Quart, render_template, session, request, redirect, url_for, abort
import grpc
import json
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2

from config import admin_pitt_id, grpc_address

app = Quart(__name__)

app.secret_key = "secret"


async def get_json_from_server(admin_name):
    try:
        async with grpc.aio.insecure_channel(grpc_address) as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.GetJSON(Pittscord_ipc_pb2.JSONRequest(admin_name=admin_name))
        return response.json
    except grpc.aio.AioRpcError as e:
        print(e)
        return None


@app.route('/')
async def default():
    # wanted this to come from a login page but ran out of time
    session['admin'] = admin_pitt_id
    return redirect(url_for('ui'))


@app.route("/ui")
async def ui():
    return await render_template("ui.html")


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


@app.route("/get_server_json")
async def get_json():
    ret = await get_json_from_server(session['admin'])
    if ret:
        return json.loads(ret)
    else:
        return abort(500)


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


if __name__ == "__main__":
    app.run()

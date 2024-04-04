from quart import Quart, render_template, session, request, redirect, url_for
import grpc
import json
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2

app = Quart(__name__)

app.secret_key = "secret"


async def get_json_from_server(server_id):
    try:
        async with grpc.aio.insecure_channel('[::]:50051') as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.GetJSON(Pittscord_ipc_pb2.JSONRequest(admin_name=session['admin']))
        return response.json
    except grpc.aio.AioRpcError:
        return None


@app.route('/')
async def default():
    # In reality, get from a login
    session['admin'] = 'jbb65'
    return redirect(url_for('ui'))


@app.route("/ui")
async def ui():
    return await render_template("example.html")


@app.route("/config", methods=["POST"])
async def recv_config():
    config = await request.json
    config['admin'] = session['admin']
    try:
        async with grpc.aio.insecure_channel('[::]:50051') as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.SendConfig(Pittscord_ipc_pb2.ConfigRequest(config=json.dumps(config)))
        return [response.code]
    except grpc.aio.AioRpcError:
        return 500


@app.route("/get_server_json")
async def get_json():
    # TODO: get from database based on login? or should this be sending the admin name instead?
    # Probably the second
    server = 1204258474851041330
    ret = await get_json_from_server(server)
    return json.loads(ret)


@app.route("/cleanup", methods=["DELETE"])
async def cleanup():
    return 200


if __name__ == "__main__":
    app.run()

from quart import Quart, render_template, session
import grpc
import json
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2

app = Quart(__name__)

app.secret_key = "secret"


async def get_json_from_server(server_id):
    try:
        async with grpc.aio.insecure_channel('[::]:50051') as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.GetJSON(Pittscord_ipc_pb2.JSONRequest(server_id=server_id))
        return response.json
    except grpc.aio.AioRpcError:
        return None


@app.route("/")
async def default():
    # In reality, get from a login
    session['server'] = 1204258474851041330
    return await render_template("example.html")


@app.route("/config", methods=["POST"])
async def recv_config():
    return {}


@app.route("/get_server_json")
async def get_json():
    ret = await get_json_from_server(session['server'])
    return json.loads(ret)


if __name__ == "__main__":
    app.run()

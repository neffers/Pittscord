from quart import Quart

import grpc
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2


async def do_hello() -> None:
    async with grpc.aio.insecure_channel('[::]:50051') as channel:
        stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
        response = await stub.SayHello(Pittscord_ipc_pb2.HelloRequest())


app = Quart(__name__)


@app.route("/")
async def default():
    await do_hello()
    return ""


if __name__ == "__main__":
    app.run()

from quart import Quart

import grpc
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2


async def do_hello() -> str:
    try:
        async with grpc.aio.insecure_channel('[::]:50051') as channel:
            stub = Pittscord_ipc_pb2_grpc.Pittscord_ipcStub(channel)
            response = await stub.SayHello(Pittscord_ipc_pb2.HelloRequest())
        return "Success"
    except grpc.aio.AioRpcError:
        return "Failure"


app = Quart(__name__)


@app.route("/")
async def default():
    ret = await do_hello()
    return ret


if __name__ == "__main__":
    app.run()

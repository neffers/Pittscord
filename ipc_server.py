import grpc

from bot import bot
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2


class PittscordIpcServer(Pittscord_ipc_pb2_grpc.Pittscord_ipcServicer):
    def __init__(self):
        self.bot = bot

    async def GetJSON(
            self,
            request: Pittscord_ipc_pb2.JSONRequest,
            context: grpc.aio.ServicerContext
    ) -> Pittscord_ipc_pb2.JSONResponse:
        json = self.bot.generate_server_json(request.server_id)
        response = Pittscord_ipc_pb2.JSONResponse(json=json)
        return response

    async def SayHello(
            self,
            request: Pittscord_ipc_pb2.HelloRequest,
            context: grpc.aio.ServicerContext
    ):
        await self.bot.say_hello()
        return Pittscord_ipc_pb2.HelloResponse()

    async def SendConfig(
            self,
            request: Pittscord_ipc_pb2.ConfigRequest,
            context: grpc.aio.ServicerContext
    ):
        response_code = await self.bot.process_semester_config(request.config)
        return Pittscord_ipc_pb2.ConfigResponse(code=response_code)

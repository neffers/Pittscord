import grpc

from bot import bot
from rpc import Pittscord_ipc_pb2_grpc, Pittscord_ipc_pb2
from config import grpc_address


class PittscordIpcServer(Pittscord_ipc_pb2_grpc.Pittscord_ipcServicer):
    def __init__(self):
        self.bot = bot

    async def GetJSON(
            self,
            request: Pittscord_ipc_pb2.JSONRequest,
            context: grpc.aio.ServicerContext
    ) -> Pittscord_ipc_pb2.JSONResponse:
        admin_name = request.admin_name
        server_id = self.bot.db.get_admin_server(admin_name)
        json = self.bot.generate_server_json(server_id)
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

    async def Cleanup(
            self,
            request: Pittscord_ipc_pb2.CleanupRequest,
            context: grpc.aio.ServicerContext
    ):
        admin_name = request.admin_name
        server_id = self.bot.db.get_admin_server(admin_name)
        response_code = await self.bot.semester_cleanup(server_id)
        return Pittscord_ipc_pb2.CleanupResponse(code=response_code)


async def launch(discord_token):
    server = grpc.aio.server()
    ipc_server = PittscordIpcServer()
    Pittscord_ipc_pb2_grpc.add_Pittscord_ipcServicer_to_server(ipc_server, server)
    listen_addr = grpc_address
    server.add_insecure_port(listen_addr)
    print("starting rpc server")
    await server.start()
    print("starting discord bot")
    await ipc_server.bot.start(discord_token)


if __name__ == '__main__':
    import asyncio
    from secret import discord_token as token

    asyncio.run(launch(token))

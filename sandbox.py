import asyncio
import grpc
import multiprocessing
import signal

from secret import discord_token
from rpc import Pittscord_ipc_pb2_grpc
from ipc_server import PittscordIpcServer
import web


def sigint_handler(sig, frame):
    print("Caught ctrl+c, terminating processes")
    bot_process.terminate()
    web_process.terminate()


async def launch_ipc_server(token) -> None:
    server = grpc.aio.server()
    ipc_server = PittscordIpcServer()
    Pittscord_ipc_pb2_grpc.add_Pittscord_ipcServicer_to_server(ipc_server, server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    print("starting rpc server")
    await server.start()
    print("starting discord bot")
    await ipc_server.bot.start(token)


def start_server(token):
    asyncio.run(launch_ipc_server(token))


if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=start_server, args=(discord_token,))
    web_process = multiprocessing.Process(target=web.app.run, args=())

    bot_process.start()
    web_process.start()

    signal.signal(signal.SIGINT, sigint_handler)

    web_process.join()
    bot_process.join()

from quart import Quart


app = Quart(__name__)


@app.route("/")
async def default():
    return ""


if __name__ == "__main__":
    app.run()

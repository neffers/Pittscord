# WHAT YOU WILL SEE IN EACH FILE
Hello! 
Glad to see a new semester's team pick up Pittscord.
Seán here, I mostly worked on the CSS and a bit of the HTML for this project.
Also some comments and documentation :)

Here's a rundown of what you will see in most of these files and directories:
## Directories
- `logs`
  - The default directory for the bot to store logs of deleted channels
- `rpc`
  - `__init__.py`
    - An empty file that serves to make python think of the `rpc` directory as a module, so that imports are a little cleaner and the generated files don't clutter the already cluttered base directory.
  - `Pittscord_ipc.proto`
    - The definitions for the RPC functions, argument and return types. If you're adding functionality to the UI, you will probably need to mess with this, but otherwise you should be able to leave it as-is.
  - Other Files
    - These are generated files and shouldn't be modified. If you need to change the protocol, you'll need to re-generate them.
      - For more information on that, see the [documentation](https://grpc.io/docs/languages/python/basics/)
      - Basically, make sure you have `grpcio-tools` installed and run `python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. Pittscord_ipc.proto` in the rpc directory. You will need to make sure the `..._pb2_grpc.py` file says `from . import ...`though.
- `static`
    - 'static' (non-templated) files for the webserver.
- `templates`
    - html files for the webserver to serve.
## Files
- `.gitignore`
  - standard practice to stop certain things getting uploaded to the remote repository
- `bot.py`
  - The actual discord bot logic, implemented using the [discord.py](https://discordpy.readthedocs.io/en/stable/index.html) library
  - Creates an instance of the `database.py`'s Database class to use.
  - Also creates an instance of the `canvas.py`'s Canvas class to use.
- `canvas.py`
  - A simple module that pretty much runs off a single method to fetch courses from
  - Uses the python [CanvasAPI](https://canvasapi.readthedocs.io/en/stable/getting-started.html) library.
- `config.py`
  - Various configuration options for the application
- `database_useful_test.py`
  - A simulation of the database calls made by the bot. Could potentially be removed.
- `database.py`
  - A module for managing the database connection and facilitating simple calls to the SQLite database in other modules.
- `EXPLANATION_of_files.md`
  - You're looking at it
- `ipc_server.py`
  - The module which instantiates and runs the grpc server. This also runs the discord bot, such that the rpc server can call functions on it.
  - There is probably a more elegant way of implementing this.
- `LICENSE`
  - self-explanatory
- `README.md`
  - The readme.
- `requirements.txt`
  - Generated with `pip freeze > requirements.txt` in the venv. A list of required libraries and their versions.
- `run_both.py`
  - A script which will run both the ipc server and webserver by using python's multiprocessing.
  - Might not work on all platforms
- `secret.example.py`
  - An example file to demonstrate what should be in `secret.py` (see below)
- `secret.py`
  - Not included in the repo, but you should copy `secret.example.py` and put your actual bot and canvas tokens in there.
- `web.py`
  - A simple webserver implemented in [quart](https://palletsprojects.com/p/quart/) (an async version of [flask](https://flask.palletsprojects.com/en/3.0.x/))
  - Serves as the Web interface for the bot's semester configuration capabilities.
  - Utilizes files in `/static/` and `/templates/`

# Development next steps
Short of adding new features (and perhaps even before you do that) I believe the most important thing you could do would be to carefully go through `bot.py` and make it more robust.
Adding real error handling and proper logging would be the top of my wishlist.
If you're feeling brave, catching errors halfway through things like the `/configure_server` or semester configuration actions and undoing what's been done so far would be impressive.

I'm afraid we've left some things in a half-finished state.
Most notably, we began with an intention of supporting more than one professor's discord server, but that proved to be beyond the scope of our capabilities.
However, nearly all that would need to be done would be putting the professor's canvas token in the database, although I don't know how good an idea that is realistically.

# The End
Good luck, from the first semester Pittscord team: Jordan Brudenell, Seán O'Rourke, and Foster Stravino!
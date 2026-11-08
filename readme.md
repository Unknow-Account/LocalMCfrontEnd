## What is this?

This is a website with a flask backend server for my minecraft sever!
It uses mainly uses a API and your server Stat folder for its main functions!


## Features!

1: Player Count Tracking + graph making

2: Player can see in detailed data about their stats, like block placed, and more!

3: Simple Yet Complex: Easily Expandable to add more features!

4: Flask backend for simple python editing!

5: And much much more!

## How to set up

WINDOWS:

In a CMD PROMPT:

cd C:\path\to\folder\containing\this\repo\

venv\Scripts\activate

pip install flask waitress

pip install flask-caching flask-limiter matplotlib apscheduler requests

waitress-serve --host=127.0.0.1 --port=5000 py:app
    ^NOTE: Edit as needed


I so not know if any other OS's work, as I do not have access to them. if any issues let me know!

After:

Go into py.py and fill in serverIP, Stats_Folder, and CSVFile!


## How to launch and shutdown

Launch:

cd C:\path\to\folder\containing\this\repo\

venv\Scripts\activate

waitress-serve --host=127.0.0.1 --port=5000 py:app

Shutdown:

Ctrl+C on the temerinal.

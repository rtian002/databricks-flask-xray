from flask import Flask,redirect
import os
import main

if main.WEB_ARGO_AUTH:
    main.create_web_tunnel()
else:
    main.run_start()

app = Flask(__name__)

@app.route("/")
def home():
    #return "TEST: Hello World from Flask in a uWSGI Nginx Docker container with Python ..."
    return app.send_static_file("index.html")

@app.route("/start")
def start():
    main.run_start()
    os.system("sleep 5")
    return redirect("/sub-status")

@app.route("/stop")
def stop():
    main.run_stop()
    os.system("sleep 2")
    return redirect("/sub-status")

@app.route("/sub-status")
def status():
    results=main.get_links()
    return results
    
@app.route('/<path:path>')
def catch_all(path):
    SUB_PATH=main.SUB_PATH
    if path==SUB_PATH:
        results=main.get_links(0)
        return results
    else:
        return app.send_static_file("index.html")
    
if __name__ == "__main__":
    app.run()

from flask import render_template, request, Blueprint

webui_bp = Blueprint("webui", __name__)

# ----------------------R O U T E S-----------------------
@webui_bp.route("/")
def home():
    return render_template('index.html')

@webui_bp.route("/about")
def about():
    return render_template('about.html')

@webui_bp.route("/explore")
def explore():
    return render_template('explore.html')
    
@webui_bp.route("/docs")
def docs():
    return render_template('docs.html')

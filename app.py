from image_processing import *
from flask import Flask,request,redirect, send_from_directory, render_template, url_for
import os

#config vars
UPLOAD_FOLDER = os.getcwd()

#todo: add watermarking: http://code.activestate.com/recipes/362879-watermark-with-pil/

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)
    
@app.route("/exif_processing",methods=["GET","POST"])
def exif_processing():
    if request.method == 'POST':
        img = request.files.get("image")
        if exif_preserve(img) == "no exif":
            tags = "No exif data to be found"
        else:
            tags = exif_enumerate(img.filename)
        if request.form.get("stripped")=="stripped":
            new_file = exif_strip(img.filename)
            return redirect(url_for('download',filename=new_file))
        else:
            return render_template("exif.html",exif_data=tags)
    return render_template("exif.html")

@app.route("/stego_processing",methods=["GET","POST"])
def stego_processing():
    if request.method=="POST":
        img = request.files.get("image")
        data = request.form.get("data")
        img.save(img.filename)
        if request.form.get("hide_retrieve") == "hide":
            new_file = hide_data(img.filename,data)
            return redirect(url_for("download",filename=new_file))
        if request.form.get("hide_retrieve") == "retrieve":
            retrieved_data = retrieve_data(img.filename)
            return render_template("stego.html",retrieved_data=retrieved_data)
    return render_template("stego.html")
            
app.run(debug=True)

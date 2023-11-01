from datetime import datetime
import hashlib
import os
import pathlib
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["UPLOAD_FOLDER"] = "static/upload/video"

db = SQLAlchemy()
db.init_app(app)

class MovieORM(db.Model):
    __tablename__ = "movie"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.String(255), nullable=False)
    m3u8_url = sa.Column(sa.String(255), nullable=True)
    create_at = sa.Column(sa.DATETIME, default=datetime.now)

@app.cli.command()
def create():
    db.drop_all()
    db.create_all()

@app.route("/")
def home():
    q = db.select(MovieORM)
    movie_list = db.session.execute(q).scalars()
    return render_template("index.html", movie_list=movie_list)

@app.route("/upload_movie")
def upload_movie():
    return render_template("video_upload.html")

@app.post("/video_upload")
def upload_movie2():
    file = request.files["file"]
    if file:
        filename = file.filename
        content = file.read()
        hex_name = hashlib.md5(content).hexdigest()
        suffix = pathlib.Path(filename).suffix
        new_filename = hex_name + suffix
        print("new_filename", new_filename)

        upload_dir = pathlib.Path(app.config["UPLOAD_FOLDER"])
        new_path = upload_dir.joinpath(new_filename)
        open(new_path, mode="wb").write(content)

        m3u8_path = upload_dir.parent.joinpath("m3u8")
        if not m3u8_path.exists():
            m3u8_path.mkdir()
        current_dir = m3u8_path.joinpath(hex_name)
        if not current_dir.exists():
            current_dir.mkdir()
        
        cli1 = f"ffmpeg -y -i {new_path} -vcodec copy -acodec copy -bsf:v h264_mp4toannexb {str(current_dir)}/index.ts"
        os.system(cli1)
        cli2 = f'ffmpeg -i {str(current_dir)}/index.ts -c copy -map 0 -f segment -segment_list {str(current_dir)}/index.m3u8 -segment_time 10 "{str(current_dir)}/index-%04d.ts"'
        os.system(cli2)

        mv = MovieORM()
        mv.url = ("/" + str(new_path))
        mv.name = filename
        mv.m3u8_url = ("" + str(current_dir) + "/index.m3u8")
        db.session.add(mv)
        db.session.commit()

    return {"code": 0, "msg": "上传视频成功"}

@app.route("/video_view")
def video_view():
    vid = request.args.get("video_id")
    video = MovieORM.query.get(vid)
    return render_template("video_view.html", url=video.m3u8_url.replace('\\', '/'))

if __name__ == "__main__":
    app.run(debug=True)
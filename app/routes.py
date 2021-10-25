from flask import current_app as app, render_template, jsonify
from app.models import Post, Kekambas

@app.route('/')
@app.route('/index')
def index():
    context = {
        'title': 'Kekambas Blog | HOME',
        'posts': Post.query.order_by(Post.date_created.desc()).all()
    }
    return render_template('index.html', **context)

@app.route('/kekambas')
def kekambas():
    students = Kekambas.query.all()
    return jsonify([s.to_dict() for s in students])
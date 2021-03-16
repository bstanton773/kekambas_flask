from . import bp as blog
from flask import request, redirect, url_for, jsonify, render_template
from app import db
from flask_login import login_required, current_user
from .forms import PostForm
from app.models import Post


@blog.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    title = "Kekambas Blog | CREATE POST"
    post = PostForm()
    if request.method == 'POST' and post.validate():
        post_title = post.title.data
        content = post.content.data
        user_id = current_user.id
        # print(post_title, content)
        # Create new Post instance
        new_post = Post(post_title, content, user_id)
        # Add new post instance to database
        db.session.add(new_post)
        # Commit
        db.session.commit()
        # flash a message
        flash("You have successfully created a post!", 'success')
        # redirect back to create post
        return redirect(url_for('createpost'))
    return render_template('create_post.html', post=post, title=title)


@blog.route('/myposts')
@login_required
def myposts():
    title = "Kekambas Blog | MY POSTS"
    posts = current_user.posts
    return jsonify([p.to_dict() for p in posts])
    # return render_template('my_posts.html', title=title, posts=posts)


@blog.route('/myposts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    title = f"Kekambas Blog | {post.title.upper()}"
    return render_template('post_detail.html', post=post, title=title)


@blog.route('/myposts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()
    if post.author.id != current_user.id:
        flash("You cannot update another user's post", 'danger')
        return redirect(url_for('myposts'))
    if request.method == 'POST' and update_form.validate():
        post_title = update_form.title.data
        content = update_form.content.data

        post.title = post_title
        post.content = content

        db.session.commit()
        flash("Your post has been updated.", 'info')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_update.html', form=update_form, post=post)


@blog.route('/myposts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash("You cannot delete another user's post", 'danger')
        return redirect(url_for('myposts'))
    db.session.delete(post)
    db.session.commit()
    flash("This post has been deleted", 'info')
    return redirect(url_for('index'))
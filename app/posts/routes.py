from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user,  login_required
from app import db
from app.models import Post
from .forms import PostForm

from . import posts

@posts.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('/posts/create_post.html', title="New Post", form=form, legend='New Post')


@posts.route('/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/post.html', title=post.title, post=post)


@posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('/posts/create_post.html', title="Update Post", form=form, legend='Update Post')


@posts.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))


@posts.route('/angular/allposts', methods=['GET'])
@login_required
def spa_allposts():
    return render_template('/posts/angular_allposts.html', title="Posts using angular")
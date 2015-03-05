# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, abort, redirect, url_for, request, flash, \
    current_app, make_response
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, PostForm, CommentForm
from .. import db
from ..models import User, Post, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    # pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['POSTS_PER_PAGE'],
    #     error_out=False)
    # posts = pagination.items
    # # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html', form=form, posts=posts, pagination=pagination)
    show_followed = False
    if current_user.is_authenticated():
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/user/<username>')
def user(username):
    usr = User.query.filter_by(username=username).first()
    if usr is None:
        abort(404)
    posts = usr.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=usr, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的用户资料已经更新！')
        return redirect(url_for('.user', username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post_id = Post.query.get_or_404(id)
    if current_user != post_id.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_id.body = form.body.data
        db.session.add(post_id)
        flash(u'博客已经更新！')
        return redirect(url_for('.post', id=post_id.id))
    form.body.data = post_id.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效的用户名！')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash(u'你已经关注了该用户！')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash(u'你关注了 %s。' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效的用户名！')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash(u'你还没有关注该用户！')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash(u'你已经取消关注 %s。' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效的用户名！')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
                for item in pagination.items]
    return render_template('followers.html', user=user, title=u'关注者列表',
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u'被关注者列表',
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'你评论了这篇博客！')
        return redirect(url_for('.post', id=post.id, page=-1))  # -1表示最后一页
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)
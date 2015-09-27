from chores.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from datetime import datetime


# Create your views here.

from chores.models import Blog, Category, Comment


def index(request):

    categories = category_count()
    posts = Blog.objects.filter(published='True')
    top3posts = Blog.objects.filter(published='True')[:3]
    next3posts = Blog.objects.filter(published='True')[3:6]
    search_form = SearchForm()

    return render_to_response('index.html', {
        'categories': categories,
        'posts': posts,
        'top3posts': top3posts,
        'next3posts': next3posts,
        'search_form': search_form,
        },
        context_instance=RequestContext(request)
    )


def view_post(request, slug):
    post = get_object_or_404(Blog.objects.filter(slug=slug))
    comments = Comment.objects.filter(blog_id=post.id)
    user = request.user

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('view_post', args=[post.slug]))

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog_id = post.id
            new_comment.user = request.user
            new_comment.save()

        return HttpResponseRedirect(reverse('view_post', args=[post.slug]))

    if post.published:
        categories = category_count()
        posts = Blog.objects.filter(published='True')
        form = CommentForm()

        return render_to_response(
            'view_post.html', {
                'post': post,
                'comments': comments,
                'form': form,
                'categories': categories,
                'posts': posts,
            },
            context_instance=RequestContext(request)
        )
    else:
        if user.is_superuser:
            categories = category_count()
            posts = Blog.objects.filter(published='True')
            form = CommentForm()

            return render_to_response(
                'view_post.html', {
                    'post': post,
                    'comments': comments,
                    'form': form,
                    'categories': categories,
                    'posts': posts,
                },
                context_instance=RequestContext(request)
            )

        else:
            # this is the same code as in the index view. Can just call index view instead?
            categories = category_count()
            posts = Blog.objects.filter(published='True')
            top3posts = Blog.objects.filter(published='True')[:3]
            next3posts = Blog.objects.filter(published='True')[3:6]

            return render_to_response('index.html', {
                'categories': categories,
                'posts': posts,
                'top3posts': top3posts,
                'next3posts': next3posts,
                },
                context_instance=RequestContext(request)
            )


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categoryposts = Blog.objects.filter(category=category).filter(published='True')
    categories = category_count()
    posts = Blog.objects.filter(published='True')

    return render_to_response('view_category.html', {
        'category': category,
        'categoryposts': categoryposts,
        'categories': categories,
        'posts': posts,
    },

        context_instance=RequestContext(request)
    )


@login_required()
def edit_category(request, slug):

    if request.method == 'POST':

        if slug == 'newcategory':
            form = CategoryForm(request.POST)
        else:
            form = CategoryForm(request.POST, instance=Category.objects.get(slug=slug))

        if form.is_valid():
            formcategory = form.save(commit=False)
            formcategory.save()
        return HttpResponseRedirect(reverse('index',))

    else:
        if slug == 'newcategory':
            form = CategoryForm()
        else:
            post = Category.objects.get(slug=slug)
            form = CategoryForm(instance=post)

    return render_to_response('edit_category.html', {
        'form': form},
        context_instance=RequestContext(request))


@login_required()
def profile(request, slug):

    user = request.user

    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            formpost = form.save(commit=False)
            formpost.user = request.user
            formpost.edited = datetime.now()
            formpost.save()
        return HttpResponseRedirect(reverse('profile', args=[request.user]))

    else:
        form = BlogForm()

    posts = Blog.objects.filter(user_id=user.id)
    comments = Comment.objects.filter(user_id=user.id)

    return render_to_response('profile.html', {
        'posts': posts,
        'comments': comments,
        'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required()
def generate_post_form(request, slug):

    if request.method == 'POST':

        if slug == 'newpost':
            form = BlogForm(request.POST)

            if form.is_valid():
                formpost = form.save(commit=False)
                formpost.user = request.user
                formpost.edited = datetime.now()
                formpost.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user]))
        else:
            form = BlogForm(request.POST, instance=Blog.objects.get(slug=slug))

            if form.is_valid():
                formpost = form.save(commit=False)
                formpost.user = request.user
                formpost.edited = datetime.now()
                formpost.save()

            post = Blog.objects.get(slug=slug)
            form = BlogForm(instance=post)

            return form

    else:
        if slug == 'newpost':
            form = BlogForm()
        else:
            post = Blog.objects.get(slug=slug)
            form = BlogForm(instance=post)
        return form


@login_required()
def edit_post(request, slug):
    # form = generate_post_form(request, slug)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=Blog.objects.get(slug=slug))

        if form.is_valid():
            formpost = form.save(commit=False)
            formpost.user = request.user
            formpost.edited = datetime.now()
            formpost.save()

        post = Blog.objects.get(slug=slug)
        form = BlogForm(instance=post)

    else:
        post = Blog.objects.get(slug=slug)
        form = BlogForm(instance=post)

    return render_to_response('edit_post.html', {'form': form, },
                              context_instance=RequestContext(request))


@login_required()
def delete_comment(request, slug):
    Comment.objects.filter(slug=slug).delete()

    post = get_object_or_404(Blog, slug=slug)
    return render_to_response('view_post.html', {
        'post': post},
        context_instance=RequestContext(request)) + '#comments'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/accounts/register/complete')

    else:
        form = UserCreationForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response(
        'registration/registration_form.html',
        token,
        context_instance=RequestContext(request)
    )


def registration_complete(request):
    return render_to_response(
        'registration/registration_complete.html',
        context_instance=RequestContext(request)
    )


def notauthorized(request):
    return render_to_response(
        'registration/not_authorized.html',
        context_instance=RequestContext(request)
    )


def loggedin(request):
    return render_to_response(
        'registration/loggedin.html',
        context_instance=RequestContext(request)
    )


def loggedout(request):
    return render_to_response(
        'registration/loggedout.html',
        context_instance=RequestContext(request)
    )

def category_count():
    categories = Category.objects.extra(select={'total': 'select count(bb.category_id) ' +
                                                         'from blog_blog bb ' +
                                                         'where bb.category_id = blog_category.id ' +
                                                         'and bb.published = True '
                                                })
    return categories


def search(request):

    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search_term = search_form.cleaned_data['search_term']

            categories = Category.objects.filter(title__icontains=search_term)
            post_title = Blog.objects.filter(title__icontains=search_term)
            post_body = Blog.objects.filter(body__icontains=search_term)
            comments = Comment.objects.filter(comment__icontains=search_term)

            return render_to_response('search_results.html', {
                'categories': categories,
                'post_title': post_title,
                'post_body': post_body,
                'comments': comments,
            },
                context_instance=RequestContext(request)
            )

    # this is the same code as in the index view. Can just call index view instead?
    categories = category_count()
    posts = Blog.objects.filter(published='True')
    top3posts = Blog.objects.filter(published='True')[:3]
    next3posts = Blog.objects.filter(published='True')[3:6]

    return render_to_response('index.html', {
        'categories': categories,
        'posts': posts,
        'top3posts': top3posts,
        'next3posts': next3posts,
        },
        context_instance=RequestContext(request)
    )

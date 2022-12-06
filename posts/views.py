from django.shortcuts import render, redirect
from posts.models import Post, Comment, Hashtag
from posts.forms import PostCreateForm, CommentCreateForm
from users.utils import get_user_from_request
from django.views.generic import ListView, CreateView, DetailView

# Create your views here.

PAGINATION_LIMIT = 3


class PostsView(ListView):
    model = Post
    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        return {
            'posts': kwargs['posts'],
            'user': get_user_from_request(self.request),
            'max_page': range(1, kwargs['max_page'] + 1),
            'hashtag_id': kwargs['hashtag_id']
        }

    def get(self, request, *args, **kwargs):
        hashtag_id = request.GET.get('hashtag_id')
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if hashtag_id:
            posts = Post.objects.filter(hashtags__in=[hashtag_id])
        else:
            posts = Post.objects.all()

        if search_text:
            posts = posts.filter(title__icontains=search_text)

        posts = [{
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'author': post.author,
            'hashtags': post.hashtags.all(),
            'image': post.image,
        } for post in posts]

        max_page = round(posts.__len__() / PAGINATION_LIMIT)
        posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, self.template_name, context=self.get_context_data(
            posts=posts,
            max_page=max_page,
            hashtag_id=hashtag_id
        ))


# def detail_post_view(request, id):
#     if request.method == 'GET':
#         post = Post.objects.get(id=id)
#         comment = Comment.objects.filter(post__id=id)
#
#         data = {
#             'post': post,
#             'hashtags': post.hashtags.all(),
#             'comments': comment,
#             'form': CommentCreateForm,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'posts/detail.html', context=data)
#
#     if request.method == 'POST':
#         form = CommentCreateForm(data=request.POST)
#
#         if form.is_valid():
#             Comment.objects.create(
#                 author_id=request.user.id,
#                 text=form.cleaned_data.get('text'),
#                 post_id=id
#             )
#             return redirect(f'/posts/{id}/')
#         else:
#             post = Post.objects.get(id=id)
#             comments = Comment.objects.filter(post_id=id)
#
#             data = {
#                 'post': post,
#                 'hashtags': post.hashtags,
#                 'comments': comments,
#                 'form': form,
#                 'user': get_user_from_request(request)
#             }
#             return render(request, 'posts/detail.html', context=data)


class DetailPostView(DetailView, CreateView):
    model = Post
    form_class = CommentCreateForm
    template_name = 'posts/detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'form': kwargs['form'] if kwargs.get('form') else self.form_class,
            'post': self.get_object(),
            'comments': kwargs['comments'],
            'hashtags': kwargs['hashtags']
        }

    def get(self, request, *args, **kwargs):
        post_id = self.model.objects.get(id=kwargs['id'])
        comments = Comment.objects.filter(post_id=post_id)
        hashtags = post_id.hashtags.all()

        return render(request, self.template_name, context=self.get_context_data(
            comments=comments,
            hashtags=hashtags
        ))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author_id=request.user.id,
                post_id=kwargs['id'],
                text=form.cleaned_data.get('text')
            )
            return redirect(f"/posts/{kwargs['id']}/")

        else:
            post_id = self.model.objects.get(id=kwargs['id'])
            comments = Comment.objects.filter(post_id=post_id)
            hashtags = post_id.hashtags.all()

            return render(request, self.template_name, context=self.get_context_data(
                comments=comments,
                hashtags=hashtags
            ))


class HashtagsView(ListView):
    model = Hashtag
    template_name = 'hashtags/hashtags.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'hashtags': self.get_queryset(),
            'user': get_user_from_request(self.request),
        }


class PostCreateView(ListView, CreateView):
    model = Post
    template_name = 'posts/create.html'
    form_class = PostCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                author_id=request.user.id,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )
            return redirect('/posts')
        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))

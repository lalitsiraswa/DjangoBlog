from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#         'title': "Home"
#     }
#     return render(request, template_name="blog/home.html", context=context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # By-default name of the variable is : 'object_list'
    # ordering = ['date_posted']
    ordering = ['-date_posted']  # changing the order of Querying the database.(Means By doing this the latest post will be at the top!)
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # By-default name of the variable is : 'object_list'
    # ordering = ['date_posted']
    # ordering = ['-date_posted']  # changing the order of Querying the database.(Means By doing this the latest post will be at the top!)
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # success_url = 'blog-home' *This will Not Work Here
    # success_url = '/' *Work Properly

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # success_url = 'blog-home' *This will Not Work Here

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, template_name="blog/about.html", context={'title': "About"})

# print(posts[0]["title"])

# posts = [
#     {
#         'author': "Lalit Siraswa",
#         'title': "Blog Post 1",
#         'content': "First Post Content",
#         'data_posted': "August 27, 2020"
#     },
#     {
#         'author': "Lucky Sira swa",
#         'title': "Blog Post 2",
#         'content': "Second Post Content",
#         'data_posted': "August 28, 2020"
#     }
# ]

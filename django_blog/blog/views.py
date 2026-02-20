from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        # Simple update: only email here
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, "Profile updated!")
    return render(request, 'blog/profile.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# List all posts (public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # your template path
    context_object_name = 'posts'
    ordering = ['-published_date']  # newest first

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

from django.urls import reverse_lazy

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# Detail of a single post (public)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create a post (authenticated)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        # Set logged-in user as author
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post (author only)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can edit

# Delete a post (author only)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # redirect after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

from django.shortcuts import redirect, render
from django.views import View

from .forms import TestForm
from .models import Post


class PostUpdate(View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        bound_form = TestForm(instance=post)
        return render(request, 'blog/post_update.html', {'form': bound_form, 'post': post})

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        bound_form = TestForm(request.POST, instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_update.html', {'form': bound_form, 'post': post})


class PostView(View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'blog/post_view.html', {'post': post})

from django.http.response import BadHeaderError, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,

    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.base import RedirectView
from .models import Comment, Post , Comment
from .forms import ContactForm, NewCommentForm
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'blog/post_detail.html', {'post':post, 'form':form})


# class PostDetailView(DetailView):
#     model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content','image']

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
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html' , {'title': 'About'})



   
def contactview(request):
    name=''
    email=''
    comment=''


    form= ContactForm(request.POST or None)
    if form.is_valid():
        subject = "Website Inquiry" 
        body={
            'name':form.cleaned_data["name"],
            'email': form.cleaned_data["email"],
            'comment':form.cleaned_data["comment"],

             }
        comment = "\n".join(body.values())

        try:
            send_mail(subject, comment, 'settings.EMAIL_HOST_USER', ['deepanshumaitrey123@gmail.com']) 
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect ('blog-home')
    
            
        form = ContactForm()
    return render(request, "blog/contact.html", {'form':form})    
    #     if request.user.is_authenticated():
    #         subject= str(request.user) + "'s Comment"
    #     else:
    #         subject= "A Visitor's Comment"


    #     comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
    #     send_mail(subject, comment, 'jha221528@gmail.com', [email])


    #     context= {'form': form}

    #     return render(request, 'blog/contact.html', context)

    # else:
    #     context= {'form': form}
    #     return render(request, 'blog/contact.html', context)


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    fields = '__all__'
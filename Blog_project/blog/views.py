from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailSendForm,CommentForm, CommentModelForm
from taggit.models import Tag

# Create your views here.
def PostList(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,4)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

class PostListView(ListView):
    model=Post
    paginate_by=3

from django.db.models import Count
def Detail_Post_view(request,year,month,day,slug):
    post=get_object_or_404(Post,slug=slug,status='publish',publish__year=year,publish__month=month,publish__day=day)
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    comments=post.comments.filter(status=True)
    csubmit=False
    if request.method=='POST':
        cform=CommentModelForm(request.POST)
        if cform.is_valid():
           new_comment=cform.save(commit=False)
           new_comment.post=post
           new_comment.save()
           csubmit=True
    else:
        cform=CommentForm()
    return render(request,'blog/detailpostview.html',{'post':post,'cform':cform,'comments':comments,'csubmit':csubmit,'similar_posts':similar_posts})

def search_view(request):
    posts=None
    value=request.GET.get('searched')
    print(value)
    if value!=None:
        posts=Post.objects.filter(title__icontains=value,body__icontains=value)
        
        

    return render(request,'blog/searchresults.html',{'posts':posts,'value':value})


from django.core.mail import send_mail
def send_mail_view(request,pk):
    post=get_object_or_404(Post,pk=pk,status='publish')
    if post.status!='publish':
        print('This article is not Published yet..(Draft)')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) reccomends you to read {}'.format(cd['name'],cd['from_email'],post.title)
            message="Read this Article at:\n\t{}\n{}'s Comments:\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'python77zak@gmail.com',[cd['to_email']])
            sent=True
    else:
        form=EmailSendForm()

    return render(request,'blog/share_post.html',{'form':form,'post':post,'sent':sent})

def about_view(request):
    return render(request,'blog/about.html')

def contact_view(request):
    return render(request,'blog/contactus.html')

    



from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
import json
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import *
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .forms import GroupForm, LibraryDocumentForm, VideoForm, RegistrationForm


def index(request):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/login.html", {
            "error_message": error_message,
        })

    post = Post.objects.all().order_by("id").reverse().select_related("user")
    paginator = Paginator(post, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_post = paginator.get_page(page_number)
    user = request.user
    groups = Group.objects.all()
    profile_pics = user.profile_pics
    # Get comments for the posts displayed on the page
    comments = Comment.objects.filter(post__in=page_post)

    return render(request, "network/index.html", {

        "post": post,
        "page_post": page_post,
        "groups":groups,
        "profile_pics": profile_pics,
        "comments": comments,
        "user": user,
    })
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

            # Automatically add the creator to the members field
            group.members.add(request.user)

            return redirect('group_detail', group_id=group.pk)
    else:
        form = GroupForm()
    
    return render(request, 'network/create_group.html', {'form': form})


def join_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user = request.user
    group.members.add(request.user)
    
    # Add a welcome message to the user's session
    welcome_message = "Welcome to the group!"
    messages.success(request, welcome_message)
    
    # Redirect to the group detail page
    return redirect('group_detail', group_id=group.pk)

@login_required
def group_newPost(request, group_id):
    if request.method == "POST":
        group_id = request.POST.get("group_id")  # Assuming the group_id is passed as a form field in the request
        group = get_object_or_404(Group, pk=group_id)
        post = request.POST["post_content"]
        post_image = request.FILES.get("post_image")
        user = User.objects.get(pk=request.user.id)

        # Assign the group to the new GroupPost instance
        postContent = GroupPost(group=group, postContent=post, user=user, post_image=post_image)
        postContent.save()

        return render(request, "network/group_detail.html", {
            "postContent": postContent,
            "test": "test"
        })

    return render(request, "network/group_newPost.html")


    
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group_posts = GroupPost.objects.filter(group=group).order_by("-timestamp").select_related("user")
    paginator = Paginator(group_posts, 10)
    page_number = request.GET.get('page')
    page_group_posts = paginator.get_page(page_number)

    # Filter GroupComment based on related Post objects (not GroupPost)
    post_ids = group_posts.values_list('id', flat=True)
    comments = GroupComment.objects.filter(post__in=post_ids)
    user = request.user
    profile_pics = user.profile_pics
    is_group_member = group.members.filter(id=user.id).exists()

    return render(request, "network/group_detail.html", {
        "group": group,
        "group_posts": group_posts,
        "page_group_posts": page_group_posts,
        "profile_pics": profile_pics,
        "comments": comments,
        "group_id": group_id,
        "is_group_member": is_group_member,
    })



@login_required
def group_newPost(request, group_id):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
    
    if request.method == "POST":
        group = Group.objects.get(pk=group_id)  # Get the Group object based on group_id
        post = request.POST["post_content"]
        post_image = request.FILES.get("post_image")
        user = User.objects.get(pk=request.user.id)
        postContent = GroupPost(group=group, user=user, postContent=post, post_image=post_image)
        postContent.save()
        return redirect('group_detail', group_id=group_id)  # Redirect to the group detail page
        
    return render(request, "network/group_newPost.html", {'group_id': group_id})


@login_required
def group_addComment(request, post_id):
    if request.method == 'POST':
        message = request.POST.get('newComment')
        if not message.strip():
            messages.error(request, "Comment cannot be empty.")
        else:
            post = get_object_or_404(GroupPost, id=post_id)
            author = request.user
            comment = GroupComment.objects.create(author=author, post=post, message=message)
            group_id = post.group.id  # Store the group ID
            return redirect('group_detail', group_id=group_id)  # Redirect to the group detail page

    # If the request method is not POST or the message is empty, redirect to the same page
    return redirect('group_detail', group_id=post_id)



@login_required
def group_add_or_remove_reaction(request, post_id, reaction_type):
    post = get_object_or_404(GroupPost, id=post_id)
    user = request.user

    if request.method == 'POST':
        if reaction_type == 'love':
            ReactionModel = GroupLove
        elif reaction_type == 'haha':
            ReactionModel = GroupHaha
        elif reaction_type == 'like':
            ReactionModel = GroupLike
        elif reaction_type == 'shock':
            ReactionModel = GroupShock
        elif reaction_type == 'sad':
            ReactionModel = GroupSad
        else:
            raise Http404("Invalid reaction type.")

        try:
            reaction = ReactionModel.objects.get(post=post, user=user)
            reaction.delete()
            messages.success(request, f'You removed {reaction_type} reaction on this post.')
        except ReactionModel.DoesNotExist:
            reaction = ReactionModel.objects.create(post=post, user=user)
            messages.success(request, f'You added {reaction_type} reaction on this post.')

    return HttpResponseRedirect(reverse('group_detail', kwargs={'group_id': post.group.id}))

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = LibraryDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploader = request.user
            document.save()
            return redirect('general_library')
    else:
        form = LibraryDocumentForm()

    return render(request, 'network/general_library.html', {'doc_form': form})

@login_required
def upload_video(request):

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
            return redirect('general_library')
    else:
        form = VideoForm()

    return render(request, 'network/general_library.html', {'vid_form': form})



def general_library(request):
    documents = LibraryDocument.objects.all()
    videos = Video.objects.all()
    categories = LibraryCategory.objects.all()
    return render(request, 'network/general_library.html', {
        'documents': documents,
        'videos': videos,
        'categories': categories,
    })

def category_detail(request, category_name):
    documents = LibraryDocument.objects.filter(category__categoryName=category_name)
    videos = Video.objects.filter(category__categoryName=category_name)
    return render(request, 'network/category_detail.html', {
        'documents': documents,
        'videos': videos,
        'category_name': category_name,
    })

def add_to_favorites(request, item_id, item_type):
    user = request.user

    if item_type == 'document':
        item = get_object_or_404(LibraryDocument, pk=item_id)
        FavoriteDocument.objects.get_or_create(user=user, document=item)
    elif item_type == 'video':
        item = get_object_or_404(Video, pk=item_id)
        FavoriteVideo.objects.get_or_create(user=user, video=item)

    return redirect('general_library')

def my_library(request):
    user = request.user
    favorite_documents = FavoriteDocument.objects.filter(user=user)
    favorite_videos = FavoriteVideo.objects.filter(user=user)
    return render(request, 'network/my_library.html', {
        'favorite_documents': favorite_documents,
        'favorite_videos': favorite_videos,
    })


def view_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.views += 1
    video.save()
    return redirect(video.file.url)



@login_required
def forum(request):
    topics = ForumTopic.objects.all().order_by('-created_at')
    return render(request, 'network/forum.html', {'topics': topics})

@login_required
def create_topic(request):
    if request.method == 'POST':
        title = request.POST['title']
        topic = ForumTopic.objects.create(title=title, creator=request.user)
        post_content = request.POST['post_forum_content']
        ForumPost.objects.create(content=post_content, topic=topic, creator=request.user)
        return redirect('forum')
    return render(request, 'network/create_topic.html')

@login_required
def view_topic(request, topic_id):
    topic = ForumTopic.objects.get(pk=topic_id)
    posts = topic.posts.all().order_by('created_at')
    return render(request, 'network/view_topic.html', {'topic': topic, 'posts': posts})

@login_required
def add_forum_post(request, topic_id):
    if request.method == 'POST':
        post_content = request.POST['forum_post_content']
        topic = ForumTopic.objects.get(pk=topic_id)
        ForumPost.objects.create(content=post_content, topic=topic, creator=request.user)
        return redirect('view_topic', topic_id=topic_id)

def new_announcement(request):
    if request.method == "POST":
        title = request.POST["announcement_title"]
        content = request.POST["announcement_content"]
        announcement_image = request.FILES.get("announcement_image")
        poster = request.user
        Announcement.objects.create(poster=poster, title=title, content=content, announcement_image=announcement_image)
        return redirect("announcements")
    
def announcements(request):
    announcement = Announcement.objects.all().order_by('-created_at')
    return render(request, 'network/announcements.html', {'announcements': announcement})
    

@login_required
def like_count(request):
    post = Post.objects.all().order_by("id").reverse().select_related("user")
    return render(request, "network/likecount.html", {
        "posts": post
    })


@login_required
def profile(request, user_id):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
    user = User.objects.get(pk=user_id)
    post = Post.objects.filter(user=user).order_by("id").reverse()
    paginator = Paginator(post, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_post = paginator.get_page(page_number)
    user_like = request.user

    following = Follow.objects.filter(following=user)
    follower = Follow.objects.filter(follower=user)

    try:
        checkFollowers = follower.filter(following=User.objects.get(pk=request.user.id))
        if len(checkFollowers) != 0:
            newFollowing = True
        else:
            newFollowing = False
    except:
        newFollowing = False

    return render(request, "network/user_profile.html", {
        "userProfile": user,
        "post": post,
        "user_like": user_like,
        "page_post": page_post,
        "following": following,
        "follower": follower,
        "username": user.username,
        "isFollowing": newFollowing
    })


@login_required
def edit_profile(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        user.first_name = request.POST["1"]
        user.last_name = request.POST["2"]
        user.about = request.POST["3"]
        user.email = request.POST["4"]
        user.phone_number = request.POST["5"]
        user.save()

        # Redirect to the user profile page
        return render(request, "network/user_profile.html")  # Replace 'user_profile' with the appropriate URL name


@login_required
def post_content(request, post_id):
    post = Post.objects.get(pk=post_id)
    allComments = Comment.objects.filter(post=post)
    user = request.user
    

    return render(request, "network/post_content.html", {
        "posts": post,
        "allComments": allComments,
        
    })

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'network/reset_password_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'network/reset_password.html'


@login_required
def addComment(request, post_id):
    if request.method == 'POST':
        message = request.POST.get('newComment')
        if not message.strip():
            messages.error(request, "Comment cannot be empty.")
            return redirect('index')
        post = Post.objects.get(id=post_id)
        author = request.user
        comment = Comment.objects.create(author=author, post=post, message=message)
        return HttpResponseRedirect(reverse("post_content",args=(post_id, )))





@login_required
def profile_pic(request, user_id):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page"
        return render(request, "network/register.html")


@login_required
def post_image(request, post_id):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page"
        return render(request, "network/register.html")


@login_required
def newPost(request):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
    if request.method == "POST":
        post = request.POST["post_content"]
        post_image = request.FILES.get("post_image")
        user = User.objects.get(pk=request.user.id)
        postContent = Post(postContent=post, user=user, post_image=post_image)
        postContent.save()
        return HttpResponseRedirect(reverse(index))


@login_required
def remove_love(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        maashaa = Love.objects.get(post=post, user=request.user)
        maashaa.delete()
    except Love.DoesNotExist:
        messages.error(request, 'You have not liked this post.')
    return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))


@login_required
def add_love(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        user = request.user
        try:
            maa = Love.objects.get(post=post, user=user)
            maa.delete()
        except Love.DoesNotExist:
            haha = Love.objects.create(post=post, user=user)
        return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))
    else:
        raise Http404("Method not allowed")


@login_required
def remove_haha(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        haha = Haha.objects.get(post=post, user=request.user)
        haha.delete()
    except Haha.DoesNotExist:
        messages.error(request, 'You have not liked this post.')
    return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))


@login_required
def add_haha(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        user = request.user
        try:
            haha = Haha.objects.get(post=post, user=user)
            haha.delete()
        except Haha.DoesNotExist:
            haha = Haha.objects.create(post=post, user=user)
        return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))
    else:
        raise Http404("Method not allowed")


@login_required
def remove_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        messages.success(request, 'You unliked this post.')
    except Like.DoesNotExist:
        messages.error(request, 'You have not liked this post.')

    return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))


@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            messages.success(request, 'You unliked this post.')
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, user=user)
            messages.success(request, 'You liked this post.')

        return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))
    else:
        raise Http404("Method not allowed")



@login_required
def add_shock(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        user = request.user
        try:
            like = Shock.objects.get(post=post, user=user)
            like.delete()
            messages.success(request, 'You unliked this post.')
        except Shock.DoesNotExist:
            like = Shock.objects.create(post=post, user=user)
            messages.success(request, 'You liked this post.')

        return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))
    else:
        raise Http404("Method not allowed")



@login_required
def remove_shock(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Shock.objects.get(post=post, user=request.user)
        like.delete()
        messages.success(request, 'You unliked this post.')
    except Shock.DoesNotExist:
        messages.error(request, 'You have not liked this post.')

    return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))

@login_required
def add_sad(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        user = request.user
        try:
            like = Sad.objects.get(post=post, user=user)
            like.delete()
            messages.success(request, 'You unliked this post.')
        except Sad.DoesNotExist:
            like = Sad.objects.create(post=post, user=user)
            messages.success(request, 'You liked this post.')

        return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))
    else:
        raise Http404("Method not allowed")



@login_required
def remove_sad(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Sad.objects.get(post=post, user=request.user)
        like.delete()
        messages.success(request, 'You unliked this post.')
    except Sad.DoesNotExist:
        messages.error(request, 'You have not liked this post.')

    return HttpResponseRedirect(reverse(post_content, kwargs={'post_id': post_id}))



@login_required
def follow(request):
   if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
   user_follow = request.POST["followUser"]
   current_user = User.objects.get(pk=request.user.id)
   userFollowData =User.objects.get(username=user_follow)
   saveFollowers = Follow(following=current_user, follower=userFollowData)
   saveFollowers.save()
   user_id = userFollowData.id
   return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))




@login_required
def unfollow(request):
   if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
   user_follow = request.POST["followUser"]
   current_user = User.objects.get(pk=request.user.id)
   userFollowData =User.objects.get(username=user_follow)
   saveFollowers = Follow.objects.get(following=current_user, follower=userFollowData)
   saveFollowers.delete()
   user_id = userFollowData.id
   return HttpResponseRedirect(reverse("index"))


@login_required
def following(request):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")

    current_user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(following=current_user)

    # Get the posts by the users the current user is following
    followingPosts = Post.objects.filter(user__in=[f.follower for f in following]).order_by('-timestamp')

    paginator = Paginator(followingPosts, 10)  # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_post = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_post": page_post
    })


@login_required
def edit(request, post_id):
    if not request.user.is_authenticated:
        error_message = "You need to log in to access this page."
        return render(request, "network/register.html")
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.postContent = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return render(request, "network/login.html")

def terms(request):
    return render(request, "terms.html")
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)

            # Save the profile picture if provided
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                user.profile_pic = profile_pic

            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, "network/register.html", {'form': form})



class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('registration/password_reset_done')
    email_template_name = 'registration/password_reset_email.html'

    def form_valid(self, form):
        context = {'email': form.cleaned_data['email']}
        return render(self.request, self.template_name, context)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('registration/password_reset_complete')


class CustomPasswordResetCompleteView(TemplateView):
    template_name = 'registration/password_reset_complete.html'
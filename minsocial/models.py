from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pics = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="post_user")
    postContent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user} {self.postContent} {self.timestamp}"

class PostImage(models.Model):
    postContent = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images")
    post_image = models.ImageField(upload_to='post_image/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.postContent}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postComment")
    message = models.CharField(max_length=10000)

    def __str__(self):
        return f"{str(self.author)} commented on {self.post}"
    
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="following_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="followed_user")

    def __str__(self):
        return f"{self.following} is following {self.follower}"

# Regular post reactions
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.user} likes {self.post}"

class Sad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userSad")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postSad")

    def __str__(self):
        return f"{self.user} reacts Sad on {self.post}"

class Love(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLove")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postLove")

    def __str__(self):
        return f"{self.user} reacts Love on {self.post}"

class Haha(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userHaha")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postHaha")

    def __str__(self):
        return f"{self.user} reacts Haha on {self.post}"

class Shock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userShock")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postShock")

    def __str__(self):
        return f"{self.user} reacts Shock on {self.post}"

# Define the Group model and GroupPost model
class Group(models.Model):
    name = models.CharField(max_length=100)  # Default value for 'name'
    description = models.TextField(blank=True, null=True,)  # Default value for 'description'
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='group_members')

    def __str__(self):
        return f"{self.name}"

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="group_post_user")
    postContent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.postContent}"
    
class GroupPostImage(models.Model):
    postContent = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_post_images")
    post_image = models.ImageField(upload_to='post_image/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.postContent}"
    
class GroupComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="group_userComment")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, blank=True, null=True, related_name="group_postComment")
    message = models.CharField(max_length=10000)

    def __str__(self):
        return f"{str(self.author)} commented on {self.post}"
    


class GroupLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_user_like")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_post_like")

    def __str__(self):
        return f"{self.user} likes {self.post}"

class GroupSad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_userSad")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_postSad")

    def __str__(self):
        return f"{self.user} reacts Sad on {self.post}"

class GroupLove(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_userLove")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_postLove")

    def __str__(self):
        return f"{self.user} reacts Love on {self.post}"

class GroupHaha(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_userHaha")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_postHaha")

    def __str__(self):
        return f"{self.user} reacts Haha on {self.post}"

class GroupShock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_userShock")
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="group_postShock")

    def __str__(self):
        return f"{self.user} reacts Shock on {self.post}"
    


class LibraryCategory(models.Model):
    CATEGORY_CHOICES = [
        ('Science', 'Science'),
        ('IT', 'IT'),
        ('Math', 'Math'),
        ('Skills and Self-growth', 'Skills and Self-growth'),
        ('Agriculture', 'Agriculture'),
        ('Finance', 'Finance'),
        ('Economics', 'Economics'),
        ('Philosophy', 'Philosophy'),
    ]

    categoryName = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.categoryName

class LibraryDocument(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(LibraryCategory, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='library/documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(LibraryCategory, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='library/videos/')
    views = models.PositiveIntegerField(default=0)
    viewers_ip = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    
class FavoriteDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey('LibraryDocument', on_delete=models.CASCADE)

class FavoriteVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)



class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumTopicImage(models.Model):
    content = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name="forum_topic_post_images")
    post_image = models.ImageField(upload_to='post_image/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.content}"

class ForumPost(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.creator.username} in {self.topic.title}"

class Announcement(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_poster")
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} announced by {self.poster}"
    
class AnnouncementPostImage(models.Model):
    content = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="announcement_post_images")
    post_image = models.ImageField(upload_to='post_image/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.content}"
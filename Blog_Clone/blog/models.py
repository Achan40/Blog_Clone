from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    # Only expect one user, that's why we use this 
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    # when you hit publish, list current time
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Eventually we will have a list of comments, then we will filter by approval
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # function must be called get_absolute_url
    # sends to a detail view
    # After a post is created, go to the post's detail page of the post with the primary key that you just created
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    # After comment is created, go back to the list view, which is also the homepage
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
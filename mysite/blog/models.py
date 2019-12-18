from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    last_publication_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        time_now = timezone.now()
        self.last_publication_date = time_now
        new_pub = Publication(post=self, publication_date=time_now)
        new_pub.save()
        self.save()


    def approve_comments(self):
        # comment will be another class
        return self.comments.filter(approved_comment=True)

    # needed to figure out where the site should go once
    # create an instance of the class
    def get_absolute_url(self):
        return reverse("blog:post_details", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text

class Publication(models.Model):
    post = models.ForeignKey('blog.Post', related_name = 'publications', on_delete=models.CASCADE)
    publication_date = models.DateTimeField(blank=True)

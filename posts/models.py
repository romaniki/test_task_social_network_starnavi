from django.db import models
from accounts.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"Post {self.id} posted by {self.author} on {self.created.strftime('%d %b %Y %H:%M:%S')}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"Like {self.id} by {self.user} on object {self.post.id}"

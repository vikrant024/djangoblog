from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    # header_image = models.ImageField(null=True , blank= True, upload_to="media/images/" )
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="post",null=True , blank= True)
    
    def __str__(self):
        return self. title 
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self, ** kwargs):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 700 or img.width > 700:
            output_size =(400 , 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments" , on_delete=models.CASCADE)
    name = models.CharField(max_length =255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    
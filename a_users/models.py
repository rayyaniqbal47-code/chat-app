from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='avatars/', default='images/ape1.jpg', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.username
    
    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.username 
        return name
    
    @property
    def avatar(self):
        if self.image and hasattr(self.image, "url"):
            try:
                return self.image.url
            except:
                pass
        return static("images/ape1.jpg")

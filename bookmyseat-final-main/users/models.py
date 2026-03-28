from django.db import models
class Movie(models.Model):
   trailer_key = models.URLField(
      blank=True,
      null=True,
      help_text="Youtube link for movies trailer"
   )
   def __str__(self):
      return f"{self.title}"
   
   def get_trailer_id(self):
       if self.trailer_key and "v=" in self.trailer_key:
           return self.trailer_key.split("v=")[1].split("&")[0]
       return ""




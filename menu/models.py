from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    menu_name = models.CharField(max_length=120, help_text="Название меню")
    name = models.CharField(max_length=120)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, blank=True, help_text="named URL")
    named_url = models.CharField(max_length=100, blank=True, help_text="Имя именованного URL")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return self.url or '#'
        return self.url or '#'
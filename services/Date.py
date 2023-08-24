from django.db import models

class Date(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def get_time(self):
        return f'{str(self.created_date.hour)}:{str(self.created_date.minute)}'

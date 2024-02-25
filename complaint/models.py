from django.db import models
from django.contrib.auth import get_user_model
from services.Date import Date

Users = get_user_model()


class Complaint(Date):
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name='from_user')
    to_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name='to_user')
    compliant_reason = models.CharField(max_length=500)
    content = models.TextField()

    def __str__(self):
        return f'{self.to_user.username}'

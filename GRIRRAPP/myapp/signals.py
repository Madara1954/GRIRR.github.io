from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_delete
from django.dispatch import receiver
from myapp.models import CustomUser

@receiver(post_delete, sender=CustomUser)
def delete_user_logs(sender, instance, **kwargs):
    LogEntry.objects.filter(user_id=instance.id).delete()

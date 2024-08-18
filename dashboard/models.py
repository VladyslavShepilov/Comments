from django.db import models
from django.contrib.auth import get_user_model


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), related_name="comments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.user.username} at ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    class Meta:
        ordering = ["-created_at"]

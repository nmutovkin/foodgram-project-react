from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='Subcriber',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='Author',
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow')
        ]

    def __str__(self):
        return str(self.user) + " follows " + str(self.author)

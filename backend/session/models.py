from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_code

CustomUser = get_user_model()

class Session(models.Model):
    """
    Sessions in this app are represented by this model

    The creator field is required.
    """

    STAGE_CHOICES = {
        "0": "Suggesting",
        "1": "Banning",
        "2": "Voting",
        "3": "Results",
    }

    join_code = models.CharField(max_length=6, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="session"
    )
    stage = models.CharField(max_length=1, choices=STAGE_CHOICES)

    REQUIRED_FIELDS = ["creator"]

    class Meta:
        verbose_name = "session"
        verbose_name_plural = "sessions"

    def generate_unique_code(self):
        """Uses the generate_code function to generate a unique code"""
        code = generate_code()
        while Session.objects.filter(code=code).exists():
            code = generate_code()
        return code

    def save(self, *args, **kwargs):
        """Modifies the save function to automatically generate a unique code"""
        if not self.join_code:
            self.join_code = self.generate_unique_code()
        super().save(*args, **kwargs)


class RestaurantSuggestion(models.Model):
    """
    Suggestions in this app are represented by this model.

    The session the suggestion belongs to and the name of the restaurant are
    required.
    """

    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="session"
    )
    name = models.CharField(max_length=100)
    is_banned = models.BooleanField(default=False)
    picks = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    REQUIRED_FIELDS = ["session", "name"]

    class Meta:
        verbose_name = "restaurant"
        verbose_name_plural = "restaurants"

    def __str__(self):
        """Returns the restaurant's name"""
        return self.display_name
    
class Member(models.Model):
    """
    Members of a session are represented in this model

    The user the member represents and the session the member is in are required.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ["user", "session"]

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return str(self.text)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

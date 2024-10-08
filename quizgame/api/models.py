from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    """
    A Quiz represents a collection of questions created by a user.
    It has a title, creator, creation timestamp, and last update timestamp.

    Attributes:
        title (CharField): The title of the quiz.
        creator (ForeignKey): The user who created the quiz.
        created_at (DateTimeField): Timestamp of when the quiz was created.
        updated_at (DateTimeField): Timestamp of when the quiz was last updated.
    """

    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    """
    A Question represents a single question within a Quiz.
    It contains the question text, type, number of answers, difficulty,
    and a foreign key to the Quiz it belongs to.

    Attributes:
        quiz (ForeignKey): The Quiz this question belongs to.
        text (TextField): The text of the question.
        type (CharField): The type of question (e.g., multiple choice, true/false).
        number_of_answers (IntegerField): The number of possible answers for this question.
        difficulty (CharField): The difficulty level of the question.
    """

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    difficulty = models.CharField(max_length=255)

    def __str__(self):
        return str(self.text)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.text)


class QuizSession(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name="quiz_sessions")
    current_question = models.ForeignKey(
        Question, null=True, blank=True, on_delete=models.SET_NULL
    )
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.title} - {', '.join(player.username for player in self.players.all())}"


class Player(models.Model):
    """
    A Player represents a user who is playing a quiz.
    It has a user, score, and current quiz session.

    Attributes:
        user (OneToOneField): The user associated with the player.
        score (IntegerField): The player's score.
        current_session (ForeignKey): The current quiz session the player is in.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    current_session = models.ForeignKey(
        QuizSession, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.user.username

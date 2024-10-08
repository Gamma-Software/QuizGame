# QuizGame
This is a web application to implement a quiz game for fun with others

In this exercise, you’ll create the basic structure of a quiz game where users can:

	1.	Create a quiz session with multiple questions and answers.
	2.	Retrieve and play a quiz by answering questions.
	3.	Submit answers and get feedback on their performance.

Goal

	•	Practice creating serializers, generic views, and viewsets to build a REST API that supports a quiz game.
	•	Implement the core functionality for creating, retrieving, and interacting with quiz sessions.

Step-by-Step Instructions

Step 1: Setup Django Project

First, set up a new Django project and app for the quiz game.

django-admin startproject quizgame
cd quizgame
python manage.py startapp quiz

Add quiz and rest_framework to your INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
    ...
    'rest_framework',
    'quiz',
]

Step 2: Define Models

Create the models for the quiz game. You’ll need models for Quizzes, Questions, Answers, and QuizSessions.

In quiz/models.py:

from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.username} - {self.quiz.title}"

Step 3: Create Serializers

Next, create serializers to convert the models into JSON format and validate the data.

In quiz/serializers.py:

from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizSession

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'creator', 'questions']

class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = ['id', 'quiz', 'player', 'score', 'completed']

	•	AnswerSerializer and QuestionSerializer are used to handle nested relationships in a quiz.
	•	QuizSerializer will return all questions and answers related to the quiz.
	•	QuizSessionSerializer tracks a user’s performance in a particular quiz session.

Step 4: Create Views (Generic Views)

Now, implement the views to handle creating quizzes, answering questions, and retrieving results.

In quiz/views.py:

from rest_framework import generics, permissions
from .models import Quiz, QuizSession
from .serializers import QuizSerializer, QuizSessionSerializer

# List quizzes and create new ones
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# Retrieve a quiz with its questions
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

# Start a quiz session (associate a player with the quiz)
class QuizSessionCreateView(generics.CreateAPIView):
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

# Retrieve a player's quiz session
class QuizSessionDetailView(generics.RetrieveAPIView):
    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizSession.objects.filter(player=self.request.user)

	•	QuizListCreateView allows users to list all quizzes or create a new quiz.
	•	QuizDetailView provides a detailed view of a quiz along with its questions and answers.
	•	QuizSessionCreateView lets a player start a new quiz session, associating them with a specific quiz.
	•	QuizSessionDetailView retrieves the session data for a particular player.

Step 5: Define URLs

In quiz/urls.py, define the endpoints for the views.

from django.urls import path
from .views import QuizListCreateView, QuizDetailView, QuizSessionCreateView, QuizSessionDetailView

urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('sessions/', QuizSessionCreateView.as_view(), name='quiz-session-create'),
    path('sessions/<int:pk>/', QuizSessionDetailView.as_view(), name='quiz-session-detail'),
]

Include this in your main urls.py file:

from django.urls import path, include

urlpatterns = [
    path('api/', include('quiz.urls')),
    path('api-auth/', include('rest_framework.urls')),  # for login/logout
]

Step 6: Test the API

	1.	Create a Quiz:
Send a POST request to /api/quizzes/ with the title of the quiz.
	2.	View Quiz Details:
Send a GET request to /api/quizzes/<quiz_id>/ to view the questions and answers.
	3.	Start a Quiz Session:
Send a POST request to /api/sessions/ to start a new quiz session for a player.
	4.	Retrieve Quiz Session Results:
Send a GET request to /api/sessions/<session_id>/ to retrieve the results for a quiz session.

Bonus Tasks (For Extra Practice)

	1.	Scoring Logic:
Add logic in the QuizSession to calculate and store the player’s score based on their answers.
	2.	Answer Submission Endpoint:
Create a new API endpoint to submit answers to questions and update the player’s score.
	3.	Leaderboard Feature:
Implement a leaderboard system where players can see their scores compared to others.
	4.	Pagination:
Add pagination to the quiz listing endpoint to handle a large number of quizzes.

Summary

This exercise walks you through creating a basic backend for a quiz game using Django REST Framework, focusing on key concepts like generic views and serialization. The project can be extended with features like scoring, leaderboards, and real-time multiplayer gameplay.

By working through this, you’ll strengthen your understanding of DRF’s generic views, nested serialization, permissions, and API design principles.
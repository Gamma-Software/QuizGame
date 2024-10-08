"""
URL configuration for quizgame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import (
    QuestionListCreateView,
    QuizListCreateView,
    QuizDetailView,
    QuizSessionCreateView,
    QuizSessionDetailView,
    UserQuizSessionDetailView,
    PlayerDetailView,
)

urlpatterns = [
    path("quizzes/", QuizListCreateView.as_view(), name="quiz-list-create"),
    path("quizzes/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("sessions/", QuizSessionCreateView.as_view(), name="quiz-session-create"),
    path(
        "sessions/<int:pk>/",
        QuizSessionDetailView.as_view(),
        name="quiz-session-detail",
    ),
    path(
        "user-session/<int:user>/",
        UserQuizSessionDetailView.as_view(),
        name="user-quiz-session-detail",
    ),
    path("me/", PlayerDetailView.as_view(), name="player-detail"),
]

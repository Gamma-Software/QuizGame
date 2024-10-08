from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from .models import Quiz, QuizSession, Question, Player
from .serializers import (
    QuizSerializer,
    QuizSessionSerializer,
    QuestionSerializer,
    PlayerSerializer,
)


# Create your views here.
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizSessionCreateView(generics.CreateAPIView):
    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(players=[self.request.user])


class QuizSessionDetailView(generics.RetrieveAPIView):
    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserQuizSessionDetailView(generics.RetrieveAPIView):
    """Find the quiz session for the user and return it"""

    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get("user")
        return QuizSession.objects.filter(players=user_id).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(
            {"detail": "No active quiz session found for this user."},
            status=status.HTTP_404_NOT_FOUND,
        )


class PlayerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = Player.objects.filter(user=request.user).first()
        if player:
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        return Response(
            {"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND
        )

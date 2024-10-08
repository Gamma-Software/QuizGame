from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Quiz, QuizSession
from .serializers import QuizSerializer, QuizSessionSerializer


# Create your views here.
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

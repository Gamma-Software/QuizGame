from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizSession


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def validate_type(self, value):
        valid_types = ["multiple", "single"]
        if value.lower() not in valid_types:
            raise serializers.ValidationError(
                "Question type must be either 'multiple' or 'single'."
            )
        return value.lower()

    def validate_number_of_answers(self, value):
        if value < 1:
            raise serializers.ValidationError("Number of answers must be at least 1.")
        if value > 4:
            raise serializers.ValidationError("Number of answers must be at most 4.")
        return value

    def validate(self, attrs):
        if attrs["type"] == "multiple" and attrs["number_of_answers"] <= 1:
            raise serializers.ValidationError(
                "For multiple choice questions, number of answers must be more than 1."
            )
        if attrs["type"] == "single" and attrs["number_of_answers"] != 1:
            raise serializers.ValidationError(
                "For single answer questions, number of answers must be 1."
            )
        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = "__all__"

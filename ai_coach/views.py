from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from groq import Groq
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer


class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        user_message = request.data.get('message', '')

        if not user_message:
            return Response(
                {'error': 'Message content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save user message
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message
        )

        # Get AI response using Groq
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            # Get conversation history
            messages = [{'role': msg.role, 'content': msg.content} 
                       for msg in session.messages.all()]

            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )

            ai_response = response.choices[0].message.content

            # Save AI response
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=ai_response
            )

            return Response({
                'user_message': user_message,
                'ai_response': ai_response
            })

        except Exception as e:
            return Response(
                {'error': f'Failed to get AI response: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(session__student=self.request.user)

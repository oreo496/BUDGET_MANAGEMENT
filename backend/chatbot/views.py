from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from .service import get_funderbot_reply


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        # Return only messages for the current user (would need auth)
        return ChatMessage.objects.all()

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message and get a response from FunderBot."""
        user_message = request.data.get('message', '').strip()
        
        if not user_message:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get AI response
            bot_response = get_funderbot_reply(user_message)
            
            # Store in database (optional, requires user auth)
            # chat_msg = ChatMessage.objects.create(
            #     user_id=request.user.id,
            #     message=user_message,
            #     response=bot_response
            # )
            
            return Response(
                {
                    'user_message': user_message,
                    'bot_response': bot_response,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to process message: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

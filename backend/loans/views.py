from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdmin
from .models import Loan
from .serializers import LoanSerializer
import jwt
from django.conf import settings
from accounts.models import User


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        # If Authorization Bearer JWT present, return loans for that user
        request = self.request
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                user_id = payload.get('user_id')
                if user_id:
                    return Loan.objects.filter(user__id=user_id).order_by('-created_at')
            except Exception:
                return Loan.objects.none()
        # Otherwise return none for security
        return Loan.objects.none()

    def create(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1].strip()
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            if not user_id:
                raise Exception('user_id missing')
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            loan = Loan(
                user=user,
                amount=serializer.validated_data['amount'],
                term_months=serializer.validated_data['term_months'],
                interest_rate=serializer.validated_data.get('interest_rate', 0.0),
            )
            loan.save()
            return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

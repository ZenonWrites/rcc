from rest_framework import viewsets, permissions
from .models import DeliveryAssignment
from .serializers import DeliveryAssignmentSerializer

class DeliveryAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAssignmentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.user_type in ['admin', 'owner']:
            return DeliveryAssignment.objects.all()
        return DeliveryAssignment.objects.filter(delivery_agent=user)
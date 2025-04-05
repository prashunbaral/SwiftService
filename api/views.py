from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Category, Service, Booking
from .serializers import (
    UserSerializer, RegisterSerializer, CategorySerializer,
    ServiceSerializer, BookingSerializer
)

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        # In JWT, we don't need to do anything on the server side
        # The token will be invalidated by removing it from the client
        return Response({'message': 'Successfully logged out'})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Service.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset
    
    @action(detail=False)
    def featured(self, request):
        featured_services = Service.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_services, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.customer != request.user and not request.user.is_staff:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'Booking cancelled'}) 
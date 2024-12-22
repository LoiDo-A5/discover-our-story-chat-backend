from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Friendship, User
from ..serializers.friendship import FriendshipSerializer
from rest_framework.generics import get_object_or_404
from django.db import models


class FriendshipViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)) & models.Q(status='accepted')
        )

    def create(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        to_user = get_object_or_404(User, id=to_user_id)

        if not to_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if to_user == request.user:
            return Response({'error': 'You cannot send a friend request to yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_request = Friendship.objects.filter(from_user=request.user, to_user=to_user).first()
        if existing_request:
            return Response({'error': 'Friend request already sent or exists.'}, status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.create(from_user=request.user, to_user=to_user, status='pending')
        return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        action = request.data.get('action')
        friendship = Friendship.objects.filter(id=kwargs.get('pk'), to_user=request.user).first()

        if not friendship:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friendship.status = 'accepted'
            friendship.save()
            return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friendship.status = 'rejected'
            friendship.save()
            return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
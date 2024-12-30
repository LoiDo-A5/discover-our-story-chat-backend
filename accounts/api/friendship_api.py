from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Friendship, User
from ..serializers.friendship import FriendshipSerializer
from rest_framework.generics import get_object_or_404
from django.db import models
from rest_framework.decorators import action
from django.db.models import Q


class FriendshipViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)) & models.Q(status='accepted')
        )

    # def get_serializer_class(self):
    #     if self.action == 'list_artwork_by_artist':
    #         return cancel_request
    #     return super().get_serializer_class()

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

    @action(detail=False, methods=['get'])
    def cancel_request(self, request):
        to_user_id = request.data.get('to_user_id')
        friendship = Friendship.objects.filter(from_user=request.user, to_user_id=to_user_id, status='pending').first()

        if not friendship:
            return Response({"error": "Friendship request not found."}, status=status.HTTP_404_NOT_FOUND)

        friendship.delete()
        return Response({"message": "Friendship request cancelled."}, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'], url_path='remove-friend')
    # def remove_friend(self, request):
    #     user_id = request.data.get('user_id')
    #     friendship = Friendship.objects.filter(
    #         (Q(from_user=request.user, to_user_id=user_id) | Q(to_user=request.user, from_user_id=user_id)),
    #         status='accepted'
    #     ).first()
    #
    #     if not friendship:
    #         return Response({"error": "Friendship not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     friendship.status = 'removed'
    #     friendship.save()
    #     return Response({"message": "Friend removed."}, status=status.HTTP_200_OK)
    #
    # @action(detail=False, methods=['get'], url_path='friends-list')
    # def friends_list(self, request):
    #     friendships = Friendship.objects.filter(
    #         Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted')
    #     )
    #
    #     friends = [
    #         friendship.to_user if friendship.from_user == request.user else friendship.from_user
    #         for friendship in friendships
    #     ]
    #
    #     serializer = UserSerializer(friends, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
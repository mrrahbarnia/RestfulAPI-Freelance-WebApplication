from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    permissions,
    serializers
)
from drf_spectacular.utils import extend_schema

from core.selectors.portfolio import (
    get_my_portfolios,
    list_comments
)
from core.services.portfolio import (
    create_portfolio,
    get_portfolio,
    get_portfolio_for_delete,
    publish_portfolio,
    get_portfolio_comment_for_delete
)
from portfolio.models import (
    Portfolio,
    PortfolioComment
)
from .permission import (
    IsOwnerOrReadOnly,
    IsOwner
)
from core.permission import IsAdmin


class CreatePortfolioApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    class InputPortfolioSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=250, required=True)
        description = serializers.CharField(max_length=1000, required=False)
        cover_image = serializers.ImageField(required=False)


    class OutputPortfolioSerializer(serializers.ModelSerializer):

        class Meta:
            model = Portfolio
            fields = ('title', )
    
    @extend_schema(
            request=InputPortfolioSerializer,
            responses=OutputPortfolioSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputPortfolioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            portfolio = create_portfolio(
                user=request.user,
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                cover_image=serializer.validated_data.get('cover_image')
            )
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        response = self.OutputPortfolioSerializer(portfolio).data
        return Response(response, status=status.HTTP_201_CREATED)


class MyPortfoliosApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    class MyPortfolioOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Portfolio
            fields = ('title', 'description', 'cover_image')
        
    def get(self, request, *args, **kwargs):
        try:
            portfolios = get_my_portfolios(user=request.user)
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        response = self.MyPortfolioOutputSerializer(portfolios, many=True).data
        return Response(response, status=status.HTTP_200_OK)


class PortfolioDetailApiView(APIView):
    permission_classes = [IsOwnerOrReadOnly]


    class PortfolioDetailOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Portfolio
            fields = ('title', 'description', 'cover_image')

    @extend_schema(responses=PortfolioDetailOutputSerializer)
    def get(self, request, slug, *args, **kwargs):
        try:
            portfolio = get_portfolio(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        response = self.PortfolioDetailOutputSerializer(portfolio).data
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, slug, *args, **kwargs):
        """
        Delete method allowed only by the owner of the portfolio.
        """
        try:
            portfolio = get_portfolio_for_delete(slug=slug)
            self.check_object_permissions(request=request, obj=portfolio)
            portfolio.delete()
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentApiView(APIView):
    permission_classes = [IsAdmin]

    class CommentOutputSerializer(serializers.ModelSerializer):
        user = serializers.CharField(source='user.phone_number')
        portfolio = serializers.CharField(source='portfolio.title')

        class Meta:
            model = PortfolioComment
            fields = ('comment', 'user', 'portfolio')

    @extend_schema(responses=CommentOutputSerializer)
    def get(self, request, *args, **kwargs):
        try:
            comments = list_comments()
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        response = self.CommentOutputSerializer(comments, many=True).data
        return Response(response, status=status.HTTP_200_OK)


class PublishPortfolioApiView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, slug, *args, **kwargs):
        try:
            publish_portfolio(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_200_OK)


class DeleteCommentApiView(APIView):
    permission_classes = [IsOwner]

    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = get_portfolio_comment_for_delete(pk=pk)
            self.check_object_permissions(obj=comment, request=request)
            comment.delete()
        except Exception as ex:
            raise serializers.ValidationError(
                {'detail': f'{ex}'}
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

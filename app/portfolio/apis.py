from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    permissions,
    serializers
)
from drf_spectacular.utils import extend_schema

from core.services.portfolio import (
    create_portfolio,
)
from portfolio.models import (
    Portfolio
)


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
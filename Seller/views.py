from rest_framework.response import Response
from rest_framework import status
from .serializer import SellerSerializer
from .models import Seller
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import viewsets
from rest_framework.decorators import action


class SellerAPI(viewsets.GenericViewSet, CreateModelMixin,
                RetrieveModelMixin, DestroyModelMixin):
    serializer_class = SellerSerializer
    model = Seller
    lookup_field = 'buyer_id'
    queryset = Seller.objects.all()

    def get_queryset(self):
        buyer_id = self.request.headers.get('Authorization')
        qs = Seller.objects.get(buyer=buyer_id)
        return qs

    def get_object(self):
        obj = self.get_queryset()
        return obj

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        try:
            self.create(request, *args, **kwargs)
            return Response({"success": True, "msg": "Seller Created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Seller Does Not Exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({"success": True, "msg": "Seller Deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"success": False, "mdg": "Seller does not exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['patch'], detail=True)
    def patch(self, request):
        try:
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, "msg": "Seller Data is Updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

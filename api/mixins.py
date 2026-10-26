
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from api.services import next_order
 
from api.permissions import IsAdmin
from api.serializers import ReorderSerializer
 
 
class MultipartParserMixin:
    """
    Use on every view that accepts images/files; send data as multipart/form-data.
    Form parsers only (no JSON) so drf-yasg shows real file inputs in Swagger.
    """
 
    parser_classes = [MultiPartParser, FormParser, JSONParser,]
 
 
class VisibilityMixin:
    """
    Visitors only see active/published rows; Admin sees everything.
    Set `visibility_field` to "is_published" for news, etc.
    """
 
    visibility_field = "is_active"
 
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return queryset
        return queryset.filter(**{self.visibility_field: True})
    

class ReorderMixin:
    """
    Adds POST <list-url>/reorder/  with JSON body {"ids": [3, 1, 2]} (admin only).
    The model must have an integer `order` field (ActiveOrderModel).
    """
 
    @swagger_auto_schema(request_body=ReorderSerializer)
    @action(
        detail=False,
        methods=["post"],
        url_path="reorder",
        permission_classes=[IsAdmin],
        parser_classes=[JSONParser],
    )
    def reorder(self, request):
        serializer = ReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data["ids"]
 
        model = self.get_queryset().model
        objects = {obj.pk: obj for obj in model.objects.filter(pk__in=ids)}
        missing = [pk for pk in ids if pk not in objects]
        if missing:
            return Response({"ids": f"Unknown ids: {missing}"}, status=400)
 
        with transaction.atomic():
            for position, pk in enumerate(ids):
                objects[pk].order = position
            model.objects.bulk_update(objects.values(), ["order"])
        return Response({"detail": "Order updated."})
    
    
class SingletonMixin:
    """For RetrieveUpdateAPIView on a SingletonModel: always returns the one row.
    The view must set `queryset = Model.objects.all()`."""
 
    def get_object(self):
        obj = self.queryset.model.load()
        self.check_object_permissions(self.request, obj)
        return obj
    

class GalleryMixin:
    """
    Gallery images under a detail URL (plots, flats, csr, news):
 
        GET    <detail>/images/            visitor  - list images
        POST   <detail>/images/            admin    - upload (multipart): one file as
                                                      `image`, or many by repeating `images`
        PATCH  <detail>/images/<id>/       admin    - caption / order / replace file
        DELETE <detail>/images/<id>/       admin
 
    The viewset sets:
        gallery_serializer_class  serializer with fields id, image, caption, order
        gallery_related_name      related_name on the parent model (default "images")
        gallery_parent_field      name of the ForeignKey on the gallery model (e.g. "plot")
    Put this mixin FIRST in the class bases, before ModelViewSet.
    """
 
    gallery_serializer_class = None
    gallery_related_name = "images"
    gallery_parent_field = None
 
    def get_serializer_class(self):
        if getattr(self, "action", None) in ("images", "image_detail"):
            return self.gallery_serializer_class
        return super().get_serializer_class()
 
    def _gallery(self, parent):
        return getattr(parent, self.gallery_related_name)
 
    @action(detail=True, methods=["get", "post"], url_path="images")
    def images(self, request, *args, **kwargs):
        parent = self.get_object()
        gallery = self._gallery(parent)
        serializer_class = self.gallery_serializer_class
        context = self.get_serializer_context()
 
        if request.method == "GET":
            return Response(serializer_class(gallery.all(), many=True, context=context).data)
 
        files = request.FILES.getlist("images")
        if not files and "image" in request.FILES:
            files = [request.FILES["image"]]
        if not files:
            raise ValidationError({"image": "Upload at least one image."})
 
        caption = request.data.get("caption", "")
        position = next_order(gallery)
        created = []
        with transaction.atomic():
            for file in files:
                serializer = serializer_class(
                    data={"image": file, "caption": caption, "order": position}, context=context
                )
                serializer.is_valid(raise_exception=True)
                created.append(serializer.save(**{self.gallery_parent_field: parent}))
                position += 1
        return Response(
            serializer_class(created, many=True, context=context).data,
            status=status.HTTP_201_CREATED,
        )
 
    @action(detail=True, methods=["patch", "delete"], url_path=r"images/(?P<image_id>\d+)")
    def image_detail(self, request, image_id=None, *args, **kwargs):
        parent = self.get_object()
        image = get_object_or_404(self._gallery(parent), pk=image_id)
        if request.method == "DELETE":
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.gallery_serializer_class(
            image, data=request.data, partial=True, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
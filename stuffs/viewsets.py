from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.viewmixins import NestedObjectMixin
from core.viewsets import CreateListViewSet, RetrieveUpdateDestroyViewset

from .models import Component, Group, Specification
from .serializers import (
    ComponentSerializer,
    GroupSerializer,
    PartCodeAssignmentSerializer,
    SpecificationCloneSerializer,
    SpecificationImportSerializer,
    SpecificationSerializer,
)


class SpecificationViewSet(ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

    @action(detail=True, methods=["post"], serializer_class=SpecificationCloneSerializer)
    def clone(self, request, *args, **kwargs):
        specification = self.get_object()
        serializer = self.get_serializer(data=request.data, specification=specification)

        if serializer.is_valid():
            cloned_specification = serializer.clone()
            specification_serializer = SpecificationSerializer(cloned_specification, context={"request": request})

            return Response(
                {"status": "Specification cloned successfully!", "cloned": specification_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], serializer_class=SpecificationImportSerializer)
    def import_data(self, request):
        serializer = SpecificationImportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "Specifications imported successfully!"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseNestedSpecificationViewSet(NestedObjectMixin, CreateListViewSet):
    parent_model = Specification
    parent_object_lookup_field = "specification_pk"

    def get_serializer(self, *args, **kwargs):
        kwargs.update(specification=self.get_parent_object())

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(specification_id=self.look_up_field_value)


class NestedSpecificationGroupViewSet(BaseNestedSpecificationViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(specification_id=self.look_up_field_value)


class NestedSpecificationComponentsViewSet(BaseNestedSpecificationViewSet):
    serializer_class = ComponentSerializer

    def get_queryset(self):
        return Component.objects.filter(specification_id=self.look_up_field_value)


class GroupViewSet(RetrieveUpdateDestroyViewset):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ComponentViewSet(RetrieveUpdateDestroyViewset):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    @action(detail=True, methods=["patch"], serializer_class=PartCodeAssignmentSerializer)
    def assign_part(self, request, *args, **kwargs):
        component = self.get_object()
        serializer = self.get_serializer(component, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "part_assigned",
                    "component": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

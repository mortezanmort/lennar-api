from copy import deepcopy

from django.db.models import Q
from rest_framework import serializers

from .models import Component, Group, Specification


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    components = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Specification
        fields = "__all__"

    def validate_completed(self, value):
        if value and self.instance.components.filter(Q(part_code=None) | Q(part_code="")).exists():
            raise serializers.ValidationError("Cannot complete a specification if any component is missing a part.")

        return value

    def validate(self, data):
        if self.instance and self.instance.completed:
            raise serializers.ValidationError("Cannot modify a specification that has been completed.")

        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    components = serializers.StringRelatedField(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        self.specification = kwargs.pop("specification", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ("specification",)

    def validate_name(self, value):
        if Group.objects.filter(name=value).exclude(specification=self.specification).exists():
            raise serializers.ValidationError(f"The group name '{value}' is already in use by another specification.")

        return value

    def validate(self, data):
        if self.specification and self.specification.completed:
            raise serializers.ValidationError("Cannot create/update a group of a completed specification.")
        return data


class BaseComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        specification = kwargs.pop("specification", None)
        super().__init__(*args, **kwargs)

        self.specification = self.instance_specification or specification

    @property
    def instance_specification(self):
        if hasattr(self, "instance") and isinstance(self.instance, Component):
            return self.instance.specification
        return None

    def validate(self, data):
        if self.specification and self.specification.completed:
            raise serializers.ValidationError("Cannot create/update a component of a completed specification.")

        return data


class ComponentSerializer(BaseComponentSerializer):
    class Meta:
        model = Component
        fields = "__all__"
        read_only_fields = ("specification",)

    def validate_group(self, value):
        if self.specification and value.specification != self.specification:
            raise serializers.ValidationError("Group must be in the same specification as the component.")

        return value


class PartCodeAssignmentSerializer(BaseComponentSerializer):
    class Meta:
        model = Component
        fields = ["part_code"]


class SpecificationCloneSerializer(serializers.Serializer):
    include_parts = serializers.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        self.specification = kwargs.pop("specification", None)

        super().__init__(*args, **kwargs)

    def validate(self, data):
        if self.specification is None:
            raise serializers.ValidationError("Specification must be specified.")

        if self.specification.status not in ["Planning Phase", "Planning Ready"]:
            raise serializers.ValidationError("Only specifications in Planning Phase or Planning Ready can be cloned.")

        return super().validate(data)

    def clone(self):
        cloned_specification = deepcopy(self.specification)
        include_parts = self.validated_data.get("include_parts", False)

        cloned_specification.pk = None
        cloned_specification.status = "Planning Phase" if not include_parts else "Design Phase"
        cloned_specification.save()

        cloned_groups = {
            group.name: self.clone_group(group, cloned_specification) for group in self.specification.groups.all()
        }
        cloned_components = [
            self.clone_component(component, cloned_groups[component.group.name], cloned_specification, include_parts)
            for component in self.specification.components.all()
        ]
        Group.objects.bulk_create(cloned_groups.values())
        Component.objects.bulk_create(cloned_components)

        return cloned_specification

    def clone_group(self, group, specification):
        group.pk = None
        group.specification = specification

        return group

    def clone_component(self, component, group, specification, include_parts):
        component.pk = None
        component.group = group
        if not include_parts:
            component.part_code = None
        component.specification = specification

        return component


class GroupImportSerializer(GroupSerializer):
    components = ComponentSerializer(many=True)


class SpecificationImportExportSerializer(SpecificationSerializer):
    groups = GroupImportSerializer(many=True, required=False)


class SpecificationImportSerializer(serializers.Serializer):
    specifications = SpecificationImportExportSerializer(many=True)

    def create(self, validated_data):
        specifications_data = validated_data["specifications"]
        created_specifications = []

        for spec_data in specifications_data:
            # Extract and pop the nested data for groups
            groups_data = spec_data.pop("groups", [])

            # Create the specification
            specification = self.create_specification(spec_data)

            # Create nested groups and components
            self.create_groups(groups_data, specification)

            created_specifications.append(specification)

        return created_specifications

    def create_specification(self, spec_data):
        """Create a specification instance."""
        return Specification.objects.create(**spec_data)

    def create_groups(self, groups_data, specification):
        """Create group instances and their nested components."""
        for group_data in groups_data:
            components_data = group_data.pop("components", [])
            group = self.create_group(group_data, specification)

            self.create_components(components_data, group, specification)

    def create_group(self, group_data, specification):
        """Create a group instance."""
        group_serializer = GroupSerializer(data=group_data)
        group_serializer.is_valid(raise_exception=True)

        return group_serializer.save(specification=specification)

    def create_components(self, components_data, group=None, specification=None):
        """Create component instances."""
        component_serializer = ComponentSerializer(data=components_data, many=True)
        component_serializer.is_valid(raise_exception=True)
        component_serializer.save(group=group, specification=specification)

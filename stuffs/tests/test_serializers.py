from django.core.management import call_command
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from stuffs.models import Component, Group, Specification
from stuffs.serializers import (
    ComponentSerializer,
    GroupSerializer,
    PartCodeAssignmentSerializer,
    SpecificationCloneSerializer,
    SpecificationSerializer,
)


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "test_data.json")


class SpecificationSerializerTest(BaseTest):
    def test_validate_completed(self):
        specification = Specification.objects.get(pk=1)
        serializer = SpecificationSerializer(specification, data={"completed": True}, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_completed_with_parts(self):
        component = Component.objects.get(pk=1)
        component.part_code = "PART001"
        component.save()
        specification = Specification.objects.get(pk=1)
        serializer = SpecificationSerializer(specification, data={"completed": True}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["completed"], True)

    def test_validate_modification_of_completed_specification(self):
        specification = Specification.objects.get(pk=1)
        specification.completed = True
        specification.save()
        serializer = SpecificationSerializer(specification, data={"name": "New Name"}, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class GroupSerializerTest(BaseTest):
    def test_validate_name(self):
        another_specification = Specification.objects.get(pk=2)
        Group.objects.create(name="Test Group", group_code="GRP003", specification=another_specification)
        specification = Specification.objects.get(pk=1)
        serializer = GroupSerializer(data={"name": "Test Group", "group_code": "GRP004"}, specification=specification)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_group_creation_in_completed_specification(self):
        specification = Specification.objects.get(pk=1)
        specification.completed = True
        specification.save()
        serializer = GroupSerializer(data={"name": "New Group", "group_code": "GRP003"}, specification=specification)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ComponentSerializerTest(BaseTest):
    def test_validate_group(self):
        specification = Specification.objects.get(pk=1)
        Specification.objects.get(pk=2)
        another_group = Group.objects.get(pk=2)
        serializer = ComponentSerializer(
            data={
                "name": "Component 1",
                "description": "A test component",
                "part_code": "PART002",
                "group": another_group.id,
            },
            specification=specification,
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_component_creation_in_completed_specification(self):
        specification = Specification.objects.get(pk=1)
        specification.completed = True
        specification.save()
        group = Group.objects.get(pk=1)
        serializer = ComponentSerializer(
            data={
                "name": "New Component",
                "description": "A new component",
                "part_code": "PART002",
                "group": group.id,
            },
            specification=specification,
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class PartCodeAssignmentSerializerTest(BaseTest):
    def test_part_code_assignment(self):
        component = Component.objects.get(pk=1)
        serializer = PartCodeAssignmentSerializer(component, data={"part_code": "PART001"}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["part_code"], "PART001")


class SpecificationCloneSerializerTest(BaseTest):
    def test_clone_specification(self):
        specification = Specification.objects.get(pk=1)
        data = {"include_parts": True}
        serializer = SpecificationCloneSerializer(data=data, specification=specification)
        self.assertTrue(serializer.is_valid())
        cloned_specification = serializer.clone()

        self.assertNotEqual(cloned_specification.pk, specification.pk)
        self.assertEqual(cloned_specification.status, "Design Phase")
        self.assertEqual(cloned_specification.groups.count(), specification.groups.count())
        self.assertEqual(cloned_specification.components.count(), specification.components.count())

    def test_validate_clone(self):
        data = {"include_parts": True}
        serializer = SpecificationCloneSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

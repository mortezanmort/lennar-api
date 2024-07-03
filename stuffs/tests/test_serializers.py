from django.test import TestCase
from rest_framework.exceptions import ValidationError

from stuffs.factories import ComponentFactory, GroupFactory, SpecificationFactory
from stuffs.serializers import (
    ComponentSerializer,
    GroupSerializer,
    PartCodeAssignmentSerializer,
    SpecificationCloneSerializer,
    SpecificationSerializer,
)


class SpecificationSerializerTest(TestCase):
    def setUp(self):
        self.specification = SpecificationFactory()
        self.group = GroupFactory(specification=self.specification)
        self.component = ComponentFactory(specification=self.specification, group=self.group)

    def test_validate_completed(self):
        self.specification.completed = True
        serializer = SpecificationSerializer(self.specification, data={"completed": True}, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_completed_with_parts(self):
        self.component.part_code = "PART001"
        self.component.save()
        serializer = SpecificationSerializer(self.specification, data={"completed": True}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["completed"], True)

    def test_validate_modification_of_completed_specification(self):
        self.specification.completed = True
        self.specification.save()
        serializer = SpecificationSerializer(self.specification, data={"name": "New Name"}, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class GroupSerializerTest(TestCase):
    def setUp(self):
        self.specification = SpecificationFactory()
        self.group = GroupFactory(specification=self.specification)

    def test_validate_name(self):
        another_specification = SpecificationFactory()
        GroupFactory(name="Test Group", specification=another_specification)
        serializer = GroupSerializer(
            data={"name": "Test Group", "group_code": "GRP004"}, specification=self.specification
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_group_creation_in_completed_specification(self):
        self.specification.completed = True
        self.specification.save()
        serializer = GroupSerializer(
            data={"name": "New Group", "group_code": "GRP003"}, specification=self.specification
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ComponentSerializerTest(TestCase):
    def setUp(self):
        self.specification = SpecificationFactory()
        self.group = GroupFactory(specification=self.specification)
        self.component = ComponentFactory(specification=self.specification, group=self.group)

    def test_validate_group(self):
        another_specification = SpecificationFactory()
        another_group = GroupFactory(specification=another_specification)
        serializer = ComponentSerializer(
            data={
                "name": "Component 1",
                "description": "A test component",
                "part_code": "PART002",
                "group": another_group.id,
            }
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_component_creation_in_completed_specification(self):
        self.specification.completed = True
        self.specification.save()
        serializer = ComponentSerializer(
            data={
                "name": "New Component",
                "description": "A new component",
                "part_code": "PART002",
                "group": self.group.id,
            }
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class PartCodeAssignmentSerializerTest(TestCase):
    def setUp(self):
        self.component = ComponentFactory(part_code="")

    def test_part_code_assignment(self):
        serializer = PartCodeAssignmentSerializer(self.component, data={"part_code": "PART001"}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["part_code"], "PART001")


class SpecificationCloneSerializerTest(TestCase):
    def setUp(self):
        self.specification = SpecificationFactory()
        self.group = GroupFactory(specification=self.specification)
        self.component = ComponentFactory(specification=self.specification, group=self.group)

    def test_clone_specification(self):
        data = {"include_parts": True}
        serializer = SpecificationCloneSerializer(data=data, specification=self.specification)
        self.assertTrue(serializer.is_valid())
        cloned_specification = serializer.clone()

        self.assertNotEqual(cloned_specification.pk, self.specification.pk)
        self.assertEqual(cloned_specification.status, "Design Phase")
        self.assertEqual(cloned_specification.groups.count(), self.specification.groups.count())
        self.assertEqual(cloned_specification.components.count(), self.specification.components.count())

    def test_validate_clone(self):
        data = {"include_parts": True}
        serializer = SpecificationCloneSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..factories import SpecificationFactory


class BuiltSpecificationsReportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/stuffs/specifications/export_built_specification_report/"

        # Create specifications with different statuses
        self.spec1 = SpecificationFactory(code_number="SPEC001", status="Built")
        self.spec2 = SpecificationFactory(code_number="SPEC001", status="Built")
        self.spec3 = SpecificationFactory(code_number="SPEC002", status="Built")
        self.spec4 = SpecificationFactory(code_number="SPEC003", status="Planning Phase")

    def test_export_built_specification_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.content.decode("utf-8")
        lines = content.split("\n")
        self.assertEqual(lines[0], "Specification Code,Number of Built Specifications")
        self.assertIn("SPEC001,2", lines)
        self.assertIn("SPEC002,1", lines)
        self.assertNotIn("SPEC003", lines)

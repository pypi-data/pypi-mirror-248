# django_auto_permissions/auto_permissions/tests/test_viewset_analysis.py

from django.test import TestCase
from auto_permissions.viewset_analysis import get_custom_methods

class ViewsetAnalysisTests(TestCase):

    def test_get_custom_methods(self):
        class TestViewSet:
            def list(self):
                pass

            def custom_method(self):
                pass

        expected_methods = ['custom_method']
        self.assertEqual(get_custom_methods(TestViewSet), expected_methods)

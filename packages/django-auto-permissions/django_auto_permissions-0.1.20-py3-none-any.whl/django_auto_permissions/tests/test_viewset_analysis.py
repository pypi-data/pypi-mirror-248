

from django.test import TestCase

class ViewsetAnalysisTests(TestCase):

    def test_get_custom_methods(self):
        class TestViewSet:
            def list(self):
                pass

            def custom_method(self):
                pass

        expected_methods = ['custom_method']
        self.assertEqual(get_custom_methods(TestViewSet), expected_methods)

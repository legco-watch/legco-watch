import logging
from django.test import TestCase
from raw.models import RawMember, Override


logging.disable(logging.CRITICAL)


class OverrideTestCase(TestCase):
    def setUp(self):
        self.obj = RawMember.objects.create()

    def test_create_from(self):
        override = Override.objects.create_from(self.obj)
        self.assertEqual(override.ref_model, self.obj._meta.model_name)
        self.assertEqual(override.ref_id, self.obj.id)

    def test_get_from_reference(self):
        override = Override.objects.create_from(self.obj)
        override.save()
        ref = Override.objects.get_from_reference(self.obj)
        self.assertEqual(ref, override)

    def test_get_from_reference_none(self):
        ref = Override.objects.get_from_reference(self.obj)
        self.assertIsNone(ref)

    def test_get_reference(self):
        override = Override.objects.create_from(self.obj)
        ref = override.get_reference()
        self.assertEqual(ref, self.obj)

    def test_get_model(self):
        override = Override.objects.create_from(self.obj)
        mdl = override._get_model()
        self.assertEqual(mdl, RawMember)

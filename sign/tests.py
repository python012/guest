from django.test import TestCase
from sign.models import Event, Guest

class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1,
                             name="iPhone X event",
                             status=True,
                             limit=2000,
                             address='somewhere in USA',
                             start_time='2015-09-08 14:12:00')
        Guest.objects.create(id=1,
                             event_id=1,
                             realname='Tim Cook',
                             phone='9810921',
                             email='tim.cook@apple.com',
                             sign=False)
    
    def test_event_models(self):
        result = Event.objects.get(name="iPhone X event")
        self.assertEqual(result.address, 'somewhere in USA')
        self.assertTrue(result.status)
    
    def test_guest_models(self):
        result = Guest.objects.get(phone="9810921")
        self.assertEqual(result.realname, 'Tim Cook')
        self.assertFalse(result.sign)

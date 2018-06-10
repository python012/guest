from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User


class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1,
                             name="iPhone X event",
                             status=True,
                             attendees_limit=2000,
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


class IndexPageTest(TestCase):

    def test_index_page_renders_index_template(self):
        '''test index view'''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    '''
    test login action
    '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@dj.com', 'admin123456')

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@dj.com')

    def test_login_action_user_password_null(self):
        '''test login when username and password are null'''

        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password is not correct!',
                      response.content)

    def test_login_action_user_password_error(self):
        '''test login when username and password are not correct'''

        test_data = {'username': 'admin', 'password': 'incorrect-password'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password is not correct!',
                      response.content)

    def test_login_action_success(self):
        '''tes login when username and password are correct'''

        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    '''
    test event manage
    '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@dj.com', 'admin123456')
        Event.objects.create(id=1,
                             name="Moto X",
                             attendees_limit="1000",
                             address="Sunnyvale",
                             status=1,
                             start_time="2014-8-12 12:30:00")
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Moto X", response.content)
        self.assertIn(b"Sunnyvale", response.content)
    
    def test_event_manage_search_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {"name": "Moto"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Moto X", response.content)
        self.assertIn(b"Sunnyvale", response.content)


class GuestManageTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@dj.com', 'admin123456')
        Event.objects.create(id=1,
                             name="Moto X",
                             attendees_limit="1000",
                             address="Sunnyvale",
                             status=1,
                             start_time="2014-8-12 12:30:00")
        Guest.objects.create(realname='John',
                             phone='18612341234',
                             email='joh@yu.com',
                             sign=False,
                             event_id=1)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_guest_manage_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John", response.content)
        self.assertIn(b"18612341234", response.content)
    
    def test_guest_manage_search(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_guest/', {'name': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John", response.content)
        self.assertIn(b"18612341234", response.content)


class SignIndexActionTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@wi.com', 'admin123456')
        Event.objects.create(id=1,
                             name="Moto X Release",
                             attendees_limit="1000",
                             address="Sunnyvale",
                             status=1,
                             start_time="2014-8-12 12:30:00")
        Event.objects.create(id=2,
                             name="iPhone X Release",
                             attendees_limit="800",
                             address="Pala Anto",
                             status=1,
                             start_time="2016-6-12 9:30:00")
        Guest.objects.create(realname='John',
                             phone='18612341234',
                             email='joh@yu.com',
                             sign=False,
                             event_id=1)
        Guest.objects.create(realname='Elena',
                             phone='0109872',
                             email='elena@apple.com',
                             sign=True,
                             event_id=2)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_sign_index_action_phone_null(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone": ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone number error", response.content)
    
    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone": '0109872'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone number or event id error", response.content)
    
    def test_sign_index_action_guest_already_signed(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {"phone": '0109872'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"guest already sign in", response.content)

    def test_sign_index_action_sign_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone": '18612341234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"guest sign in successfully!", response.content)

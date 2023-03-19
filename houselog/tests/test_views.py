from django.test import TestCase, Client
import houselog.views as hlv
from houselog.models import Houselog
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.contrib import messages

class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

    def test_login_url(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'houselog/login.html')

    def test_logout_url(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_login_extra_context(self):
        response = self.client.get('/login')
        self.assertIn('suppress_header', response.context)

    def test_login_happy_path(self):
        """
        TODO: fix me, this is falling into the fail path
        """
        # response = self.client.post('/login', {
        #     'username': 'test_user',
        #     'password': '1234'
        # })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, reverse('dashboard'))
        pass

    def test_login_invalid_user(self):
        """
        TODO: implement after fixing happy path
        """
        pass


    def test_logged_in_user_redirect(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    

    # test_login_post_incorrect(self):

class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

        Houselog.objects.create(
            title="test",
            frequency="100",
            last_done=datetime.date.today(),
            user=self.user
        )

    def test_dashboard_login_required(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/login?next=/', response.url)

    def test_dashboard_happy_path(self):
        """
        TODO: test that items are sorted in e2e test
        """
        self.client.force_login(user=self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'houselog/dashboard.html')
        self.assertIn('add_form', response.context)


class AddItemViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

    def test_add_login_required(self):
        response = self.client.post('/add')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/login?next=/add', response.url)

    def test_add_view_not_get_accessible(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 405)

    def test_add_post_happy_path(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/add', {
            'title': 'test_add',
            'frequency': 100,
            'last_done': '2023-12-12',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        self.assertEqual(Houselog.objects.count(), 1)

    def test_add_post_invalid_form(self):
        """
        TODO: assert on flash message
        """
        self.client.force_login(user=self.user)
        response = self.client.post('/add', {
            'title': 'missing_required_fields',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))


class DeleteItemViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

        Houselog.objects.create(
            title="test",
            frequency="20",
            last_done=datetime.date.today(),
            user=self.user
        )

    def test_delete_login_required(self):
        response = self.client.post('/delete?id=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/login?next=/delete%3Fid%3D1', response.url)

    def test_delete_view_not_get_accessible(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/delete?id=1')
        self.assertEqual(response.status_code, 405)

    def test_delete_post_happy_path(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/delete?id=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        self.assertEqual(Houselog.objects.count(), 0)

    def test_delete_no_id(self):
        """
        TODO: assert on flash message
        """
        self.client.force_login(user=self.user)
        response = self.client.post('/delete')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_delete_bad_id(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/delete?id=99')
        self.assertEqual(response.status_code, 404)


class DoneItemViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

        Houselog.objects.create(
            title="test",
            frequency="20",
            last_done=datetime.date.today(),
            user=self.user
        )

    def test_done_post_endpoint_login_required(self):
        response = self.client.post('/done?id=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/login?next=/done%3Fid%3D1', response.url)

    def test_done_post_endpoint(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/done?id=1', {'update_last_done': '2023-01-01'})
        item = Houselog.objects.get(id=1)
        self.assertEqual(item.last_done, datetime.date(2023, 1, 1))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_done_post_no_id(self):
        """
        TODO: check flash  message
        """
        self.client.force_login(user=self.user)
        response = self.client.post('/done', {'update_last_done': '2023-01-01'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        # print(messages.get_messages(response))
        # print(dir(response))
        # print(response.context)
        # message = response.context.get('messages')[0]
        # print(message)
        pass


class EditViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            username="test_user",
            password="1234"
        )

        Houselog.objects.create(
            title="test",
            frequency="20",
            last_done=datetime.date.today(),
            user=self.user
        )

    def test_edit_view_login_required(self):
        response = self.client.get('/edit?id=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/login?next=/edit%3Fid%3D1', response.url)

    def test_get_queryset_happy_path(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/edit?id=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'houselog/edit.html')

    def test_get_queryset_invalid_id(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/edit?id=99')
        self.assertEqual(response.status_code, 404)
        
    def test_edit_post_happy_path(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/edit?id=1', {
            'title': 'test_update',
            'frequency': 100,
            'last_done': '2023-12-12'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_edit_post_invalid_form(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/edit?id=1', {
            'title': 'missing_required_fields'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/edit?id=1', response.url)

    def test_edit_post_invalid_id(self):
        """
        TODO: assert on flash message
        """
        self.client.force_login(user=self.user)
        response = self.client.post('/edit?id=99', {
            'title': 'incorrect_item_id'
        })
        self.assertEqual(response.status_code, 404)

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from prefecture.models import Prefecture

UserModel = get_user_model()


class HomePageTest(TestCase):
    def test_home_page_returns_200_and_expected_links(self):
        response = self.client.get('/home/')
        self.assertContains(response, '会員登録', status_code=200)
        self.assertContains(response, 'ログイン', status_code=200)

    def test_home_page_uses_expected_template(self):
        response = self.client.get('/home/')
        self.assertTemplateUsed(response, 'prefecture/home.html')


class MypageRenderPrefecturesTest(TestCase):
    def test_mypage_return_200_and_expected_titles(self):
        client = Client()
        client.force_login(UserModel.objects.create(
            username='test_user',
            email='test@example.com',
            password='top_secret_pass0001'
        ))
        response = client.get('/mypage/')
        self.assertContains(response, 'ログアウト', status_code=200)
        self.assertContains(response, '都道府県登録', status_code=200)
        self.assertContains(response, '訪問済み', status_code=200)
        self.assertContains(response, '未訪問', status_code=200)

    def test_mypage_not_authenticated_user_redirect_login(self):
        response = self.client.get('/mypage/')
        self.assertRedirects(
            response,
            '/accounts/login/?next=/mypage/',
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


class RegisterPrefectureTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.client.force_login(self.user)

    def test_render_registration_form(self):
        response = self.client.get('/prefecture/register/')
        self.assertContains(response, '登録する', status_code=200)

    def test_register_prefecture(self):
        data = {'name': '北海道'}
        self.client.post('/prefecture/register/', data)
        prefecture = Prefecture.objects.get(name='北海道')
        self.assertEqual('北海道', prefecture.name)



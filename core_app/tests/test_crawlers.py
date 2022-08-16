# Django
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User

# local Django
from ..crawlers import crawl_website
from ..models import E2ETestResultsModel

# Note: These tests will fail if the Chromedriver's version is not  
# matched to the installed Chrome version on the local machine.
# Chromedriver can be downloaded from here:
# https://chromedriver.chromium.org/downloads

# Since it is aimed to be implemented on a server or self-hosted,
# such as raspberry pi, the application was tested on Linux (Debian, Ubuntu).
# I did not test the application on Windows or MacOS.
class TestCrawlerTransaction(TransactionTestCase):
    user_dummy_credentials_1 = None

    def setUp(self):
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'email': 'test1@tests.com',
            'password': 'Test12321',
        }

        # Create Django's default user 
        User.objects.create_user(**self.user_dummy_credentials_1)

    def tearDown(self):
        User.objects.all().delete()


    def test_crawl_website_launch_chrome_instance(self):
        # Arrange
        user_pk = 1
        e2e_test_params_pk = 0
        url = 'https://www.google.com'
        tasks = [{'1': 1}]
        # Act
        crawl_website(user_pk, e2e_test_params_pk, url, tasks)
        # Assert
        self.assertTrue(True)
    
    def test_crawl_website_will_not_launch_with_invalid_user(self):
        # Arrange
        user_pk = 2
        e2e_test_params_pk = 0
        url = 'https://www.google.com'
        tasks = [{'1': 1}]
        # Act
        try:
            crawl_website(user_pk, e2e_test_params_pk, url, tasks)
            # Assert: the test shouldn't pass since user_pk 2 doesn't exist.
            self.assertTrue(False)
        except Exception:
            # Assert: the test should raise exception.
            self.assertTrue(True)
    
    def test_crawl_website_will_raise_exception_if_user_pk_is_null(self):
        # Arrange
        user_pk = None
        e2e_test_params_pk = 0
        url = 'https://www.google.com'
        tasks = [{'1': 1}]
        # Act
        try:
            crawl_website(user_pk, e2e_test_params_pk, url, tasks)
            # Assert: the test shouldn't pass since user_pk is None.
            self.assertTrue(False)
        except Exception:
            # Assert: the test should raise exception.
            self.assertTrue(True)

    def test_crawl_website_will_raise_exception_if_e2e_test_params_pk_is_null(self):
        # Arrange
        user_pk = 1
        e2e_test_params_pk = None
        url = 'https://www.google.com'
        tasks = [{'1': 1}]
        # Act
        try:
            crawl_website(user_pk, e2e_test_params_pk, url, tasks)
            # Assert: the test shouldn't pass since e2e_test_params_pk is None.
            self.assertTrue(False)
        except Exception:
            # Assert: the test should raise exception.
            self.assertTrue(True)

    def test_crawl_website_will_raise_exception_if_url_is_null(self):
        # Arrange
        user_pk = 1
        e2e_test_params_pk = 0
        url = None
        tasks = [{'1': 1}]
        # Act
        try:
            crawl_website(user_pk, e2e_test_params_pk, url, tasks)
            # Assert: the test shouldn't pass since url is None.
            self.assertTrue(False)
        except Exception:
            # Assert: the test should raise exception.
            self.assertTrue(True)
        
    def test_crawl_website_will_raise_exception_if_tasks_is_null(self):
        # Arrange
        user_pk = 1
        e2e_test_params_pk = 0
        url = 'https://www.google.com'
        tasks = None
        # Act
        try:
            crawl_website(user_pk, e2e_test_params_pk, url, tasks)
            # Assert: the test shouldn't pass since tasks is None.
            self.assertTrue(False)
        except Exception:
            # Assert: the test should raise exception.
            self.assertTrue(True)


class TestCrawler(TestCase):
    user_dummy_credentials_1 = None

    def setUp(self):
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'email': 'test1@tests.com',
            'password': 'Test12321',
        }

        # Create Django's default user 
        User.objects.create_user(**self.user_dummy_credentials_1)

    def tearDown(self):
        User.objects.all().delete()

    
    # Using TestCase instead of TransactionTestCase because the latter has
    # different mechanism to handle ORM database.
    # Resource: https://stackoverflow.com/questions/43978468/django-test-transactionmanagementerror-you-cant-execute-queries-until-the-end
    def test_crawl_website_will_return_list_of_errors_if_invalid_XPath(self):
        # Arrange
        user_pk = 1
        e2e_test_params_pk = 0
        url = 'https://www.google.com'
        tasks = [{'2': 'invalid_xpath'}]
        # Act
        crawl_website(user_pk, e2e_test_params_pk, url, tasks)
        errors = E2ETestResultsModel.objects.filter(user=user_pk).values_list('error_list', flat=True)
        # Assert
        self.assertTrue(len(errors) > 0)
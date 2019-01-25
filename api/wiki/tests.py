from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from .models import (
    VersionModel,
    PageModel
)


class WikiTests(APITestCase):

    def setUp(self):
        self.main_page = PageModel.objects.create(
            title='Hello',
            text='World'
        )

    def test_create_wiki_page(self):
        """
        Ensure we can create a new page object.
        """
        url = reverse('wiki:page-create')
        data = {'title': 'aaa',
                'text': 'bbb'}
        response = self.client.post(url, data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PageModel.objects.count(), 2)
        self.assertEqual(VersionModel.objects.count(), 2)
        self.assertEqual(PageModel.objects.get(id=response_data['id']).title, 'aaa')
        self.assertEqual(PageModel.objects.get(id=response_data['id']).text, 'bbb')
        self.assertIn('id', response_data)
        self.assertIn('title', response_data)
        self.assertIn('text', response_data)

    def test_get_all_wiki_pages(self):
        """
        Ensure we can get list of pages.
        """
        url = reverse('wiki:pages-list')
        response = self.client.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {'id': 3, 'title': 'Hello', 'text': 'World'})


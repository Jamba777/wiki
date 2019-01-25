from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
        self.old_version = VersionModel.objects.create(
            current=False,
            page_id=self.main_page.id,
            text='11111'
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
        self.assertEqual(VersionModel.objects.count(), 3)
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
        self.assertEqual(data[0]['title'], 'Hello')
        self.assertEqual(data[0]['text'], 'World')

    def test_get_all_version_of_given_page(self):
        """
        Ensure we can get list of pages.
        """
        url = reverse('wiki:pages-versions', kwargs=dict(pk=self.main_page.id))
        response = self.client.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'Hello')
        self.assertEqual(data['text'], 'World')
        self.assertIn('versions', data)
        self.assertIn('id', data)
        self.assertEqual(len(data['versions']), 2)

    def test_update_current_page(self):
        """
        Ensure we can update current page ang get relevant data.
        """
        url = reverse('wiki:page-update', kwargs=dict(pk=self.main_page.id))
        response = self.client.patch(url, data=dict(text='ooo'), format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'Hello')
        self.assertEqual(data['text'], 'ooo')
        self.assertIn('id', data)

    def test_get_another_version_page(self):
        """
        Ensure we can get another version of given page.
        """
        url = reverse(
            'wiki:page-get-version',
            kwargs=dict(
                pk=self.main_page.id,
                version_id=self.old_version.id
            )
        )
        response = self.client.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'Hello')
        self.assertEqual(data['text'], '11111')
        self.assertIn('id', data)

    def test_set_another_version_to_page(self):
        """
        Ensure we can set another version of given page.
        """
        url = reverse(
            'wiki:page-set-current',
            kwargs=dict(
                pk=self.main_page.id,
                version_id=self.old_version.id
            )
        )
        response = self.client.post(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'Hello')
        self.assertEqual(data['text'], '11111')
        self.assertIn('id', data)

from django.db import transaction

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import ValidationError

from .models import (
    PageModel,
    VersionModel
)


class PageSerializer(ModelSerializer):

    class Meta:
        model = PageModel
        fields = '__all__'


class VersionSerializer(ModelSerializer):

    class Meta:
        model = VersionModel
        fields = ['id', 'create_date', 'current', 'text', 'page']
        read_only_fields = fields

    def set_current(self):

        page = self.instance.page
        version = self.instance

        with transaction.atomic():
            page.text = version.text
            page.page_versions.filter(
                current=True
            ).update(
                current=False
            )
            version.current = True
            page.save(update_fields=['text'])
            version.save(update_fields=['current'])

        return version


class PageVersionsSerializer(PageSerializer):
    versions = VersionSerializer(many=True, source='page_versions')

    class Meta(PageSerializer.Meta):
        fields = ('id', 'text', 'title', 'versions')


class PageSingleVersionsSerializer(PageSerializer):

    class Meta(PageSerializer.Meta):
        fields = ('id', 'text', 'title')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        version = instance.page_versions.get(id=self.context['version_id'])
        data['text'] = version.text
        return data


class PageUpdateSerializer(ModelSerializer):

    class Meta(PageSerializer.Meta):
        read_only_fields = ['title']

    def validate(self, attrs):
        if 'text' not in attrs:
            raise ValidationError
        return super().validate(attrs)

    def update(self, instance, validated_data):

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            instance.page_versions.filter(
                current=True
            ).update(
                current=False
            )

            VersionModel.objects.create(
                text=instance.text,
                page_id=instance.id
            )
        return instance


class PageSetCurrentVersionOutSerializer(ModelSerializer):

    class Meta(PageSerializer.Meta):
        read_only_fields = ['title', 'text']
        
    





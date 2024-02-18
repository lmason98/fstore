from django.conf import settings
from rest_framework.fields import CharField, IntegerField, DateTimeField, SerializerMethodField
from rest_framework.serializers import Serializer


class BaseDataSerializer(Serializer):

	id = IntegerField()
	name = CharField()
	updated = DateTimeField(format=settings.REST_FRAMEWORK['DATETIME_FORMAT'], read_only=True, source='updated_at')

	class Meta:
		fields = ('id', 'name', 'updated')


class FolderSerializer(BaseDataSerializer):

	type = SerializerMethodField('get_type')

	class Meta:
		fields = BaseDataSerializer.Meta.fields + ('type',)

	@staticmethod
	def get_type(_):
		return 'folder'


class BlobSerializer(BaseDataSerializer):

	type = SerializerMethodField('get_type')
	size = CharField(source='size_display')

	class Meta:
		fields = BaseDataSerializer.Meta.fields + ('type', 'size')

	@staticmethod
	def get_type(_):
		return 'file'

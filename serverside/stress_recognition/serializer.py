from rest_framework import serializers
from .models import UserCondition


class UserConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCondition
        fields = ('user_name', 'expression', 'weather', 'temp_max', 'temp_min', 'diff_tmp', 'humidity', 'predicted')

'''
class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
'''

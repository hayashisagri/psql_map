from rest_framework import serializers

from prefecture.models import Prefecture


class PrefectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prefecture
        fields = ('name', 'user_id')

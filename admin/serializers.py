from rest_framework import serializers
from admin.models import Advisor

class Serial(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('id', 'name', 'profile_pic_url')

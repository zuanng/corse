from rest.models import Breed, Cat
from rest_framework import serializers

class BreedSerializer(serializers.ModelSerializer):
    # Thêm computed field để đếm số cats
    cat_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Breed
        fields = ('id', 'name', 'cat_count')
        
    def get_cat_count(self, obj):
        """SerializerMethodField để tính số lượng cats của breed này"""
        return obj.cat_set.count()

class CatSerializer(serializers.ModelSerializer):
    # Nested breed info
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    
    class Meta:
        model = Cat
        fields = ('id', 'nickname', 'weight', 'foods', 'breed', 'breed_name')
    
    def validate_weight(self, value):
        """Field-level validation cho weight"""
        if value <= 0:
            raise serializers.ValidationError("Weight must be positive")
        if value > 50:
            raise serializers.ValidationError("Weight seems too high for a cat")
        return value

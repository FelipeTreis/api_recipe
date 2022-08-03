from rest_framework import serializers
from tag.models import Tag

from recipes.models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'description',
            'author', 'category', 'tags',
            'public', 'preparation',
            'tags_objects', 'tag_link',
        )

    public = serializers.BooleanField(
        source='is_published', read_only=True,
    )
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    tags_objects = TagSerializer(
        many=True, source='tags', read_only=True,
    )
    tag_link = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

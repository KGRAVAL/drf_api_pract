from rest_framework import serializers
from .models import BookData


class BookDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookData
        fields = ["book_name", "author_name", "book_price", "published_date", "copies_available", "available_sw_cpy"]

    # book_name = serializers.CharField(max_length=255)    # author_name = serializers.CharField(max_length=255)
    # book_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    # published_date = serializers.DateField()
    # copies_available = serializers.IntegerField()
    # available_sw_cpy = serializers.BooleanField(default=False)


class AddBookData(serializers.Serializer):
    pass


class ViewBookData(serializers.Serializer):
    pass


class DeleteBookData(serializers.Serializer):
    pass


class UpdateBookData(serializers.Serializer):
    pass

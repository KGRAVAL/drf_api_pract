from django.contrib import admin
from bookmanage.models import BookData


@admin.register(BookData)
class BookDataAdmin(admin.ModelAdmin):
    list_display = ["id", "book_name", "author_name", "book_price", "published_date", "copies_available",
                    "available_sw_cpy"]

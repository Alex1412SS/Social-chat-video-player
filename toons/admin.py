from django.contrib import admin
from .models import toons_model, category, toon_series, genre, Review, authors, Review_review

admin.site.register(Review)
admin.site.register(Review_review)
admin.site.register(authors)
admin.site.register(toons_model)
admin.site.register(category)
admin.site.register(toon_series)
admin.site.register(genre)



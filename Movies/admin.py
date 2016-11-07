from django.contrib import admin
from models import Movie,Cast,Movie_Meta,Show,Ticket
# Register your models here.

admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Movie_Meta)
admin.site.register(Show)
admin.site.register(Ticket)
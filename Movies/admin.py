from django.contrib import admin
from models import Movie,Cast,Movie_Meta,Show,Ticket
# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):

        instance = form.save(commit=False)
        instance.user = request.user
        #if not change or not instance.created_by:
            #instance.created_by = user
        #instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):
        if formset.model == Ticket:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                #if not change or not instance.created_by:
                    #instance.created_by = request.user
                #instance.modified_by = request.user
                instance.save()
        else:
            formset.save()

admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Movie_Meta)
admin.site.register(Show)
admin.site.register(Ticket,TicketAdmin)
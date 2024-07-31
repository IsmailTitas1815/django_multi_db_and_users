from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from listing.extras import delete_realtors_listing_data
from django.contrib.auth.models import Permission

class UserAdmin(admin.ModelAdmin):
    using = 'users'
    list_display = ('id', 'name', 'email', )
    list_display_links = ('id', 'name', 'email', )
    search_fields = ('name', 'email', )
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        email = obj.email
        obj.delete(using=self.using)
        delete_realtors_listing_data(email)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

class PermissionAdmin(admin.ModelAdmin):
    using = 'users'
    list_display = ('id','codename', 'name', 'content_type', )
    list_display_links = ('id','codename', 'name', 'content_type',  )
    search_fields = ('id', 'name', 'codename', )
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)

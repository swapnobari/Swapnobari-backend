from django.contrib import admin

# Register your models here.

admin.site.site_header = "Swapno Bari Housing Ltd. Admin"
admin.site.site_title = "Swapno Bari Admin"
admin.site.index_title = "Dashboard"


class SingletonAdmin(admin.ModelAdmin):
    """Admin for SingletonModel: edit the one row, no extra rows, no delete."""
 
    def has_add_permission(self, request):
        return not self.model.objects.exists()
 
    def has_delete_permission(self, request, obj=None):
        return False
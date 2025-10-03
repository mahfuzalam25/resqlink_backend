from django.contrib import admin
from .models import Profile,Location, Experience, Education, Certification

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Certification)

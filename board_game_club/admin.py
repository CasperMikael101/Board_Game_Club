from django.contrib import admin
from .models import BoardGame

# Admin stuff
@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    # Show all board games, owner, creat at when, and is it borrowed
    list_display = ('title', 'owner', 'created_at', 'is_available')  
    search_fields = ('title', 'owner__username')  
    list_filter = ('is_available', 'created_at')  

    # Optionally, you can add more customization, like fieldsets, ordering, etc.
    fieldsets = (
        ('Game Information', {'fields': ('title', 'description', 'owner')}),
        ('Availability', {'fields': ('is_available',)}),
    )
    readonly_fields = ('created_at',)

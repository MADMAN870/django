from django.contrib import admin
from django.utils.html import format_html
from .models import TripCategory, Trip, TripOption, Reservation

@admin.register(TripCategory)
class TripCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'trip_count')
    search_fields = ('name',)

    def trip_count(self, obj):
        return obj.trip_set.count()
    trip_count.short_description = 'Number of Trips'

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'departure_date', 'return_date', 'available_seats', 
                   'price_per_person', 'status', 'image_preview')
    list_filter = ('category', 'departure_date', 'available_seats')
    search_fields = ('name', 'description', 'destination')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image', 'image_preview')
        }),
        ('Trip Details', {
            'fields': ('departure_date', 'return_date', 'departure_location', 'destination')
        }),
        ('Capacity and Pricing', {
            'fields': ('available_seats', 'price_per_person')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'

    def status(self, obj):
        if obj.available_seats > 10:
            color = 'green'
            text = 'Available'
        elif obj.available_seats > 0:
            color = 'orange'
            text = 'Limited'
        else:
            color = 'red'
            text = 'Sold Out'
        return format_html('<span style="color: {};">{}</span>', color, text)
    status.short_description = 'Status'

@admin.register(TripOption)
class TripOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'trip', 'price', 'description')
    list_filter = ('trip',)
    search_fields = ('name', 'description')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip', 'number_of_persons', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'trip', 'created_at')
    search_fields = ('user__username', 'trip__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Reservation Details', {
            'fields': ('user', 'trip', 'number_of_persons', 'children_ages')
        }),
        ('Options and Pricing', {
            'fields': ('selected_options', 'total_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new reservations
            # Update available seats
            obj.trip.available_seats -= obj.number_of_persons
            obj.trip.save()
        super().save_model(request, obj, form, change)

# Customize admin site header and title
admin.site.site_header = 'Travel Agency Management'
admin.site.site_title = 'Travel Agency Portal'
admin.site.index_title = 'Travel Agency Administration'

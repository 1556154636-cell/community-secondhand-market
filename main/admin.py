#coding:utf-8
from django.contrib import admin
from .models import *
from .security_models import SecurityLog, UserSecurityInfo, DataEncryptionRecord, RecommendationRecord, UserBehaviorLog, FailedLoginAttempt


class YonghuAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'phone', 'balance', 'addtime')
    search_fields = ('username', 'name', 'phone')
    list_filter = ('addtime',)
    ordering = ('-addtime',)


class ErshouShangpinAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_type', 'price', 'favorite_count', 'addtime')
    search_fields = ('product_name', 'product_type')
    list_filter = ('product_type', 'addtime')
    ordering = ('-addtime',)


class YonghuShangpinAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_type', 'price', 'is_approved', 'username', 'publish_time')
    search_fields = ('product_name', 'product_type', 'username')
    list_filter = ('is_approved', 'product_type')
    ordering = ('-publish_time',)


class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'username', 'parent_id', 'status', 'is_top', 'addtime')
    search_fields = ('title', 'username')
    list_filter = ('status', 'is_top', 'addtime')
    ordering = ('-addtime',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'addtime')
    search_fields = ('title',)
    ordering = ('-addtime',)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_code', 'product_name', 'total_price', 'order_status', 'user_id', 'create_time')
    search_fields = ('order_code', 'product_name')
    list_filter = ('order_status', 'create_time')
    ordering = ('-create_time',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'quantity', 'unit_price', 'user_id', 'addtime')
    search_fields = ('product_name',)
    ordering = ('-addtime',)


class StoreupAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'collect_type', 'user_id', 'addtime')
    search_fields = ('product_name',)
    list_filter = ('collect_type',)
    ordering = ('-addtime',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver_name', 'phone_number', 'full_address', 'is_default', 'user_id', 'addtime')
    search_fields = ('receiver_name', 'phone_number')
    ordering = ('-addtime',)


class ShangpinLeixingAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'addtime')
    search_fields = ('category_name',)
    ordering = ('-addtime',)


class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action_type', 'target_user', 'ip_address', 'status', 'log_time')
    search_fields = ('action_type', 'target_user', 'ip_address')
    list_filter = ('action_type', 'status', 'log_time')
    ordering = ('-log_time',)


class UserSecurityInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'security_level', 'last_login_time', 'last_login_ip', 'login_failed_count')
    search_fields = ('username',)
    list_filter = ('security_level',)
    ordering = ('-last_login_time',)


class DataEncryptionRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_type', 'encryption_type', 'operation', 'status', 'created_at')
    search_fields = ('data_type', 'encryption_type')
    list_filter = ('encryption_type', 'operation', 'status')
    ordering = ('-created_at',)


class RecommendationRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'algorithm_type', 'score', 'execution_time', 'created_at')
    search_fields = ('user_id', 'algorithm_type')
    ordering = ('-created_at',)


class UserBehaviorLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'behavior_type', 'target_type', 'target_name', 'ip_address', 'created_at')
    search_fields = ('username', 'behavior_type', 'target_name')
    list_filter = ('behavior_type', 'target_type')
    ordering = ('-created_at',)


class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'username', 'attempt_time', 'lock_until')
    search_fields = ('ip_address', 'username')
    ordering = ('-attempt_time',)


admin.site.register(yonghu, YonghuAdmin)
admin.site.register(ershoushangpin, ErshouShangpinAdmin)
admin.site.register(yonghushangpin, YonghuShangpinAdmin)
admin.site.register(forum, ForumAdmin)
admin.site.register(news, NewsAdmin)
admin.site.register(orders, OrdersAdmin)
admin.site.register(cart, CartAdmin)
admin.site.register(storeup, StoreupAdmin)
admin.site.register(address, AddressAdmin)
admin.site.register(shangpinleixing, ShangpinLeixingAdmin)
admin.site.register(config)
admin.site.register(menu)
admin.site.register(users)
admin.site.register(system_notice)
admin.site.register(smsregistercode)

admin.site.register(SecurityLog, SecurityLogAdmin)
admin.site.register(UserSecurityInfo, UserSecurityInfoAdmin)
admin.site.register(DataEncryptionRecord, DataEncryptionRecordAdmin)
admin.site.register(RecommendationRecord, RecommendationRecordAdmin)
admin.site.register(UserBehaviorLog, UserBehaviorLogAdmin)
admin.site.register(FailedLoginAttempt, FailedLoginAttemptAdmin)

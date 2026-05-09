#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主应用URL配置
"""

from django.urls import path
from . import front_views, auth_views, product_views, order_views, admin_views

urlpatterns = [
    # 页面视图
    path('', front_views.index_view, name='index'),
    
    # 用户认证API
    path('api/login', auth_views.api_login, name='api_login'),
    path('api/register', auth_views.api_register, name='api_register'),
    path('api/logout', auth_views.api_logout, name='api_logout'),
    path('api/change_password', auth_views.api_change_password, name='api_change_password'),
    path('api/user_info', auth_views.api_user_info, name='api_user_info'),
    path('api/update_user_info', auth_views.api_update_user_info, name='api_update_user_info'),
    
    # 安全相关API
    path('api/hmac_sign', auth_views.api_hmac_sign, name='api_hmac_sign'),
    path('api/hmac_verify', auth_views.api_hmac_verify, name='api_hmac_verify'),
    path('api/encrypt_data', auth_views.api_encrypt_data, name='api_encrypt_data'),
    path('api/check_password_strength', auth_views.api_check_password_strength, name='api_check_password_strength'),
    path('api/security_logs', auth_views.api_security_logs, name='api_security_logs'),
    path('api/user_security_info', auth_views.api_user_security_info, name='api_user_security_info'),
    
    # 商品API
    path('api/products', front_views.api_products, name='api_products'),
    path('api/product_detail', front_views.api_product_detail, name='api_product_detail'),
    path('api/categories', front_views.api_categories, name='api_categories'),
    
    # 商品管理API
    path('api/publish_product', product_views.api_publish_product, name='api_publish_product'),
    path('api/published_products', product_views.api_published_products, name='api_published_products'),
    path('api/update_product', product_views.api_update_product, name='api_update_product'),
    path('api/delete_published_product', product_views.api_delete_published_product, name='api_delete_published_product'),
    path('api/pending_products', product_views.api_pending_products, name='api_pending_products'),
    path('api/approve_product', product_views.api_approve_product, name='api_approve_product'),
    path('api/search_products', product_views.api_search_products, name='api_search_products'),
    path('api/hot_products', product_views.api_hot_products, name='api_hot_products'),
    path('api/new_products', product_views.api_new_products, name='api_new_products'),
    path('api/product_types', product_views.api_product_types, name='api_product_types'),
    path('api/add_product_type', product_views.api_add_product_type, name='api_add_product_type'),
    path('api/delete_product_type', product_views.api_delete_product_type, name='api_delete_product_type'),
    path('api/price_range', product_views.api_price_range, name='api_price_range'),
    
    # 推荐API
    path('api/recommend', front_views.api_recommend, name='api_recommend'),
    
    # 论坛API
    path('api/forums', front_views.api_forums, name='api_forums'),
    path('api/forum_detail', front_views.api_forum_detail, name='api_forum_detail'),
    path('api/create_forum', front_views.api_create_forum, name='api_create_forum'),
    path('api/reply_forum', front_views.api_reply_forum, name='api_reply_forum'),
    
    # 新闻API
    path('api/news', front_views.api_news, name='api_news'),
    path('api/news_detail', front_views.api_news_detail, name='api_news_detail'),
    
    # 购物车API
    path('api/add_to_cart', front_views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart_list', front_views.api_cart_list, name='api_cart_list'),
    path('api/update_cart', front_views.api_update_cart, name='api_update_cart'),
    path('api/delete_cart', front_views.api_delete_cart, name='api_delete_cart'),
    
    # 收藏API
    path('api/add_favorite', front_views.api_add_favorite, name='api_add_favorite'),
    path('api/favorite_list', front_views.api_favorite_list, name='api_favorite_list'),
    path('api/delete_favorite', front_views.api_delete_favorite, name='api_delete_favorite'),
    
    # 地址API
    path('api/add_address', front_views.api_add_address, name='api_add_address'),
    path('api/address_list', front_views.api_address_list, name='api_address_list'),
    path('api/update_address', front_views.api_update_address, name='api_update_address'),
    path('api/delete_address', front_views.api_delete_address, name='api_delete_address'),
    
    # 订单API
    path('api/create_order', front_views.api_create_order, name='api_create_order'),
    path('api/order_list', front_views.api_order_list, name='api_order_list'),
    path('api/order_detail', front_views.api_order_detail, name='api_order_detail'),
    path('api/update_order', front_views.api_update_order, name='api_update_order'),
    
    # 订单管理API
    path('api/batch_create_order', order_views.api_batch_create_order, name='api_batch_create_order'),
    path('api/pay_order', order_views.api_pay_order, name='api_pay_order'),
    path('api/confirm_receipt', order_views.api_confirm_receipt, name='api_confirm_receipt'),
    path('api/cancel_order', order_views.api_cancel_order, name='api_cancel_order'),
    path('api/order_status_counts', order_views.api_order_status_counts, name='api_order_status_counts'),
    path('api/all_orders', order_views.api_all_orders, name='api_all_orders'),
    path('api/update_order_logistics', order_views.api_update_order_logistics, name='api_update_order_logistics'),
    path('api/order_stats', order_views.api_order_stats, name='api_order_stats'),
    path('api/add_balance', order_views.api_add_balance, name='api_add_balance'),
    
    # 行为记录API
    path('api/record_behavior', front_views.api_record_behavior, name='api_record_behavior'),
    
    # 统计API
    path('api/stats', front_views.api_stats, name='api_stats'),
    
    # 管理员API
    path('api/admin_login', admin_views.api_admin_login, name='api_admin_login'),
    path('api/admin_users', admin_views.api_admin_users, name='api_admin_users'),
    path('api/admin_add_user', admin_views.api_admin_add_user, name='api_admin_add_user'),
    path('api/admin_update_user', admin_views.api_admin_update_user, name='api_admin_update_user'),
    path('api/admin_delete_user', admin_views.api_admin_delete_user, name='api_admin_delete_user'),
    path('api/admin_add_news', admin_views.api_admin_add_news, name='api_admin_add_news'),
    path('api/admin_update_news', admin_views.api_admin_update_news, name='api_admin_update_news'),
    path('api/admin_delete_news', admin_views.api_admin_delete_news, name='api_admin_delete_news'),
    path('api/admin_forums', admin_views.api_admin_forums, name='api_admin_forums'),
    path('api/admin_delete_forum', admin_views.api_admin_delete_forum, name='api_admin_delete_forum'),
    path('api/admin_set_top', admin_views.api_admin_set_top, name='api_admin_set_top'),
    path('api/admin_set_notice', admin_views.api_admin_set_notice, name='api_admin_set_notice'),
    path('api/admin_stats', admin_views.api_admin_stats, name='api_admin_stats'),
    path('api/admin_recent_activities', admin_views.api_admin_recent_activities, name='api_admin_recent_activities'),
]

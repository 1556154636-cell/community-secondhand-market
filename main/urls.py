#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主应用URL配置
"""

from django.urls import path
from . import front_views, auth_views

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
    
    # 行为记录API
    path('api/record_behavior', front_views.api_record_behavior, name='api_record_behavior'),
    
    # 统计API
    path('api/stats', front_views.api_stats, name='api_stats'),
]

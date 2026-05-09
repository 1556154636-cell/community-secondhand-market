#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全日志模型
"""

from django.db import models
from datetime import datetime


class SecurityLog(models.Model):
    """
    安全日志模型
    记录所有安全相关操作
    """
    
    ACTION_TYPES = [
        ('REGISTER_SUCCESS', '注册成功'),
        ('REGISTER_FAILED', '注册失败'),
        ('LOGIN_SUCCESS', '登录成功'),
        ('LOGIN_FAILED', '登录失败'),
        ('LOGOUT', '登出'),
        ('USER_INFO_UPDATE', '用户信息更新'),
        ('PASSWORD_CHANGE', '密码修改'),
        ('ACCESS_DENIED', '访问拒绝'),
        ('SUSPICIOUS_ACTIVITY', '可疑活动'),
        ('DATA_ENCRYPT', '数据加密'),
        ('DATA_DECRYPT', '数据解密'),
    ]
    
    STATUS_CHOICES = [
        ('SUCCESS', '成功'),
        ('FAILED', '失败'),
        ('WARNING', '警告'),
    ]
    
    id = models.AutoField(primary_key=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name='操作类型')
    target_user = models.CharField(max_length=255, null=True, verbose_name='目标用户')
    ip_address = models.CharField(max_length=50, null=True, verbose_name='IP地址')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='状态')
    description = models.TextField(null=True, verbose_name='描述')
    log_time = models.DateTimeField(default=datetime.now, verbose_name='记录时间')
    
    class Meta:
        db_table = 'security_log'
        verbose_name = verbose_name_plural = '安全日志'
        ordering = ['-log_time']


class UserSecurityInfo(models.Model):
    """
    用户安全信息模型
    存储用户的安全相关信息
    """
    
    SECURITY_LEVELS = [
        ('LOW', '低'),
        ('MEDIUM', '中'),
        ('HIGH', '高'),
    ]
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户ID')
    username = models.CharField(max_length=255, verbose_name='用户名')
    password_salt = models.CharField(max_length=64, verbose_name='密码盐值')
    last_login_time = models.DateTimeField(null=True, verbose_name='最后登录时间')
    last_login_ip = models.CharField(max_length=50, null=True, verbose_name='最后登录IP')
    login_failed_count = models.IntegerField(default=0, verbose_name='登录失败次数')
    security_level = models.CharField(max_length=10, choices=SECURITY_LEVELS, default='MEDIUM', verbose_name='安全等级')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_security_info'
        verbose_name = verbose_name_plural = '用户安全信息'


class DataEncryptionRecord(models.Model):
    """
    数据加密记录模型
    记录数据加密和解密操作
    """
    
    ENCRYPTION_TYPES = [
        ('AES-256-CFB', 'AES-256-CFB'),
        ('SHA256', 'SHA256'),
        ('HMAC', 'HMAC'),
    ]
    
    id = models.AutoField(primary_key=True)
    data_type = models.CharField(max_length=50, verbose_name='数据类型')
    original_length = models.IntegerField(verbose_name='原始数据长度')
    encrypted_length = models.IntegerField(verbose_name='加密后长度')
    encryption_type = models.CharField(max_length=20, choices=ENCRYPTION_TYPES, verbose_name='加密类型')
    operation = models.CharField(max_length=10, choices=[('ENCRYPT', '加密'), ('DECRYPT', '解密')], verbose_name='操作类型')
    status = models.CharField(max_length=20, choices=[('SUCCESS', '成功'), ('FAILED', '失败')], verbose_name='状态')
    error_message = models.TextField(null=True, verbose_name='错误信息')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    
    class Meta:
        db_table = 'data_encryption_record'
        verbose_name = verbose_name_plural = '数据加密记录'


class RecommendationRecord(models.Model):
    """
    推荐记录模型
    记录推荐算法的执行情况
    """
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户ID')
    recommendation_list = models.TextField(verbose_name='推荐列表')
    algorithm_type = models.CharField(max_length=50, verbose_name='算法类型')
    score = models.FloatField(null=True, verbose_name='推荐分数')
    execution_time = models.FloatField(null=True, verbose_name='执行时间(ms)')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    
    class Meta:
        db_table = 'recommendation_record'
        verbose_name = verbose_name_plural = '推荐记录'


class UserBehaviorLog(models.Model):
    """
    用户行为日志模型
    记录用户的各种行为
    """
    
    BEHAVIOR_TYPES = [
        ('VIEW', '浏览'),
        ('FAVORITE', '收藏'),
        ('PURCHASE', '购买'),
        ('COMMENT', '评论'),
        ('SEARCH', '搜索'),
        ('CLICK', '点击'),
    ]
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, verbose_name='用户ID')
    username = models.CharField(max_length=255, null=True, verbose_name='用户名')
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPES, verbose_name='行为类型')
    target_type = models.CharField(max_length=50, null=True, verbose_name='目标类型')
    target_id = models.IntegerField(null=True, verbose_name='目标ID')
    target_name = models.CharField(max_length=255, null=True, verbose_name='目标名称')
    ip_address = models.CharField(max_length=50, null=True, verbose_name='IP地址')
    user_agent = models.TextField(null=True, verbose_name='用户代理')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    
    class Meta:
        db_table = 'user_behavior_log'
        verbose_name = verbose_name_plural = '用户行为日志'
        ordering = ['-created_at']


class FailedLoginAttempt(models.Model):
    """
    登录失败记录
    用于防止暴力破解
    """
    
    ip_address = models.CharField(max_length=50, verbose_name='IP地址')
    username = models.CharField(max_length=255, verbose_name='用户名')
    attempt_time = models.DateTimeField(default=datetime.now, verbose_name='尝试时间')
    lock_until = models.DateTimeField(null=True, verbose_name='锁定截止时间')
    
    class Meta:
        db_table = 'failed_login_attempts'
        verbose_name = verbose_name_plural = '登录失败记录'

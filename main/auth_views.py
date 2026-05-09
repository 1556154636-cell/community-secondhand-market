#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户认证视图模块
包含登录、注册、密码管理等安全功能
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json

from .models import yonghu
from .security_utils import PasswordSecurity, HMACAuthentication, DataEncryption
from .security_models import SecurityLog, UserSecurityInfo, FailedLoginAttempt


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """
    API接口 - 用户注册
    使用SHA256加密密码，记录安全日志
    """
    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        name = data.get('name', '')
        
        if not username or not password:
            return JsonResponse({'code': 400, 'msg': '用户名和密码不能为空'})
        
        if yonghu.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'msg': '用户名已存在'})
        
        if phone and yonghu.objects.filter(phone=phone).exists():
            return JsonResponse({'code': 400, 'msg': '手机号已被注册'})
        
        password_security = PasswordSecurity()
        
        if not password_security.check_password_strength(password):
            return JsonResponse({'code': 400, 'msg': '密码强度不足，请使用6位以上包含字母和数字的密码'})
        
        salt = password_security.generate_salt()
        hashed_password = password_security.hash_password(password, salt)
        
        encrypted_phone = None
        if phone:
            data_encryption = DataEncryption()
            encrypted_phone = data_encryption.encrypt_data(phone)
        
        user = yonghu.objects.create(
            username=username,
            password=hashed_password,
            phone=encrypted_phone if encrypted_phone else phone,
            name=name,
            addtime=datetime.now(),
            balance=0,
        )
        
        UserSecurityInfo.objects.create(
            user_id=user.id,
            username=username,
            password_salt=salt,
            last_login_time=None,
            last_login_ip=None,
            login_failed_count=0,
            security_level='MEDIUM',
        )
        
        SecurityLog.objects.create(
            action_type='REGISTER_SUCCESS',
            target_user=username,
            ip_address=request.META.get('REMOTE_ADDR'),
            status='SUCCESS',
            description=f'用户注册成功: {username}',
            log_time=datetime.now(),
        )
        
        return JsonResponse({
            'code': 0,
            'msg': '注册成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
            }
        })
    
    except Exception as e:
        SecurityLog.objects.create(
            action_type='REGISTER_FAILED',
            ip_address=request.META.get('REMOTE_ADDR'),
            status='FAILED',
            description=f'用户注册失败: {str(e)}',
            log_time=datetime.now(),
        )
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """
    API接口 - 用户登录
    密码验证、登录失败记录、安全日志记录
    """
    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'code': 400, 'msg': '用户名和密码不能为空'})
        
        ip_address = request.META.get('REMOTE_ADDR')
        
        failed_attempts = FailedLoginAttempt.objects.filter(
            ip_address=ip_address,
            lock_until__gt=datetime.now()
        ).count()
        
        if failed_attempts >= 5:
            SecurityLog.objects.create(
                action_type='ACCESS_DENIED',
                target_user=username,
                ip_address=ip_address,
                status='WARNING',
                description=f'账户已被锁定，请稍后再试',
                log_time=datetime.now(),
            )
            return JsonResponse({'code': 403, 'msg': '登录失败次数过多，请稍后再试'})
        
        user = yonghu.objects.filter(username=username).first()
        
        if not user:
            FailedLoginAttempt.objects.create(
                ip_address=ip_address,
                username=username,
                attempt_time=datetime.now(),
                lock_until=datetime.now() + timedelta(minutes=5) if failed_attempts >= 4 else None,
            )
            
            SecurityLog.objects.create(
                action_type='LOGIN_FAILED',
                target_user=username,
                ip_address=ip_address,
                status='FAILED',
                description=f'登录失败: 用户不存在',
                log_time=datetime.now(),
            )
            return JsonResponse({'code': 401, 'msg': '用户名或密码错误'})
        
        security_info = UserSecurityInfo.objects.filter(user_id=user.id).first()
        
        if security_info:
            security_info.login_failed_count += 1
            security_info.save()
        
        password_security = PasswordSecurity()
        salt = security_info.password_salt if security_info else ''
        
        if not password_security.verify_password(password, user.password, salt):
            FailedLoginAttempt.objects.create(
                ip_address=ip_address,
                username=username,
                attempt_time=datetime.now(),
                lock_until=datetime.now() + timedelta(minutes=5) if (security_info and security_info.login_failed_count >= 4) else None,
            )
            
            SecurityLog.objects.create(
                action_type='LOGIN_FAILED',
                target_user=username,
                ip_address=ip_address,
                status='FAILED',
                description=f'登录失败: 密码错误',
                log_time=datetime.now(),
            )
            return JsonResponse({'code': 401, 'msg': '用户名或密码错误'})
        
        if security_info:
            security_info.login_failed_count = 0
            security_info.last_login_time = datetime.now()
            security_info.last_login_ip = ip_address
            security_info.save()
        
        FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
        
        SecurityLog.objects.create(
            action_type='LOGIN_SUCCESS',
            target_user=username,
            ip_address=ip_address,
            status='SUCCESS',
            description=f'用户登录成功',
            log_time=datetime.now(),
        )
        
        data_encryption = DataEncryption()
        decrypted_phone = None
        if user.phone:
            try:
                decrypted_phone = data_encryption.decrypt_data(user.phone)
            except:
                decrypted_phone = user.phone
        
        return JsonResponse({
            'code': 0,
            'msg': '登录成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone': decrypted_phone,
                'balance': float(user.balance) if user.balance else 0,
                'avatar': user.avatar,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """
    API接口 - 用户登出
    记录安全日志
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        SecurityLog.objects.create(
            action_type='LOGOUT',
            target_user=username,
            ip_address=request.META.get('REMOTE_ADDR'),
            status='SUCCESS',
            description=f'用户登出: {username}',
            log_time=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '登出成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_change_password(request):
    """
    API接口 - 修改密码
    验证旧密码，使用SHA256加密新密码
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        security_info = UserSecurityInfo.objects.filter(user_id=user_id).first()
        
        if not security_info:
            return JsonResponse({'code': 500, 'msg': '安全信息不存在'})
        
        password_security = PasswordSecurity()
        
        if not password_security.verify_password(old_password, user.password, security_info.password_salt):
            SecurityLog.objects.create(
                action_type='PASSWORD_CHANGE',
                target_user=user.username,
                ip_address=request.META.get('REMOTE_ADDR'),
                status='FAILED',
                description=f'密码修改失败: 旧密码错误',
                log_time=datetime.now(),
            )
            return JsonResponse({'code': 400, 'msg': '旧密码错误'})
        
        if not password_security.check_password_strength(new_password):
            return JsonResponse({'code': 400, 'msg': '新密码强度不足，请使用6位以上包含字母和数字的密码'})
        
        new_salt = password_security.generate_salt()
        new_hashed_password = password_security.hash_password(new_password, new_salt)
        
        user.password = new_hashed_password
        user.save()
        
        security_info.password_salt = new_salt
        security_info.save()
        
        SecurityLog.objects.create(
            action_type='PASSWORD_CHANGE',
            target_user=user.username,
            ip_address=request.META.get('REMOTE_ADDR'),
            status='SUCCESS',
            description=f'密码修改成功',
            log_time=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '密码修改成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_update_user_info(request):
    """
    API接口 - 更新用户信息
    敏感数据加密存储
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('user_id')
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        if 'name' in data:
            user.name = data['name']
        
        if 'phone' in data:
            data_encryption = DataEncryption()
            user.phone = data_encryption.encrypt_data(data['phone'])
        
        if 'avatar' in data:
            user.avatar = data['avatar']
        
        if 'balance' in data:
            user.balance = data['balance']
        
        user.save()
        
        SecurityLog.objects.create(
            action_type='USER_INFO_UPDATE',
            target_user=user.username,
            ip_address=request.META.get('REMOTE_ADDR'),
            status='SUCCESS',
            description=f'用户信息更新成功',
            log_time=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_user_info(request):
    """
    API接口 - 获取用户信息
    """
    try:
        user_id = request.GET.get('user_id')
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        data_encryption = DataEncryption()
        decrypted_phone = None
        if user.phone:
            try:
                decrypted_phone = data_encryption.decrypt_data(user.phone)
            except:
                decrypted_phone = user.phone
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone': decrypted_phone,
                'balance': float(user.balance) if user.balance else 0,
                'avatar': user.avatar,
                'addtime': user.addtime.strftime('%Y-%m-%d') if user.addtime else '',
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_hmac_verify(request):
    """
    API接口 - HMAC签名验证
    验证请求数据完整性
    """
    try:
        data = json.loads(request.body)
        
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        payload = data.get('payload')
        
        hmac_auth = HMACAuthentication()
        
        is_valid = hmac_auth.verify_signature(payload, signature, timestamp)
        
        if is_valid:
            return JsonResponse({'code': 0, 'msg': '签名验证通过', 'data': {'valid': True}})
        else:
            SecurityLog.objects.create(
                action_type='SUSPICIOUS_ACTIVITY',
                ip_address=request.META.get('REMOTE_ADDR'),
                status='WARNING',
                description=f'HMAC签名验证失败',
                log_time=datetime.now(),
            )
            return JsonResponse({'code': 401, 'msg': '签名验证失败', 'data': {'valid': False}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_hmac_sign(request):
    """
    API接口 - 生成HMAC签名
    """
    try:
        data = json.loads(request.body)
        
        payload = data.get('payload')
        
        hmac_auth = HMACAuthentication()
        
        signature, timestamp = hmac_auth.generate_signature(payload)
        
        return JsonResponse({
            'code': 0,
            'msg': '签名生成成功',
            'data': {
                'signature': signature,
                'timestamp': timestamp,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_security_logs(request):
    """
    API接口 - 获取安全日志列表（管理员）
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        logs = SecurityLog.objects.all().order_by('-log_time')[(page-1)*page_size:page*page_size]
        total = SecurityLog.objects.count()
        
        log_list = []
        for log in logs:
            log_list.append({
                'id': log.id,
                'action_type': log.action_type,
                'target_user': log.target_user,
                'ip_address': log.ip_address,
                'status': log.status,
                'description': log.description,
                'log_time': log.log_time.strftime('%Y-%m-%d %H:%M:%S') if log.log_time else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': log_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_user_security_info(request):
    """
    API接口 - 获取用户安全信息（管理员）
    """
    try:
        user_id = request.GET.get('user_id')
        
        security_info = UserSecurityInfo.objects.filter(user_id=user_id).first()
        
        if not security_info:
            return JsonResponse({'code': 404, 'msg': '安全信息不存在'})
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': security_info.id,
                'user_id': security_info.user_id,
                'username': security_info.username,
                'last_login_time': security_info.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if security_info.last_login_time else '',
                'last_login_ip': security_info.last_login_ip,
                'login_failed_count': security_info.login_failed_count,
                'security_level': security_info.security_level,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_encrypt_data(request):
    """
    API接口 - 数据加密测试
    """
    try:
        data = json.loads(request.body)
        
        plain_text = data.get('data')
        
        if not plain_text:
            return JsonResponse({'code': 400, 'msg': '请提供要加密的数据'})
        
        data_encryption = DataEncryption()
        encrypted = data_encryption.encrypt_data(plain_text)
        decrypted = data_encryption.decrypt_data(encrypted)
        
        from .security_models import DataEncryptionRecord
        
        DataEncryptionRecord.objects.create(
            data_type='test',
            original_length=len(plain_text),
            encrypted_length=len(encrypted),
            encryption_type='AES-256-CFB',
            operation='ENCRYPT',
            status='SUCCESS',
            created_at=datetime.now(),
        )
        
        return JsonResponse({
            'code': 0,
            'msg': '加密成功',
            'data': {
                'original': plain_text,
                'encrypted': encrypted,
                'decrypted': decrypted,
                'verified': plain_text == decrypted,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_check_password_strength(request):
    """
    API接口 - 检查密码强度
    """
    try:
        data = json.loads(request.body)
        
        password = data.get('password')
        
        if not password:
            return JsonResponse({'code': 400, 'msg': '请提供密码'})
        
        password_security = PasswordSecurity()
        result = password_security.check_password_strength(password)
        
        return JsonResponse({
            'code': 0,
            'msg': '检查完成',
            'data': {
                'strong': result,
                'length': len(password),
                'has_letters': any(c.isalpha() for c in password),
                'has_numbers': any(c.isdigit() for c in password),
                'has_symbols': any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password),
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})

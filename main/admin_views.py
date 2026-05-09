#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
管理员视图模块
包含后台管理功能
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

from .models import users, news, yonghu, forum, system_notice


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_login(request):
    """
    API接口 - 管理员登录
    """
    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        
        admin = users.objects.filter(username=username).first()
        
        if not admin:
            return JsonResponse({'code': 401, 'msg': '用户名或密码错误'})
        
        from .security_utils import PasswordSecurity
        
        ps = PasswordSecurity()
        if not ps.verify_password(password, admin.password, 'admin_salt'):
            return JsonResponse({'code': 401, 'msg': '用户名或密码错误'})
        
        return JsonResponse({
            'code': 0,
            'msg': '登录成功',
            'data': {
                'id': admin.id,
                'username': admin.username,
                'role': admin.role,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_admin_users(request):
    """
    API接口 - 获取用户列表（管理员）
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        keyword = request.GET.get('keyword', '')
        
        users_query = yonghu.objects.all()
        
        if keyword:
            users_query = users_query.filter(
                Q(username__contains=keyword) |
                Q(name__contains=keyword) |
                Q(phone__contains=keyword)
            )
        
        total = users_query.count()
        users_list = users_query.order_by('-addtime')[(page-1)*page_size:page*page_size]
        
        result = []
        for user in users_list:
            result.append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone': user.phone,
                'balance': float(user.balance) if user.balance else 0,
                'addtime': user.addtime.strftime('%Y-%m-%d %H:%M') if user.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': result,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_add_user(request):
    """
    API接口 - 添加用户（管理员）
    """
    try:
        data = json.loads(request.body)
        
        from .security_utils import PasswordSecurity
        
        ps = PasswordSecurity()
        salt = ps.generate_salt()
        hashed_password = ps.hash_password(data.get('password', '123456'), salt)
        
        user = yonghu.objects.create(
            username=data.get('username'),
            password=hashed_password,
            name=data.get('name'),
            phone=data.get('phone'),
            balance=0,
            addtime=datetime.now(),
        )
        
        from .security_models import UserSecurityInfo
        
        UserSecurityInfo.objects.create(
            user_id=user.id,
            username=user.username,
            password_salt=salt,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        return JsonResponse({
            'code': 0,
            'msg': '添加成功',
            'data': {'id': user.id}
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_update_user(request):
    """
    API接口 - 更新用户信息（管理员）
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('id')
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'balance' in data:
            user.balance = data['balance']
        
        user.save()
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_delete_user(request):
    """
    API接口 - 删除用户（管理员）
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('id')
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        user.delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_add_news(request):
    """
    API接口 - 添加新闻（管理员）
    """
    try:
        data = json.loads(request.body)
        
        news_item = news.objects.create(
            title=data.get('title'),
            summary=data.get('summary'),
            image=data.get('image'),
            content=data.get('content'),
            addtime=datetime.now(),
        )
        
        return JsonResponse({
            'code': 0,
            'msg': '添加成功',
            'data': {'id': news_item.id}
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_update_news(request):
    """
    API接口 - 更新新闻（管理员）
    """
    try:
        data = json.loads(request.body)
        
        news_id = data.get('id')
        
        news_item = news.objects.filter(id=news_id).first()
        
        if not news_item:
            return JsonResponse({'code': 404, 'msg': '新闻不存在'})
        
        if 'title' in data:
            news_item.title = data['title']
        if 'summary' in data:
            news_item.summary = data['summary']
        if 'image' in data:
            news_item.image = data['image']
        if 'content' in data:
            news_item.content = data['content']
        
        news_item.save()
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_delete_news(request):
    """
    API接口 - 删除新闻（管理员）
    """
    try:
        data = json.loads(request.body)
        
        news_id = data.get('id')
        
        news_item = news.objects.filter(id=news_id).first()
        
        if not news_item:
            return JsonResponse({'code': 404, 'msg': '新闻不存在'})
        
        news_item.delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_admin_forums(request):
    """
    API接口 - 获取论坛帖子（管理员）
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        keyword = request.GET.get('keyword', '')
        
        forums_query = forum.objects.filter(parent_id=0)
        
        if keyword:
            forums_query = forums_query.filter(title__contains=keyword)
        
        total = forums_query.count()
        forums_list = forums_query.order_by('-addtime')[(page-1)*page_size:page*page_size]
        
        result = []
        for f in forums_list:
            reply_count = forum.objects.filter(parent_id=f.id).count()
            result.append({
                'id': f.id,
                'title': f.title,
                'username': f.username,
                'status': f.status,
                'is_top': f.is_top,
                'reply_count': reply_count,
                'addtime': f.addtime.strftime('%Y-%m-%d %H:%M') if f.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': result,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_delete_forum(request):
    """
    API接口 - 删除论坛帖子（管理员）
    """
    try:
        data = json.loads(request.body)
        
        forum_id = data.get('id')
        
        forum_obj = forum.objects.filter(id=forum_id).first()
        
        if not forum_obj:
            return JsonResponse({'code': 404, 'msg': '帖子不存在'})
        
        forum.objects.filter(Q(id=forum_id) | Q(parent_id=forum_id)).delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_set_top(request):
    """
    API接口 - 设置帖子置顶（管理员）
    """
    try:
        data = json.loads(request.body)
        
        forum_id = data.get('id')
        is_top = data.get('is_top', 0)
        
        forum_obj = forum.objects.filter(id=forum_id, parent_id=0).first()
        
        if not forum_obj:
            return JsonResponse({'code': 404, 'msg': '帖子不存在'})
        
        forum_obj.is_top = is_top
        forum_obj.top_time = datetime.now() if is_top else None
        forum_obj.save()
        
        return JsonResponse({'code': 0, 'msg': '设置成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_set_notice(request):
    """
    API接口 - 设置系统公告（管理员）
    """
    try:
        data = json.loads(request.body)
        
        content = data.get('content')
        
        system_notice.objects.all().delete()
        
        system_notice.objects.create(
            content=content,
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '设置成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_admin_stats(request):
    """
    API接口 - 获取统计数据（管理员）
    """
    try:
        from .models import ershoushangpin, orders, forum
        
        stats = {
            'user_count': yonghu.objects.count(),
            'product_count': ershoushangpin.objects.count(),
            'pending_product_count': forum.objects.filter(parent_id=0).count(),
            'order_count': orders.objects.count(),
            'forum_count': forum.objects.filter(parent_id=0).count(),
            'news_count': news.objects.count(),
        }
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': stats,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_admin_recent_activities(request):
    """
    API接口 - 获取最近活动（管理员）
    """
    try:
        from .security_models import UserBehaviorLog
        
        activities = UserBehaviorLog.objects.all().order_by('-created_at')[:20]
        
        result = []
        for activity in activities:
            result.append({
                'id': activity.id,
                'username': activity.username,
                'behavior_type': activity.behavior_type,
                'target_name': activity.target_name,
                'ip_address': activity.ip_address,
                'created_at': activity.created_at.strftime('%Y-%m-%d %H:%M:%S') if activity.created_at else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': result,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})

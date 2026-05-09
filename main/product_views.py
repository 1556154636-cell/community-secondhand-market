#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
商品管理视图模块
包含商品发布、审核、搜索等功能
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime
import json

from .models import ershoushangpin, yonghushangpin, shangpinleixing, yonghu
from .security_models import UserBehaviorLog


@csrf_exempt
@require_http_methods(["POST"])
def api_publish_product(request):
    """
    API接口 - 用户发布二手商品
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('user_id')
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        product_code = 'P' + datetime.now().strftime('%Y%m%d%H%M%S') + str(user_id)
        
        product = yonghushangpin.objects.create(
            product_code=product_code,
            product_name=data.get('product_name'),
            product_image=data.get('product_image'),
            product_type=data.get('product_type'),
            product_description=data.get('product_description'),
            price=data.get('price'),
            is_approved='待审核',
            username=user.username,
            user_name=user.name,
            publish_time=datetime.now(),
            addtime=datetime.now(),
        )
        
        UserBehaviorLog.objects.create(
            user_id=user_id,
            username=user.username,
            behavior_type='PURCHASE',
            target_type='yonghushangpin',
            target_id=product.id,
            target_name=data.get('product_name'),
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        
        return JsonResponse({
            'code': 0,
            'msg': '发布成功，等待审核',
            'data': {
                'id': product.id,
                'product_code': product_code,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_published_products(request):
    """
    API接口 - 获取用户发布的商品列表
    """
    try:
        user_id = request.GET.get('user_id')
        
        products = yonghushangpin.objects.filter(
            Q(username__in=yonghu.objects.filter(id=user_id).values('username')) |
            Q(user_id=user_id)
        ).order_by('-publish_time')
        
        product_list = []
        for p in products:
            product_list.append({
                'id': p.id,
                'product_code': p.product_code,
                'product_name': p.product_name,
                'product_image': p.product_image,
                'product_type': p.product_type,
                'price': float(p.price) if p.price else 0,
                'is_approved': p.is_approved,
                'approval_note': p.approval_note,
                'publish_time': p.publish_time.strftime('%Y-%m-%d %H:%M') if p.publish_time else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': product_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_update_product(request):
    """
    API接口 - 用户更新已发布商品
    """
    try:
        data = json.loads(request.body)
        
        product_id = data.get('id')
        
        product = yonghushangpin.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'code': 404, 'msg': '商品不存在'})
        
        if product.is_approved == '已通过':
            return JsonResponse({'code': 400, 'msg': '已通过审核的商品不能修改'})
        
        if 'product_name' in data:
            product.product_name = data['product_name']
        if 'product_image' in data:
            product.product_image = data['product_image']
        if 'product_type' in data:
            product.product_type = data['product_type']
        if 'product_description' in data:
            product.product_description = data['product_description']
        if 'price' in data:
            product.price = data['price']
        
        product.is_approved = '待审核'
        product.save()
        
        return JsonResponse({'code': 0, 'msg': '修改成功，等待重新审核'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_published_product(request):
    """
    API接口 - 用户删除已发布商品
    """
    try:
        data = json.loads(request.body)
        
        product_id = data.get('id')
        
        product = yonghushangpin.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'code': 404, 'msg': '商品不存在'})
        
        product.delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_pending_products(request):
    """
    API接口 - 获取待审核商品列表（管理员）
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        products = yonghushangpin.objects.filter(is_approved='待审核').order_by('-addtime')[(page-1)*page_size:page*page_size]
        total = yonghushangpin.objects.filter(is_approved='待审核').count()
        
        product_list = []
        for p in products:
            product_list.append({
                'id': p.id,
                'product_code': p.product_code,
                'product_name': p.product_name,
                'product_image': p.product_image,
                'product_type': p.product_type,
                'product_description': p.product_description,
                'price': float(p.price) if p.price else 0,
                'username': p.username,
                'user_name': p.user_name,
                'publish_time': p.publish_time.strftime('%Y-%m-%d %H:%M') if p.publish_time else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': product_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_approve_product(request):
    """
    API接口 - 审核商品（管理员）
    """
    try:
        data = json.loads(request.body)
        
        product_id = data.get('id')
        action = data.get('action')  # 'approve' or 'reject'
        note = data.get('note', '')
        
        product = yonghushangpin.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'code': 404, 'msg': '商品不存在'})
        
        if action == 'approve':
            product.is_approved = '已通过'
            
            # 添加到二手商品表
            ershoushangpin.objects.create(
                product_code=product.product_code,
                product_name=product.product_name,
                product_image=product.product_image,
                product_type=product.product_type,
                product_description=product.product_description,
                price=product.price,
                addtime=datetime.now(),
            )
            
        elif action == 'reject':
            product.is_approved = '已拒绝'
            product.approval_note = note
        
        product.save()
        
        return JsonResponse({
            'code': 0,
            'msg': '审核成功' if action == 'approve' else '已拒绝',
            'data': {'is_approved': product.is_approved}
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_search_products(request):
    """
    API接口 - 搜索商品
    支持关键词、分类、价格区间搜索
    """
    try:
        keyword = request.GET.get('keyword', '')
        category = request.GET.get('category', '')
        min_price = float(request.GET.get('min_price', 0))
        max_price = float(request.GET.get('max_price', float('inf')))
        sort_by = request.GET.get('sort_by', 'addtime')  # addtime, price, favorites
        sort_order = request.GET.get('sort_order', 'desc')  # asc, desc
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        
        products = ershoushangpin.objects.all()
        
        if keyword:
            products = products.filter(
                Q(product_name__contains=keyword) |
                Q(product_description__contains=keyword)
            )
        
        if category and category != 'all':
            products = products.filter(product_type=category)
        
        products = products.filter(price__gte=min_price, price__lte=max_price)
        
        if sort_by == 'price':
            products = products.order_by(f'{sort_order == "desc" and "-" or ""}price')
        elif sort_by == 'favorites':
            products = products.order_by(f'{sort_order == "desc" and "-" or ""}favorite_count')
        else:
            products = products.order_by(f'{sort_order == "desc" and "-" or ""}addtime')
        
        total = products.count()
        products = products[(page-1)*page_size:page*page_size]
        
        product_list = []
        for p in products:
            product_list.append({
                'id': p.id,
                'product_name': p.product_name,
                'price': float(p.price) if p.price else 0,
                'image': p.product_image,
                'type': p.product_type,
                'favorites': p.favorite_count or 0,
                'description': p.product_description,
                'addtime': p.addtime.strftime('%Y-%m-%d') if p.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '搜索成功',
            'data': product_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_hot_products(request):
    """
    API接口 - 获取热门商品
    """
    try:
        limit = int(request.GET.get('limit', 8))
        
        from .recommend_algorithm import HotItemsAlgorithm
        
        products = ershoushangpin.objects.all()
        items_pool = []
        
        for p in products:
            items_pool.append({
                'id': p.id,
                'product_name': p.product_name,
                'price': float(p.price) if p.price else 0,
                'product_image': p.product_image,
                'product_type': p.product_type,
                'favorite_count': p.favorite_count or 0,
                'created_time': p.addtime,
            })
        
        hot_items = HotItemsAlgorithm()
        hot_list = []
        
        for item in items_pool:
            created_timestamp = item['created_time'].timestamp() if item['created_time'] else time.time()
            score = hot_items.calculate_hot_score(
                item['favorite_count'],
                item.get('views', item['favorite_count'] * 3),
                created_timestamp
            )
            item['hot_score'] = score
            hot_list.append(item)
        
        hot_list.sort(key=lambda x: x['hot_score'], reverse=True)
        
        result = []
        for item in hot_list[:limit]:
            result.append({
                'id': item['id'],
                'name': item['product_name'],
                'price': item['price'],
                'image': item['product_image'],
                'type': item['product_type'],
                'favorites': item['favorite_count'],
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': result,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_new_products(request):
    """
    API接口 - 获取最新发布商品
    """
    try:
        limit = int(request.GET.get('limit', 8))
        
        products = ershoushangpin.objects.all().order_by('-addtime')[:limit]
        
        product_list = []
        for p in products:
            product_list.append({
                'id': p.id,
                'name': p.product_name,
                'price': float(p.price) if p.price else 0,
                'image': p.product_image,
                'type': p.product_type,
                'favorites': p.favorite_count or 0,
                'addtime': p.addtime.strftime('%Y-%m-%d %H:%M') if p.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': product_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_product_types(request):
    """
    API接口 - 获取所有商品类型
    """
    try:
        types = shangpinleixing.objects.all()
        
        type_list = []
        for t in types:
            count = ershoushangpin.objects.filter(product_type=t.category_name).count()
            type_list.append({
                'id': t.id,
                'name': t.category_name,
                'count': count,
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': type_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_product_type(request):
    """
    API接口 - 添加商品类型（管理员）
    """
    try:
        data = json.loads(request.body)
        
        category_name = data.get('category_name')
        
        if not category_name:
            return JsonResponse({'code': 400, 'msg': '类型名称不能为空'})
        
        if shangpinleixing.objects.filter(category_name=category_name).exists():
            return JsonResponse({'code': 400, 'msg': '类型已存在'})
        
        shangpinleixing.objects.create(
            category_name=category_name,
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '添加成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_product_type(request):
    """
    API接口 - 删除商品类型（管理员）
    """
    try:
        data = json.loads(request.body)
        
        type_id = data.get('id')
        
        type_obj = shangpinleixing.objects.filter(id=type_id).first()
        
        if not type_obj:
            return JsonResponse({'code': 404, 'msg': '类型不存在'})
        
        count = ershoushangpin.objects.filter(product_type=type_obj.category_name).count()
        if count > 0:
            return JsonResponse({'code': 400, 'msg': '该类型下还有商品，无法删除'})
        
        type_obj.delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_price_range(request):
    """
    API接口 - 获取商品价格范围
    """
    try:
        min_price = ershoushangpin.objects.aggregate(models.Min('price'))['price__min']
        max_price = ershoushangpin.objects.aggregate(models.Max('price'))['price__max']
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'min_price': float(min_price) if min_price else 0,
                'max_price': float(max_price) if max_price else 0,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})

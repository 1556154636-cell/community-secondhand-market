#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前台视图模块 - 动态页面渲染
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime
import json

from .models import ershoushangpin, forum, news, yonghu, cart, orders, address, storeup


def index_view(request):
    """
    首页视图 - 动态加载数据
    """
    try:
        hot_products = ershoushangpin.objects.filter(
            product_name__isnull=False
        ).exclude(
            product_name=''
        ).order_by('-favorite_count')[:8]

        recent_forums = forum.objects.filter(
            parent_id=0
        ).order_by('-addtime')[:6]

        recent_news = news.objects.all().order_by('-addtime')[:4]

        user_count = yonghu.objects.count()
        product_count = ershoushangpin.objects.count()
        forum_count = forum.objects.filter(parent_id=0).count()

        context = {
            'hot_products': hot_products,
            'recent_forums': recent_forums,
            'recent_news': recent_news,
            'user_count': user_count,
            'product_count': product_count,
            'forum_count': forum_count,
            'current_time': datetime.now(),
        }

        return render(request, 'client/index.html', context)

    except Exception as e:
        context = {
            'error': str(e),
            'hot_products': [],
            'recent_forums': [],
            'recent_news': [],
            'user_count': 0,
            'product_count': 0,
            'forum_count': 0,
        }
        return render(request, 'client/index.html', context)


@require_http_methods(["GET"])
def api_products(request):
    """
    API接口 - 获取商品列表
    """
    try:
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))

        products = ershoushangpin.objects.all()

        if category and category != 'all':
            products = products.filter(product_type=category)

        if search:
            products = products.filter(
                Q(product_name__contains=search) |
                Q(product_description__contains=search)
            )

        total = products.count()
        products = products.order_by('-addtime')[(page-1)*page_size:page*page_size]

        product_list = []
        for p in products:
            product_list.append({
                'id': p.id,
                'name': p.product_name or '未命名',
                'price': float(p.price) if p.price else 0,
                'image': p.product_image or 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=secondhand%20product%20placeholder%20icon%20simple%20clean&image_size=square',
                'type': p.product_type or '闲置',
                'favorites': p.favorite_count or 0,
                'description': p.product_description or '',
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


@require_http_methods(["GET"])
def api_recommend(request):
    """
    API接口 - 获取智能推荐商品
    基于协同过滤算法
    """
    try:
        user_id = request.GET.get('user_id', '1')
        limit = int(request.GET.get('limit', 8))
        
        from .recommend_algorithm import RecommendationEngine
        
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
                'views': (p.favorite_count or 0) * 5,
                'created_time': p.addtime,
            })
        
        engine = RecommendationEngine()
        
        sample_behaviors = [
            {'user_id': '1', 'item_id': str(items_pool[0]['id']), 'type': 'view', 'score': 0.5},
            {'user_id': '1', 'item_id': str(items_pool[2]['id']), 'type': 'favorite', 'score': 1.0},
            {'user_id': '1', 'item_id': str(items_pool[4]['id']), 'type': 'view', 'score': 0.5},
            {'user_id': '2', 'item_id': str(items_pool[0]['id']), 'type': 'purchase', 'score': 2.0},
            {'user_id': '2', 'item_id': str(items_pool[1]['id']), 'type': 'view', 'score': 0.5},
            {'user_id': '3', 'item_id': str(items_pool[2]['id']), 'type': 'favorite', 'score': 1.0},
            {'user_id': '3', 'item_id': str(items_pool[5]['id']), 'type': 'view', 'score': 0.5},
        ]
        
        engine.train(sample_behaviors)
        
        recommendations = engine.recommend(user_id, items_pool=items_pool, top_n=limit)
        
        recommend_list = []
        rec_ids = set()
        
        for item_id, score in recommendations[:int(limit*0.5)]:
            rec_ids.add(item_id)
            for p in items_pool:
                if str(p['id']) == str(item_id):
                    recommend_list.append({
                        'id': p['id'],
                        'name': p['product_name'],
                        'price': p['price'],
                        'image': p['product_image'] or 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=secondhand%20product%20placeholder%20icon%20simple%20clean&image_size=square',
                        'type': p['product_type'] or '闲置',
                        'favorites': p['favorite_count'],
                        'score': round(score, 2),
                    })
                    break
        
        for p in items_pool[:limit]:
            if str(p['id']) not in rec_ids and len(recommend_list) < limit:
                recommend_list.append({
                    'id': p['id'],
                    'name': p['product_name'],
                    'price': p['price'],
                    'image': p['product_image'] or 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=secondhand%20product%20placeholder%20icon%20simple%20clean&image_size=square',
                    'type': p['product_type'] or '闲置',
                    'favorites': p['favorite_count'],
                    'score': 0,
                })

        return JsonResponse({
            'code': 0,
            'msg': '获取推荐成功',
            'data': recommend_list
        })

    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_product_detail(request):
    """
    API接口 - 获取商品详情
    """
    try:
        product_id = request.GET.get('id')
        
        product = ershoushangpin.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'code': 404, 'msg': '商品不存在'})
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': product.id,
                'name': product.product_name or '',
                'price': float(product.price) if product.price else 0,
                'image': product.product_image or '',
                'type': product.product_type or '',
                'description': product.product_description or '',
                'favorites': product.favorite_count or 0,
                'code': product.product_code or '',
                'addtime': product.addtime.strftime('%Y-%m-%d %H:%M') if product.addtime else '',
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_forums(request):
    """
    API接口 - 获取论坛帖子列表
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        forums = forum.objects.filter(parent_id=0).order_by('-addtime')[(page-1)*page_size:page*page_size]
        total = forum.objects.filter(parent_id=0).count()

        forum_list = []
        for f in forums:
            reply_count = forum.objects.filter(parent_id=f.id).count()
            forum_list.append({
                'id': f.id,
                'title': f.title or '无标题',
                'content': f.content[:100] if f.content else '',
                'username': f.username or '匿名用户',
                'addtime': f.addtime.strftime('%Y-%m-%d %H:%M') if f.addtime else '',
                'status': f.status or '开放',
                'reply_count': reply_count,
                'is_top': f.is_top or 0,
            })

        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': forum_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        })

    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_forum_detail(request):
    """
    API接口 - 获取论坛帖子详情
    """
    try:
        forum_id = request.GET.get('id')
        
        topic = forum.objects.filter(id=forum_id).first()
        
        if not topic:
            return JsonResponse({'code': 404, 'msg': '帖子不存在'})
        
        replies = forum.objects.filter(parent_id=forum_id).order_by('addtime')
        
        reply_list = []
        for r in replies:
            reply_list.append({
                'id': r.id,
                'content': r.content,
                'username': r.username or '匿名用户',
                'addtime': r.addtime.strftime('%Y-%m-%d %H:%M') if r.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': topic.id,
                'title': topic.title,
                'content': topic.content,
                'username': topic.username,
                'addtime': topic.addtime.strftime('%Y-%m-%d %H:%M') if topic.addtime else '',
                'replies': reply_list,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_forum(request):
    """
    API接口 - 创建论坛帖子
    """
    try:
        data = json.loads(request.body)
        
        forum_obj = forum.objects.create(
            title=data.get('title'),
            content=data.get('content'),
            username=data.get('username', '匿名用户'),
            user_id=data.get('user_id', 0),
            parent_id=0,
            status='开放',
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '发布成功', 'data': {'id': forum_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_reply_forum(request):
    """
    API接口 - 回复论坛帖子
    """
    try:
        data = json.loads(request.body)
        
        forum_obj = forum.objects.create(
            content=data.get('content'),
            username=data.get('username', '匿名用户'),
            user_id=data.get('user_id', 0),
            parent_id=data.get('parent_id'),
            status='开放',
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '回复成功', 'data': {'id': forum_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_news(request):
    """
    API接口 - 获取社区资讯
    """
    try:
        news_items = news.objects.all().order_by('-addtime')[:10]

        news_list = []
        for n in news_items:
            news_list.append({
                'id': n.id,
                'title': n.title or '无标题',
                'summary': n.summary[:50] if n.summary else '',
                'image': n.image or '',
                'addtime': n.addtime.strftime('%Y-%m-%d') if n.addtime else '',
            })

        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': news_list
        })

    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_news_detail(request):
    """
    API接口 - 获取新闻详情
    """
    try:
        news_id = request.GET.get('id')
        
        news_item = news.objects.filter(id=news_id).first()
        
        if not news_item:
            return JsonResponse({'code': 404, 'msg': '新闻不存在'})
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': news_item.id,
                'title': news_item.title,
                'content': news_item.content,
                'summary': news_item.summary,
                'image': news_item.image,
                'addtime': news_item.addtime.strftime('%Y-%m-%d') if news_item.addtime else '',
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_to_cart(request):
    """
    API接口 - 添加商品到购物车
    """
    try:
        data = json.loads(request.body)
        
        cart_obj = cart.objects.create(
            user_id=data.get('user_id'),
            product_id=data.get('product_id'),
            product_name=data.get('product_name'),
            product_image=data.get('product_image'),
            unit_price=data.get('price'),
            quantity=data.get('quantity', 1),
            product_type=data.get('product_type', 'ershoushangpin'),
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '添加成功', 'data': {'id': cart_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_cart_list(request):
    """
    API接口 - 获取购物车列表
    """
    try:
        user_id = request.GET.get('user_id')
        
        cart_items = cart.objects.filter(user_id=user_id).order_by('-addtime')
        
        cart_list = []
        total_price = 0
        for item in cart_items:
            item_total = (item.unit_price or 0) * (item.quantity or 1)
            total_price += item_total
            cart_list.append({
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product_name,
                'product_image': item.product_image,
                'unit_price': float(item.unit_price) if item.unit_price else 0,
                'quantity': item.quantity or 1,
                'total_price': item_total,
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': cart_list,
            'total_price': total_price,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_update_cart(request):
    """
    API接口 - 更新购物车数量
    """
    try:
        data = json.loads(request.body)
        
        cart_obj = cart.objects.filter(id=data.get('id')).first()
        
        if not cart_obj:
            return JsonResponse({'code': 404, 'msg': '购物车项不存在'})
        
        if 'quantity' in data:
            cart_obj.quantity = data['quantity']
        if 'unit_price' in data:
            cart_obj.unit_price = data['unit_price']
        
        cart_obj.save()
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_cart(request):
    """
    API接口 - 删除购物车项
    """
    try:
        data = json.loads(request.body)
        
        cart.objects.filter(id=data.get('id')).delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_favorite(request):
    """
    API接口 - 添加收藏
    """
    try:
        data = json.loads(request.body)
        
        storeup_obj = storeup.objects.create(
            user_id=data.get('user_id'),
            ref_id=data.get('product_id'),
            table_name='ershoushangpin',
            product_name=data.get('product_name'),
            product_image=data.get('product_image'),
            collect_type='1',
            addtime=datetime.now(),
        )
        
        product = ershoushangpin.objects.filter(id=data.get('product_id')).first()
        if product:
            product.favorite_count = (product.favorite_count or 0) + 1
            product.save()
        
        return JsonResponse({'code': 0, 'msg': '收藏成功', 'data': {'id': storeup_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_favorite_list(request):
    """
    API接口 - 获取收藏列表
    """
    try:
        user_id = request.GET.get('user_id')
        
        favorites = storeup.objects.filter(user_id=user_id, collect_type='1').order_by('-addtime')
        
        favorite_list = []
        for fav in favorites:
            favorite_list.append({
                'id': fav.id,
                'product_id': fav.ref_id,
                'product_name': fav.product_name,
                'product_image': fav.product_image,
                'addtime': fav.addtime.strftime('%Y-%m-%d %H:%M') if fav.addtime else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': favorite_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_favorite(request):
    """
    API接口 - 删除收藏
    """
    try:
        data = json.loads(request.body)
        
        fav = storeup.objects.filter(id=data.get('id')).first()
        if fav:
            product_id = fav.ref_id
            fav.delete()
            
            product = ershoushangpin.objects.filter(id=product_id).first()
            if product and product.favorite_count > 0:
                product.favorite_count -= 1
                product.save()
        
        return JsonResponse({'code': 0, 'msg': '取消收藏成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_address(request):
    """
    API接口 - 添加收货地址
    """
    try:
        data = json.loads(request.body)
        
        if data.get('is_default'):
            address.objects.filter(user_id=data.get('user_id')).update(is_default=0)
        
        address_obj = address.objects.create(
            user_id=data.get('user_id'),
            receiver_name=data.get('receiver_name'),
            phone_number=data.get('phone_number'),
            full_address=data.get('full_address'),
            is_default=data.get('is_default', 0),
            addtime=datetime.now(),
        )
        
        return JsonResponse({'code': 0, 'msg': '添加成功', 'data': {'id': address_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_address_list(request):
    """
    API接口 - 获取收货地址列表
    """
    try:
        user_id = request.GET.get('user_id')
        
        addresses = address.objects.filter(user_id=user_id).order_by('-is_default', '-addtime')
        
        address_list = []
        for addr in addresses:
            address_list.append({
                'id': addr.id,
                'receiver_name': addr.receiver_name,
                'phone_number': addr.phone_number,
                'full_address': addr.full_address,
                'is_default': addr.is_default,
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': address_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_update_address(request):
    """
    API接口 - 更新收货地址
    """
    try:
        data = json.loads(request.body)
        
        addr = address.objects.filter(id=data.get('id')).first()
        
        if not addr:
            return JsonResponse({'code': 404, 'msg': '地址不存在'})
        
        if data.get('is_default'):
            address.objects.filter(user_id=addr.user_id).update(is_default=0)
        
        if 'receiver_name' in data:
            addr.receiver_name = data['receiver_name']
        if 'phone_number' in data:
            addr.phone_number = data['phone_number']
        if 'full_address' in data:
            addr.full_address = data['full_address']
        if 'is_default' in data:
            addr.is_default = data['is_default']
        
        addr.save()
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_address(request):
    """
    API接口 - 删除收货地址
    """
    try:
        data = json.loads(request.body)
        
        address.objects.filter(id=data.get('id')).delete()
        
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_order(request):
    """
    API接口 - 创建订单
    """
    try:
        data = json.loads(request.body)
        
        order_code = 'ORD' + datetime.now().strftime('%Y%m%d%H%M%S') + str(data.get('user_id'))
        
        order_obj = orders.objects.create(
            order_code=order_code,
            user_id=data.get('user_id'),
            product_id=data.get('product_id'),
            product_name=data.get('product_name'),
            product_image=data.get('product_image'),
            unit_price=data.get('unit_price'),
            quantity=data.get('quantity', 1),
            total_price=data.get('total_price'),
            shipping_address=data.get('shipping_address'),
            receiver_name=data.get('receiver_name'),
            phone=data.get('phone'),
            order_status='待付款',
            create_time=datetime.now(),
            addtime=datetime.now(),
        )
        
        cart.objects.filter(user_id=data.get('user_id'), product_id=data.get('product_id')).delete()
        
        return JsonResponse({'code': 0, 'msg': '下单成功', 'data': {'order_code': order_code, 'id': order_obj.id}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_order_list(request):
    """
    API接口 - 获取订单列表
    """
    try:
        user_id = request.GET.get('user_id')
        status = request.GET.get('status', '')
        
        orders_query = orders.objects.filter(user_id=user_id)
        
        if status:
            orders_query = orders_query.filter(order_status=status)
        
        orders_list = []
        for order in orders_query.order_by('-create_time'):
            orders_list.append({
                'id': order.id,
                'order_code': order.order_code,
                'product_name': order.product_name,
                'product_image': order.product_image,
                'unit_price': float(order.unit_price) if order.unit_price else 0,
                'quantity': order.quantity or 1,
                'total_price': float(order.total_price) if order.total_price else 0,
                'order_status': order.order_status,
                'receiver_name': order.receiver_name,
                'shipping_address': order.shipping_address,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M') if order.create_time else '',
            })
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': orders_list,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_order_detail(request):
    """
    API接口 - 获取订单详情
    """
    try:
        order_id = request.GET.get('id')
        
        order = orders.objects.filter(id=order_id).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'id': order.id,
                'order_code': order.order_code,
                'product_name': order.product_name,
                'product_image': order.product_image,
                'unit_price': float(order.unit_price) if order.unit_price else 0,
                'quantity': order.quantity or 1,
                'total_price': float(order.total_price) if order.total_price else 0,
                'order_status': order.order_status,
                'shipping_address': order.shipping_address,
                'receiver_name': order.receiver_name,
                'phone': order.phone,
                'logistics': order.logistics,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M') if order.create_time else '',
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_update_order(request):
    """
    API接口 - 更新订单状态
    """
    try:
        data = json.loads(request.body)
        
        order = orders.objects.filter(id=data.get('id')).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        if 'order_status' in data:
            order.order_status = data['order_status']
        if 'logistics' in data:
            order.logistics = data['logistics']
        
        order.save()
        
        return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_record_behavior(request):
    """
    API接口 - 记录用户行为
    """
    try:
        data = json.loads(request.body)
        
        from .security_models import UserBehaviorLog
        
        UserBehaviorLog.objects.create(
            user_id=data.get('user_id'),
            username=data.get('username'),
            behavior_type=data.get('type', 'VIEW'),
            target_type=data.get('target_type'),
            target_id=data.get('target_id'),
            target_name=data.get('target_name'),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )
        
        return JsonResponse({'code': 0, 'msg': '行为记录成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_stats(request):
    """
    API接口 - 获取统计数据
    """
    try:
        stats = {
            'user_count': yonghu.objects.count(),
            'product_count': ershoushangpin.objects.count(),
            'forum_count': forum.objects.filter(parent_id=0).count(),
            'news_count': news.objects.count(),
            'order_count': orders.objects.count(),
        }

        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': stats
        })

    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_categories(request):
    """
    API接口 - 获取商品分类
    """
    try:
        categories = [
            {'id': 'all', 'name': '全部', 'count': ershoushangpin.objects.count()},
            {'id': '数码产品', 'name': '数码产品', 'count': ershoushangpin.objects.filter(product_type='数码产品').count()},
            {'id': '家具家电', 'name': '家具家电', 'count': ershoushangpin.objects.filter(product_type='家具家电').count()},
            {'id': '服装鞋帽', 'name': '服装鞋帽', 'count': ershoushangpin.objects.filter(product_type='服装鞋帽').count()},
            {'id': '图书教材', 'name': '图书教材', 'count': ershoushangpin.objects.filter(product_type='图书教材').count()},
            {'id': '体育用品', 'name': '体育用品', 'count': ershoushangpin.objects.filter(product_type='体育用品').count()},
            {'id': '其他', 'name': '其他', 'count': ershoushangpin.objects.filter(product_type='其他').count()},
        ]
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': categories,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})

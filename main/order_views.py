#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
订单管理视图模块
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

from .models import orders, cart, yonghu


@csrf_exempt
@require_http_methods(["POST"])
def api_batch_create_order(request):
    """
    API接口 - 批量创建订单（从购物车结算）
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('user_id')
        address_id = data.get('address_id')
        cart_ids = data.get('cart_ids', [])
        
        user = yonghu.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        from .models import address
        addr = address.objects.filter(id=address_id, user_id=user_id).first()
        if not addr:
            return JsonResponse({'code': 404, 'msg': '收货地址不存在'})
        
        cart_items = cart.objects.filter(id__in=cart_ids, user_id=user_id)
        
        if not cart_items.exists():
            return JsonResponse({'code': 400, 'msg': '购物车为空'})
        
        order_codes = []
        
        for item in cart_items:
            order_code = 'ORD' + datetime.now().strftime('%Y%m%d%H%M%S') + str(user_id) + str(item.id)
            
            order = orders.objects.create(
                order_code=order_code,
                user_id=user_id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_image=item.product_image,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=float(item.unit_price) * item.quantity,
                shipping_address=addr.full_address,
                receiver_name=addr.receiver_name,
                phone=addr.phone_number,
                order_status='待付款',
                create_time=datetime.now(),
                addtime=datetime.now(),
            )
            
            order_codes.append(order_code)
            item.delete()
        
        return JsonResponse({
            'code': 0,
            'msg': '下单成功',
            'data': {
                'order_codes': order_codes,
                'count': len(order_codes),
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_pay_order(request):
    """
    API接口 - 支付订单
    """
    try:
        data = json.loads(request.body)
        
        order_id = data.get('order_id')
        
        order = orders.objects.filter(id=order_id).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        if order.order_status != '待付款':
            return JsonResponse({'code': 400, 'msg': '订单状态不正确'})
        
        user = yonghu.objects.filter(id=order.user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        total_price = float(order.total_price) if order.total_price else 0
        
        if float(user.balance) < total_price:
            return JsonResponse({'code': 400, 'msg': '余额不足'})
        
        user.balance = float(user.balance) - total_price
        user.save()
        
        order.order_status = '待发货'
        order.save()
        
        return JsonResponse({'code': 0, 'msg': '支付成功', 'data': {'balance': float(user.balance)}})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_confirm_receipt(request):
    """
    API接口 - 确认收货
    """
    try:
        data = json.loads(request.body)
        
        order_id = data.get('order_id')
        
        order = orders.objects.filter(id=order_id).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        if order.order_status != '待收货':
            return JsonResponse({'code': 400, 'msg': '订单状态不正确'})
        
        order.order_status = '已完成'
        order.save()
        
        return JsonResponse({'code': 0, 'msg': '确认收货成功'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_cancel_order(request):
    """
    API接口 - 取消订单
    """
    try:
        data = json.loads(request.body)
        
        order_id = data.get('order_id')
        
        order = orders.objects.filter(id=order_id).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        if order.order_status not in ['待付款', '待发货']:
            return JsonResponse({'code': 400, 'msg': '该状态的订单不能取消'})
        
        order.order_status = '已取消'
        order.save()
        
        if order.order_status == '待发货':
            user = yonghu.objects.filter(id=order.user_id).first()
            if user:
                user.balance = float(user.balance) + (float(order.total_price) if order.total_price else 0)
                user.save()
        
        return JsonResponse({'code': 0, 'msg': '订单已取消'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_order_status_counts(request):
    """
    API接口 - 获取订单状态统计
    """
    try:
        user_id = request.GET.get('user_id')
        
        counts = {
            'pending_payment': orders.objects.filter(user_id=user_id, order_status='待付款').count(),
            'pending_shipping': orders.objects.filter(user_id=user_id, order_status='待发货').count(),
            'pending_receipt': orders.objects.filter(user_id=user_id, order_status='待收货').count(),
            'completed': orders.objects.filter(user_id=user_id, order_status='已完成').count(),
            'cancelled': orders.objects.filter(user_id=user_id, order_status='已取消').count(),
        }
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': counts,
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_all_orders(request):
    """
    API接口 - 获取所有订单（管理员）
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        status = request.GET.get('status', '')
        
        orders_query = orders.objects.all()
        
        if status:
            orders_query = orders_query.filter(order_status=status)
        
        total = orders_query.count()
        orders_list = orders_query.order_by('-create_time')[(page-1)*page_size:page*page_size]
        
        result = []
        for order in orders_list:
            user = yonghu.objects.filter(id=order.user_id).first()
            result.append({
                'id': order.id,
                'order_code': order.order_code,
                'product_name': order.product_name,
                'total_price': float(order.total_price) if order.total_price else 0,
                'order_status': order.order_status,
                'username': user.username if user else '',
                'receiver_name': order.receiver_name,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M') if order.create_time else '',
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
def api_update_order_logistics(request):
    """
    API接口 - 更新订单物流信息（管理员）
    """
    try:
        data = json.loads(request.body)
        
        order_id = data.get('order_id')
        logistics = data.get('logistics')
        
        order = orders.objects.filter(id=order_id).first()
        
        if not order:
            return JsonResponse({'code': 404, 'msg': '订单不存在'})
        
        order.logistics = logistics
        order.order_status = '待收货'
        order.save()
        
        return JsonResponse({'code': 0, 'msg': '物流信息已更新'})
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@require_http_methods(["GET"])
def api_order_stats(request):
    """
    API接口 - 获取订单统计（管理员）
    """
    try:
        today = datetime.now().date()
        
        today_orders = orders.objects.filter(create_time__date=today).count()
        total_orders = orders.objects.count()
        completed_orders = orders.objects.filter(order_status='已完成').count()
        total_revenue = sum(float(o.total_price) for o in orders.objects.filter(order_status='已完成') if o.total_price)
        
        return JsonResponse({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'today_orders': today_orders,
                'total_orders': total_orders,
                'completed_orders': completed_orders,
                'total_revenue': total_revenue,
                'completion_rate': round(completed_orders / total_orders * 100, 2) if total_orders > 0 else 0,
            }
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_balance(request):
    """
    API接口 - 充值余额
    """
    try:
        data = json.loads(request.body)
        
        user_id = data.get('user_id')
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return JsonResponse({'code': 400, 'msg': '充值金额必须大于0'})
        
        user = yonghu.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        
        user.balance = float(user.balance) + amount
        user.save()
        
        return JsonResponse({
            'code': 0,
            'msg': '充值成功',
            'data': {'balance': float(user.balance)}
        })
    
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)})

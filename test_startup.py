#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
社区二手交易平台 - 系统测试脚本
测试各个组件是否正常工作
"""

import os
import sys
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')

def test_django_env():
    """测试Django环境"""
    try:
        import django
        django.setup()
        print("✅ Django环境配置正常")
        return True
    except Exception as e:
        print(f"❌ Django环境配置失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    try:
        from django.db import connection
        with connection.cursor():
            pass
        print("✅ 数据库连接正常")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_data_models():
    """测试数据模型"""
    try:
        from main.models import yonghu, ershoushangpin, forum
        print("✅ 数据模型导入正常")
        
        user_count = yonghu.objects.count()
        product_count = ershoushangpin.objects.count()
        forum_count = forum.objects.count()
        print(f"   用户数: {user_count}")
        print(f"   商品数: {product_count}")
        print(f"   帖子数: {forum_count}")
        return True
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

def test_security_utils():
    """测试安全工具"""
    try:
        from main.security_utils import PasswordSecurity, DataEncryption, HMACAuthentication
        
        # 测试密码哈希
        ps = PasswordSecurity()
        password = "Test@123"
        salt = ps.generate_salt()
        hashed = ps.hash_password(password, salt)
        verified = ps.verify_password(password, hashed, salt)
        assert verified, "密码验证失败"
        print("✅ 密码安全模块正常")
        
        # 测试数据加密
        de = DataEncryption()
        plain_text = "13812345678"
        encrypted = de.encrypt_data(plain_text)
        decrypted = de.decrypt_data(encrypted)
        assert plain_text == decrypted, "数据加密解密失败"
        print("✅ 数据加密模块正常")
        
        # 测试HMAC认证
        ha = HMACAuthentication()
        payload = "test_payload"
        signature, timestamp = ha.generate_signature(payload)
        verified = ha.verify_signature(payload, signature, timestamp)
        assert verified, "HMAC签名验证失败"
        print("✅ HMAC认证模块正常")
        
        return True
    except Exception as e:
        print(f"❌ 安全工具测试失败: {e}")
        return False

def test_recommendation_algorithm():
    """测试推荐算法"""
    try:
        from main.recommend_algorithm import CollaborativeFiltering, HotItemsAlgorithm, RecommendationEngine
        
        cf = CollaborativeFiltering()
        user1 = {'item1': 1, 'item2': 0.5}
        user2 = {'item1': 0.8, 'item2': 1}
        similarity = cf.cosine_similarity(user1, user2)
        assert 0 <= similarity <= 1, "余弦相似度计算异常"
        print("✅ 协同过滤算法正常")
        
        ha = HotItemsAlgorithm()
        score = ha.calculate_hot_score(100, 50, time.time() - 3600)
        assert score > 0, "热门评分计算异常"
        print("✅ 热门商品算法正常")
        
        engine = RecommendationEngine()
        behaviors = [
            {'user_id': '1', 'item_id': '1', 'type': 'view', 'score': 0.5},
            {'user_id': '1', 'item_id': '2', 'type': 'favorite', 'score': 1.0},
            {'user_id': '2', 'item_id': '1', 'type': 'view', 'score': 0.5},
        ]
        engine.train(behaviors)
        recommendations = engine.recommend('1', items_pool=[{'id': '1'}, {'id': '2'}, {'id': '3'}], top_n=2)
        assert len(recommendations) <= 2, "推荐结果数量异常"
        print("✅ 推荐引擎正常")
        
        return True
    except Exception as e:
        print(f"❌ 推荐算法测试失败: {e}")
        return False

def test_api_views():
    """测试API视图"""
    try:
        from main import front_views, auth_views
        print("✅ API视图模块导入正常")
        return True
    except Exception as e:
        print(f"❌ API视图测试失败: {e}")
        return False

def test_admin_config():
    """测试管理员配置"""
    try:
        from main.admin import YonghuAdmin, ErshouShangpinAdmin, SecurityLogAdmin
        print("✅ 管理员配置正常")
        return True
    except Exception as e:
        print(f"❌ 管理员配置测试失败: {e}")
        return False

def main():
    print("="*60)
    print("     邻里闲置 - 系统测试")
    print("         System Test Suite")
    print("="*60)
    print()
    
    results = []
    
    print("🔧 测试Django环境...")
    results.append(("Django环境", test_django_env()))
    
    print("\n🔧 测试数据库连接...")
    results.append(("数据库连接", test_database_connection()))
    
    print("\n🔧 测试数据模型...")
    results.append(("数据模型", test_data_models()))
    
    print("\n🔧 测试安全工具...")
    results.append(("安全工具", test_security_utils()))
    
    print("\n🔧 测试推荐算法...")
    results.append(("推荐算法", test_recommendation_algorithm()))
    
    print("\n🔧 测试API视图...")
    results.append(("API视图", test_api_views()))
    
    print("\n🔧 测试管理员配置...")
    results.append(("管理员配置", test_admin_config()))
    
    print("\n" + "="*60)
    print("📊 测试结果汇总:")
    print("-"*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print("-"*60)
    print(f"  总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以正常运行")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查相关模块")
        return 1

if __name__ == '__main__':
    sys.exit(main())

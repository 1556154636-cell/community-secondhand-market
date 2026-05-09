#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库字段迁移脚本
将拼音字段名改为英文字段名
"""

import pymysql
import os

def get_db_config():
    """从settings.py获取数据库配置"""
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'community_market',
        'charset': 'utf8mb4',
    }
    
    try:
        with open('dj2/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 提取数据库配置
            if "DATABASES" in content:
                import re
                
                db_config_match = re.search(r"DATABASES\s*=\s*\{.*?'default':\s*\{(.*?)\}\s*\}", content, re.DOTALL)
                if db_config_match:
                    db_config_str = db_config_match.group(1)
                    
                    host_match = re.search(r"'HOST':\s*['\"]([^'\"]+)['\"]", db_config_str)
                    user_match = re.search(r"'USER':\s*['\"]([^'\"]+)['\"]", db_config_str)
                    password_match = re.search(r"'PASSWORD':\s*['\"]([^'\"]+)['\"]", db_config_str)
                    dbname_match = re.search(r"'NAME':\s*['\"]([^'\"]+)['\"]", db_config_str)
                    
                    if host_match:
                        config['host'] = host_match.group(1)
                    if user_match:
                        config['user'] = user_match.group(1)
                    if password_match:
                        config['password'] = password_match.group(1)
                    if dbname_match:
                        config['database'] = dbname_match.group(1)
    except Exception as e:
        print(f"读取配置文件失败，使用默认配置: {e}")
    
    return config

def migrate_database():
    """执行数据库字段迁移"""
    config = get_db_config()
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        print("🔧 连接数据库成功")
        print(f"   数据库: {config['database']}")
        print(f"   主机: {config['host']}")
        
        # 迁移 ershoushangpin 表
        print("\n🔧 迁移 ershoushangpin 表...")
        
        # 重命名字段
        rename_columns = [
            ('wupinmingcheng', 'product_name'),
            ('wupintupian', 'product_image'),
            ('wupinleixing', 'product_type'),
            ('wupinjieshao', 'product_description'),
            ('shoucangshuliang', 'favorite_count'),
            ('dianjishijian', 'click_time'),
            ('wupinbianhao', 'product_code'),
        ]
        
        for old_name, new_name in rename_columns:
            try:
                cursor.execute(f"ALTER TABLE ershoushangpin CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 添加缺失字段
        add_columns = [
            ('product_code', 'VARCHAR(255) UNIQUE'),
            ('favorite_count', 'INT DEFAULT 0'),
            ('click_time', 'DATETIME'),
        ]
        
        for col_name, col_type in add_columns:
            try:
                cursor.execute(f"ALTER TABLE ershoushangpin ADD COLUMN {col_name} {col_type}")
                print(f"   ✓ 添加字段 {col_name}")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"   - {col_name} 已存在，跳过")
                else:
                    print(f"   ✗ 添加字段 {col_name} 失败: {e}")
        
        # 迁移 yonghushangpin 表
        print("\n🔧 迁移 yonghushangpin 表...")
        
        yhs_rename_columns = [
            ('wupinmingcheng', 'product_name'),
            ('wupintupian', 'product_image'),
            ('wupinleixing', 'product_type'),
            ('wupinjieshao', 'product_description'),
            ('shoucangshuliang', 'favorite_count'),
            ('wupinbianhao', 'product_code'),
            ('shifoushenhe', 'is_approved'),
            ('shenhebeizhu', 'approval_note'),
            ('fabuzhezhanghao', 'username'),
            ('fabuzhexingming', 'user_name'),
            ('fabushijian', 'publish_time'),
        ]
        
        for old_name, new_name in yhs_rename_columns:
            try:
                cursor.execute(f"ALTER TABLE yonghushangpin CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 迁移 storeup 表
        print("\n🔧 迁移 storeup 表...")
        
        storeup_rename_columns = [
            ('guanlianid', 'ref_id'),
            ('biaoming', 'table_name'),
            ('shangpinmingcheng', 'product_name'),
            ('shangpintupian', 'product_image'),
            ('shoucangleixing', 'collect_type'),
            ('tuijianleixing', 'intel_type'),
            ('beizhu', 'remark'),
            ('yonghu_id', 'user_id'),
        ]
        
        for old_name, new_name in storeup_rename_columns:
            try:
                cursor.execute(f"ALTER TABLE storeup CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 迁移 cart 表
        print("\n🔧 迁移 cart 表...")
        
        cart_rename_columns = [
            ('shangpinbiaoming', 'table_name'),
            ('shangpinid', 'product_id'),
            ('shangpinmingcheng', 'product_name'),
            ('shangpintupian', 'product_image'),
            ('goumaishuliang', 'quantity'),
            ('danjia', 'unit_price'),
            ('zhekoujia', 'discount_price'),
            ('yonghu_id', 'user_id'),
            ('shangpinleixing', 'product_type'),
        ]
        
        for old_name, new_name in cart_rename_columns:
            try:
                cursor.execute(f"ALTER TABLE cart CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 迁移 orders 表
        print("\n🔧 迁移 orders 表...")
        
        orders_rename_columns = [
            ('dingdanbianhao', 'order_code'),
            ('shangpinbiaoming', 'table_name'),
            ('shangpinid', 'product_id'),
            ('shangpinmingcheng', 'product_name'),
            ('shangpintupian', 'product_image'),
            ('goumaishuliang', 'quantity'),
            ('danjia', 'unit_price'),
            ('zhekoujia', 'discount_price'),
            ('zongjia', 'total_price'),
            ('zhekouzongjia', 'discount_total'),
            ('zhifuleixing', 'payment_type'),
            ('dingdanzhuangtai', 'order_status'),
            ('shouhuodizhi', 'shipping_address'),
            ('shouji', 'phone'),
            ('shouhuoren', 'receiver_name'),
            ('beizhu', 'remark'),
            ('wuliu', 'logistics'),
            ('yonghujuese', 'user_role'),
            ('chuangjianshijian', 'create_time'),
            ('yonghu_id', 'user_id'),
            ('shangpinleixing', 'product_type'),
        ]
        
        for old_name, new_name in orders_rename_columns:
            try:
                cursor.execute(f"ALTER TABLE orders CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 迁移 address 表
        print("\n🔧 迁移 address 表...")
        
        address_rename_columns = [
            ('xiangxidizhi', 'full_address'),
            ('shouhuoren', 'receiver_name'),
            ('lianjidianhua', 'phone_number'),
            ('shifoumoren', 'is_default'),
            ('yonghu_id', 'user_id'),
        ]
        
        for old_name, new_name in address_rename_columns:
            try:
                cursor.execute(f"ALTER TABLE address CHANGE COLUMN {old_name} {new_name} VARCHAR(255)")
                print(f"   ✓ {old_name} -> {new_name}")
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"   - {old_name} 不存在，跳过")
                else:
                    print(f"   ✗ {old_name} -> {new_name} 失败: {e}")
        
        # 迁移 shangpinleixing 表
        print("\n🔧 迁移 shangpinleixing 表...")
        
        try:
            cursor.execute("ALTER TABLE shangpinleixing CHANGE COLUMN leixingmingcheng category_name VARCHAR(255)")
            print("   ✓ leixingmingcheng -> category_name")
        except Exception as e:
            if "doesn't exist" in str(e):
                print("   - leixingmingcheng 不存在，跳过")
            else:
                print(f"   ✗ leixingmingcheng -> category_name 失败: {e}")
        
        conn.commit()
        print("\n✅ 数据库字段迁移完成！")
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
    
    return True

def main():
    print("="*60)
    print("     数据库字段迁移工具")
    print("       Field Migration Tool")
    print("="*60)
    print()
    
    print("📋 迁移说明:")
    print("   - 将拼音字段名改为英文字段名")
    print("   - 兼容已存在的字段（跳过重复）")
    print("   - 自动添加缺失的必要字段")
    print()
    
    confirm = input("是否继续执行迁移? (y/N): ").strip().lower()
    if confirm != 'y':
        print("取消迁移")
        return
    
    migrate_database()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全工具模块 - 信息安全专业特色
包含SHA256哈希、AES-256加密、HMAC认证等功能
"""

import hashlib
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hmac
from datetime import datetime


class PasswordSecurity:
    """密码安全工具"""
    
    @staticmethod
    def generate_salt(length=16):
        """生成随机盐值"""
        return os.urandom(length).hex()
    
    @staticmethod
    def hash_password(password, salt=None):
        """
        使用SHA256哈希密码
        返回: (hash_result, salt)
        """
        if salt is None:
            salt = PasswordSecurity.generate_salt()
        
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        
        hashed = hashlib.sha256(salt_bytes + password_bytes).hexdigest()
        
        return hashed, salt
    
    @staticmethod
    def verify_password(password, hashed_password, salt):
        """验证密码"""
        computed_hash, _ = PasswordSecurity.hash_password(password, salt)
        return computed_hash == hashed_password
    
    @staticmethod
    def check_password_strength(password):
        """
        检测密码强度
        返回: (strength, suggestions)
        strength: weak/medium/strong
        """
        suggestions = []
        score = 0
        
        if len(password) >= 8:
            score += 1
        else:
            suggestions.append('密码长度至少8位')
        
        if len(password) >= 12:
            score += 1
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            suggestions.append('包含至少一个大写字母')
        
        if any(c.islower() for c in password):
            score += 1
        else:
            suggestions.append('包含至少一个小写字母')
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            suggestions.append('包含至少一个数字')
        
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 1
        else:
            suggestions.append('包含至少一个特殊字符')
        
        if score >= 5:
            return 'strong', suggestions
        elif score >= 3:
            return 'medium', suggestions
        else:
            return 'weak', suggestions


class DataEncryption:
    """数据加密工具 - AES-256-CFB"""
    
    # 密钥（32字节用于AES-256）
    _SECRET_KEY = b'community_market_secret_key_for_aes_encryption!'
    
    @staticmethod
    def encrypt(data, key=None):
        """
        AES-256-CFB加密
        """
        if key is None:
            key = DataEncryption._SECRET_KEY
        
        # 确保密钥长度为32字节
        key = key[:32].ljust(32, b'\x00')
        
        # 生成随机IV
        iv = os.urandom(16)
        
        # PKCS7填充
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        data_bytes = data.encode('utf-8')
        padded_data = padder.update(data_bytes) + padder.finalize()
        
        # 加密
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # 返回IV+密文的base64编码
        return base64.b64encode(iv + encrypted_data).decode('utf-8')
    
    @staticmethod
    def decrypt(encrypted_data, key=None):
        """
        AES-256-CFB解密
        """
        if key is None:
            key = DataEncryption._SECRET_KEY
        
        key = key[:32].ljust(32, b'\x00')
        
        try:
            # 解码base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # 分离IV和密文
            iv = encrypted_bytes[:16]
            ciphertext = encrypted_bytes[16:]
            
            # 解密
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            # 去除填充
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data_bytes = unpadder.update(padded_data) + unpadder.finalize()
            
            return data_bytes.decode('utf-8')
        except Exception as e:
            return ''
    
    @staticmethod
    def encrypt_phone(phone):
        """加密手机号"""
        return DataEncryption.encrypt(phone)
    
    @staticmethod
    def decrypt_phone(encrypted_phone):
        """解密手机号"""
        return DataEncryption.decrypt(encrypted_phone)
    
    @staticmethod
    def mask_phone(phone):
        """手机号脱敏显示"""
        if len(phone) == 11:
            return phone[:3] + '****' + phone[-4:]
        return phone


class HMACAuthentication:
    """HMAC认证工具"""
    
    _SECRET_KEY = b'community_market_hmac_secret_key_for_api_authentication!'
    
    @staticmethod
    def generate_signature(data, timestamp, key=None):
        """
        生成HMAC签名
        """
        if key is None:
            key = HMACAuthentication._SECRET_KEY
        
        message = f"{timestamp}:{data}".encode('utf-8')
        signature = hmac.new(key, message, hashlib.sha256).hexdigest()
        
        return signature
    
    @staticmethod
    def verify_signature(data, timestamp, signature, key=None, max_age=300):
        """
        验证HMAC签名
        max_age: 签名有效期（秒）
        """
        if key is None:
            key = HMACAuthentication._SECRET_KEY
        
        # 检查时间戳是否过期
        try:
            sign_time = int(timestamp)
            current_time = int(datetime.now().timestamp())
            
            if abs(current_time - sign_time) > max_age:
                return False, '签名已过期'
        except:
            return False, '无效的时间戳'
        
        # 验证签名
        expected_signature = HMACAuthentication.generate_signature(data, timestamp, key)
        
        if not hmac.compare_digest(signature, expected_signature):
            return False, '签名验证失败'
        
        return True, '验证通过'


if __name__ == '__main__':
    print("=" * 60)
    print("安全工具模块测试")
    print("=" * 60)
    
    # 测试密码哈希
    print("\n【1】密码哈希测试")
    password = "Test@1234"
    hashed, salt = PasswordSecurity.hash_password(password)
    print(f"原始密码: {password}")
    print(f"哈希值: {hashed[:20]}...")
    print(f"盐值: {salt}")
    print(f"验证结果: {PasswordSecurity.verify_password(password, hashed, salt)}")
    
    # 测试密码强度
    print("\n【2】密码强度测试")
    strength, suggestions = PasswordSecurity.check_password_strength("weak")
    print(f"密码'weak'强度: {strength}")
    print(f"建议: {suggestions}")
    
    # 测试AES加密
    print("\n【3】AES加密测试")
    phone = "13812345678"
    encrypted = DataEncryption.encrypt(phone)
    decrypted = DataEncryption.decrypt(encrypted)
    print(f"原始手机号: {phone}")
    print(f"加密后: {encrypted[:30]}...")
    print(f"解密后: {decrypted}")
    print(f"脱敏显示: {DataEncryption.mask_phone(phone)}")
    
    # 测试HMAC认证
    print("\n【4】HMAC认证测试")
    data = "test_data"
    timestamp = str(int(datetime.now().timestamp()))
    signature = HMACAuthentication.generate_signature(data, timestamp)
    print(f"数据: {data}")
    print(f"时间戳: {timestamp}")
    print(f"签名: {signature[:20]}...")
    result, msg = HMACAuthentication.verify_signature(data, timestamp, signature)
    print(f"验证结果: {result}, {msg}")
    
    print("\n" + "=" * 60)
    print("所有安全工具测试完成！")
    print("=" * 60)

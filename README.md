# 邻里闲置 - 社区二手交易平台

基于 Django 框架开发的社区二手交易平台，包含信息安全功能（SHA256密码加密、AES-256数据加密、HMAC认证）和协同过滤推荐算法。

## 📁 项目结构

```
community-secondhand-market/
├── manage.py              # Django管理命令
├── requirements.txt       # 依赖配置
├── .gitignore            # Git忽略配置
├── start_server.py       # 启动脚本
├── test_startup.py       # 系统测试脚本
├── migrate_fields.py     # 数据库字段迁移脚本
├── dj2/                  # Django配置目录
│   ├── __init__.py
│   ├── settings.py       # 项目配置
│   ├── urls.py           # URL路由
│   └── wsgi.py           # WSGI配置
├── main/                 # 主应用
│   ├── __init__.py
│   ├── admin.py          # 管理员配置
│   ├── model.py          # 基础模型
│   ├── models.py         # 数据模型
│   ├── security_models.py # 安全日志模型
│   ├── security_utils.py # 安全工具
│   ├── recommend_algorithm.py # 推荐算法
│   ├── front_views.py    # 前台视图API
│   ├── auth_views.py     # 用户认证API
│   └── urls.py           # 应用路由
└── sql/                  # 数据库脚本
    └── community_market.sql
```

## 🚀 快速开始

### 环境要求

- Python 3.6+
- Django 2.2+
- MySQL 5.7+

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/1556154636-cell/community-secondhand-market.git
   cd community-secondhand-market
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置数据库**
   
   修改 `dj2/settings.py` 中的数据库配置：
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'community_market',
           'HOST': 'localhost',
           'PORT': '3306',
           'USER': 'root',
           'PASSWORD': 'your_password',
       }
   }
   ```

4. **初始化数据库**
   ```bash
   mysql -u root -p < sql/community_market.sql
   ```

5. **运行测试**
   ```bash
   python test_startup.py
   ```

6. **启动服务**
   ```bash
   python start_server.py
   ```

### 访问地址

- **前台首页**: http://localhost:5000
- **管理后台**: http://localhost:5000/admin

## 🔒 信息安全特色功能

### 1. SHA256密码哈希
- 带随机盐值的密码加密
- 密码强度检测

### 2. AES-256-CFB加密
- 敏感数据（手机号等）加密存储
- 数据加密记录追踪

### 3. HMAC认证
- API请求数据完整性验证
- 防止数据篡改

### 4. 安全审计日志
- 完整的安全操作记录
- 登录失败次数限制

## 🤖 推荐算法

### 协同过滤算法
- 基于余弦相似度的用户相似度计算
- 个性化商品推荐

### 热门商品算法
- 综合浏览量、收藏数和时间衰减因子
- 实时热门商品排序

### 混合推荐系统
- 结合协同过滤和热门推荐
- 提升推荐准确性

## 📡 API接口列表

### 用户认证
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 用户登录 |
| `/api/register` | POST | 用户注册 |
| `/api/logout` | POST | 用户登出 |
| `/api/change_password` | POST | 修改密码 |
| `/api/user_info` | GET | 获取用户信息 |

### 商品管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/products` | GET | 获取商品列表 |
| `/api/product_detail` | GET | 获取商品详情 |
| `/api/categories` | GET | 获取商品分类 |

### 推荐系统
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/recommend` | GET | 获取智能推荐 |

### 购物车
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/add_to_cart` | POST | 添加到购物车 |
| `/api/cart_list` | GET | 获取购物车列表 |
| `/api/update_cart` | POST | 更新购物车 |
| `/api/delete_cart` | POST | 删除购物车项 |

### 收藏
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/add_favorite` | POST | 添加收藏 |
| `/api/favorite_list` | GET | 获取收藏列表 |
| `/api/delete_favorite` | POST | 删除收藏 |

### 订单
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/create_order` | POST | 创建订单 |
| `/api/order_list` | GET | 获取订单列表 |
| `/api/order_detail` | GET | 获取订单详情 |

### 论坛
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/forums` | GET | 获取论坛列表 |
| `/api/forum_detail` | GET | 获取帖子详情 |
| `/api/create_forum` | POST | 创建帖子 |
| `/api/reply_forum` | POST | 回复帖子 |

### 安全API
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/hmac_sign` | POST | 生成HMAC签名 |
| `/api/hmac_verify` | POST | 验证HMAC签名 |
| `/api/encrypt_data` | POST | 数据加密测试 |
| `/api/security_logs` | GET | 获取安全日志 |

## 📊 数据库结构

### 核心数据表

| 表名 | 说明 |
|------|------|
| `yonghu` | 用户表 |
| `ershoushangpin` | 二手商品表 |
| `yonghushangpin` | 用户商品待审核表 |
| `forum` | 论坛帖子表 |
| `orders` | 订单表 |
| `cart` | 购物车表 |
| `storeup` | 收藏表 |
| `address` | 收货地址表 |
| `security_log` | 安全日志表 |
| `user_security_info` | 用户安全信息表 |

## 📝 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

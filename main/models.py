#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime


class yonghu(BaseModel):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='username'


    __authTables__={}
    __authPeople__='是'
    __loginUserColumn__='username'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='姓名',db_column='name')
    age=models.CharField ( max_length=255,null=False, unique=False, verbose_name='年龄',db_column='age')
    username=models.CharField ( max_length=255,null=False,unique=True, verbose_name='用户名',db_column='username')
    password=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码',db_column='password')
    avatar=models.TextField   (  null=True, unique=False, verbose_name='头像',db_column='avatar')
    phone=models.CharField ( max_length=255, null=True,unique=True, verbose_name='手机号',db_column='phone')
    balance=models.FloatField   (  null=True, unique=False,default='0', verbose_name='余额',db_column='balance')
    '''
    name=VARCHAR
    age=VARCHAR
    username=VARCHAR
    password=VARCHAR
    avatar=Text
    phone=VARCHAR
    balance=Float
    '''
    class Meta:
        db_table = 'yonghu'
        verbose_name = verbose_name_plural = '用户'
class yonghushangpin(BaseModel):
    __doc__ = u'''yonghushangpin'''
    __tablename__ = 'yonghushangpin'



    __authTables__={'username':'yonghu',}
    __authPeople__='否'
    __sfsh__='是'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    product_code=models.CharField ( max_length=255, null=True,unique=True, verbose_name='物品编号',db_column='product_code')
    product_name=models.CharField ( max_length=255, null=True,unique=True, verbose_name='物品名称',db_column='product_name')
    product_image=models.TextField   (  null=True, unique=False, verbose_name='物品图片',db_column='product_image')
    product_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品类型',db_column='product_type')
    product_description=models.TextField   (  null=True, unique=False, verbose_name='物品描述',db_column='product_description')
    favorite_count=models.IntegerField  (  null=True, unique=False, verbose_name='收藏数',db_column='favorite_count')
    price=models.FloatField   (  null=True, unique=False, verbose_name='价格',db_column='price')
    is_approved=models.CharField ( max_length=255, null=True, unique=False, verbose_name='是否审核',db_column='is_approved')
    approval_note=models.TextField   (  null=True, unique=False, verbose_name='审核回复',db_column='approval_note')
    username=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布者账号',db_column='username')
    user_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布者姓名',db_column='user_name')
    publish_time=models.DateTimeField  (  null=True, unique=False, verbose_name='发布时间',db_column='publish_time')
    '''
    product_code=VARCHAR
    product_name=VARCHAR
    product_image=Text
    product_type=VARCHAR
    product_description=Text
    favorite_count=Integer
    price=Float
    is_approved=VARCHAR
    approval_note=Text
    username=VARCHAR
    user_name=VARCHAR
    publish_time=DateTime
    '''
    class Meta:
        db_table = 'yonghushangpin'
        verbose_name = verbose_name_plural = '用户商品'
class config(BaseModel):
    __doc__ = u'''config'''
    __tablename__ = 'config'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='名称',db_column='name')
    value=models.TextField   (  null=True, unique=False, verbose_name='值',db_column='value')
    url=models.TextField   (  null=True, unique=False, verbose_name='链接',db_column='url')
    '''
    name=VARCHAR
    value=Text
    url=Text
    '''
    class Meta:
        db_table = 'config'
        verbose_name = verbose_name_plural = '轮播图'
class menu(BaseModel):
    __doc__ = u'''menu'''
    __tablename__ = 'menu'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    menu_json=models.TextField   ( null=False, unique=False, verbose_name='菜单',db_column='menu_json')
    '''
    menu_json=Text
    '''
    class Meta:
        db_table = 'menu'
        verbose_name = verbose_name_plural = '菜单'
class users(BaseModel):
    __doc__ = u'''users'''
    __tablename__ = 'users'



    __authTables__={}
    __authPeople__='是'
    __loginUserColumn__='username'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    username=models.CharField ( max_length=255,null=False, unique=False, verbose_name='用户名',db_column='username')
    password=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码',db_column='password')
    role=models.CharField ( max_length=255, null=True, unique=False,default='管理员', verbose_name='角色',db_column='role')
    '''
    username=VARCHAR
    password=VARCHAR
    role=VARCHAR
    '''
    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = '管理员'
class news(BaseModel):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False, verbose_name='标题',db_column='title')
    summary=models.TextField   (  null=True, unique=False, verbose_name='简介',db_column='summary')
    image=models.TextField   (  null=True, unique=False, verbose_name='图片',db_column='image')
    content=models.TextField   (  null=True, unique=False, verbose_name='内容',db_column='content')
    '''
    title=VARCHAR
    summary=Text
    image=Text
    content=Text
    '''
    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '社区资讯'
class ershoushangpin(BaseModel):
    __doc__ = u'''ershoushangpin'''
    __tablename__ = 'ershoushangpin'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='是'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    product_code=models.CharField ( max_length=255, null=True, unique=False, verbose_name='物品编号',db_column='product_code')
    product_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='物品名称',db_column='product_name')
    product_image=models.TextField   (  null=True, unique=False, verbose_name='物品图片',db_column='product_image')
    product_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品类型',db_column='product_type')
    product_description=models.TextField   (  null=True, unique=False, verbose_name='物品描述',db_column='product_description')
    favorite_count=models.IntegerField  (  null=True, unique=False, verbose_name='收藏数',db_column='favorite_count')
    click_time=models.DateTimeField  (auto_now=True,  null=True, unique=False, verbose_name='最近点击时间',db_column='click_time')
    price=models.FloatField   (  null=True, unique=False,default='0', verbose_name='价格',db_column='price')
    '''
    product_code=VARCHAR
    product_name=VARCHAR
    product_image=Text
    product_type=VARCHAR
    product_description=Text
    favorite_count=Integer
    click_time=DateTime
    price=Float
    '''
    class Meta:
        db_table = 'ershoushangpin'
        verbose_name = verbose_name_plural = '二手商品'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='是'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    ref_id=models.BigIntegerField  (  null=True, unique=False, verbose_name='关联ID',db_column='ref_id')
    table_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='表名',db_column='table_name')
    product_name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='名称',db_column='product_name')
    product_image=models.TextField   ( null=False, unique=False, verbose_name='图片',db_column='product_image')
    collect_type=models.CharField ( max_length=255, null=True, unique=False,default='1', verbose_name='类型(1:收藏,21:赞,22:踩,31:竞拍参与,41:关注)',db_column='collect_type')
    intel_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='推荐类型',db_column='intel_type')
    remark=models.CharField ( max_length=255, null=True, unique=False, verbose_name='备注',db_column='remark')
    user_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户ID',db_column='user_id')
    '''
    ref_id=BigInteger
    table_name=VARCHAR
    product_name=VARCHAR
    product_image=Text
    collect_type=VARCHAR
    intel_type=VARCHAR
    remark=VARCHAR
    user_id=BigInteger
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏'
class shangpinleixing(BaseModel):
    __doc__ = u'''shangpinleixing'''
    __tablename__ = 'shangpinleixing'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    category_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='类型名称',db_column='category_name')
    '''
    category_name=VARCHAR
    '''
    class Meta:
        db_table = 'shangpinleixing'
        verbose_name = verbose_name_plural = '商品类型'
class cart(BaseModel):
    __doc__ = u'''cart'''
    __tablename__ = 'cart'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='是'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    table_name=models.CharField ( max_length=255, null=True, unique=False,default='product', verbose_name='商品表名',db_column='table_name')
    product_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='商品ID',db_column='product_id')
    product_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品名称',db_column='product_name')
    product_image=models.TextField   ( null=False, unique=False, verbose_name='图片',db_column='product_image')
    quantity=models.IntegerField  (  null=True, unique=False, verbose_name='购买数量',db_column='quantity')
    unit_price=models.FloatField   (  null=True, unique=False, verbose_name='单价',db_column='unit_price')
    discount_price=models.FloatField   (  null=True, unique=False, verbose_name='折扣价',db_column='discount_price')
    user_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户ID',db_column='user_id')
    product_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品类型',db_column='product_type')
    '''
    table_name=VARCHAR
    product_id=BigInteger
    product_name=VARCHAR
    product_image=Text
    quantity=Integer
    unit_price=Float
    discount_price=Float
    user_id=BigInteger
    product_type=VARCHAR
    '''
    class Meta:
        db_table = 'cart'
        verbose_name = verbose_name_plural = '购物车'
class address(BaseModel):
    __doc__ = u'''address'''
    __tablename__ = 'address'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='是'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='是'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    full_address=models.CharField ( max_length=255,null=False, unique=False, verbose_name='详细地址',db_column='full_address')
    receiver_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='收货人',db_column='receiver_name')
    phone_number=models.CharField ( max_length=255, null=True, unique=False, verbose_name='联系电话',db_column='phone_number')
    is_default=models.IntegerField  (  null=True, unique=False, verbose_name='是否默认',db_column='is_default')
    user_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户ID',db_column='user_id')
    '''
    full_address=VARCHAR
    receiver_name=VARCHAR
    phone_number=VARCHAR
    is_default=Integer
    user_id=BigInteger
    '''
    class Meta:
        db_table = 'address'
        verbose_name = verbose_name_plural = '收货地址'
class orders(BaseModel):
    __doc__ = u'''orders'''
    __tablename__ = 'orders'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='是'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    order_code=models.CharField ( max_length=255,null=False,unique=True, verbose_name='订单编号',db_column='order_code')
    table_name=models.CharField ( max_length=255, null=True, unique=False,default='product', verbose_name='商品表名',db_column='table_name')
    product_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='商品ID',db_column='product_id')
    product_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品名称',db_column='product_name')
    product_image=models.TextField   ( null=False, unique=False, verbose_name='图片',db_column='product_image')
    quantity=models.IntegerField  (  null=True, unique=False, verbose_name='购买数量',db_column='quantity')
    unit_price=models.FloatField   (  null=True, unique=False, verbose_name='单价',db_column='unit_price')
    discount_price=models.FloatField   (  null=True, unique=False, verbose_name='折扣价',db_column='discount_price')
    total_price=models.FloatField   (  null=True, unique=False, verbose_name='总价',db_column='total_price')
    discount_total=models.FloatField   (  null=True, unique=False, verbose_name='折扣总价',db_column='discount_total')
    payment_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='支付类型',db_column='payment_type')
    order_status=models.CharField ( max_length=255, null=True, unique=False, verbose_name='订单状态',db_column='order_status')
    shipping_address=models.CharField ( max_length=255, null=True, unique=False, verbose_name='收货地址',db_column='shipping_address')
    phone=models.CharField ( max_length=255, null=True, unique=False, verbose_name='联系电话',db_column='phone')
    receiver_name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='收货人',db_column='receiver_name')
    remark=models.CharField ( max_length=255, null=True, unique=False, verbose_name='备注',db_column='remark')
    logistics=models.TextField   (  null=True, unique=False, verbose_name='物流',db_column='logistics')
    user_role=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户角色',db_column='user_role')
    create_time=models.DateTimeField  (  null=True, unique=False, verbose_name='创建时间',db_column='create_time')
    user_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户ID',db_column='user_id')
    product_type=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商品类型',db_column='product_type')
    '''
    order_code=VARCHAR
    table_name=VARCHAR
    product_id=BigInteger
    product_name=VARCHAR
    product_image=Text
    quantity=Integer
    unit_price=Float
    discount_price=Float
    total_price=Float
    discount_total=Float
    payment_type=VARCHAR
    order_status=VARCHAR
    shipping_address=VARCHAR
    phone=VARCHAR
    receiver_name=VARCHAR
    remark=VARCHAR
    logistics=Text
    user_role=VARCHAR
    create_time=DateTime
    user_id=BigInteger
    product_type=VARCHAR
    '''
    class Meta:
        db_table = 'orders'
        verbose_name = verbose_name_plural = '订单'
class forum(BaseModel):
    __doc__ = u'''forum'''
    __tablename__ = 'forum'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='是'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='是'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255, null=True, unique=False, verbose_name='帖子标题',db_column='title')
    content=models.TextField   ( null=False, unique=False, verbose_name='帖子内容',db_column='content')
    parent_id=models.BigIntegerField  ( null=True, unique=False, verbose_name='父节点ID',db_column='parent_id')
    user_id=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户ID',db_column='user_id')
    username=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名',db_column='username')
    avatar_url=models.TextField   (  null=True, unique=False, verbose_name='头像',db_column='avatar_url')
    status=models.CharField ( max_length=255, null=True, unique=False, verbose_name='状态',db_column='status')
    is_top=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否置顶',db_column='is_top')
    top_time=models.DateTimeField  (  null=True, unique=False, verbose_name='置顶时间',db_column='top_time')
    '''
    title=VARCHAR
    content=Text
    parent_id=BigInteger
    user_id=BigInteger
    username=VARCHAR
    avatar_url=Text
    status=VARCHAR
    is_top=Integer
    top_time=DateTime
    '''
    class Meta:
        db_table = 'forum'
        verbose_name = verbose_name_plural = '论坛交流'
class system_notice(BaseModel):
    __doc__ = u'''system_notice'''
    __tablename__ = 'systemnotice'



    __authTables__={}
    __authPeople__='否'
    __sfsh__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    content=models.TextField   (  null=True, unique=False, verbose_name='公告内容',db_column='content')
    '''
    content=Text
    '''
    class Meta:
        db_table = 'system_notice'
        verbose_name = verbose_name_plural = '系统公告'
class smsregistercode(BaseModel):
    __doc__ = u'''smsregistercode'''
    __tablename__ = 'smsregistercode'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    phone=models.CharField ( max_length=255,null=False, unique=False, verbose_name='手机号',db_column='phone')
    role=models.CharField ( max_length=255,null=False, unique=False, verbose_name='角色',db_column='role')
    verify_code=models.CharField ( max_length=255,null=False, unique=False, verbose_name='验证码',db_column='verify_code')
    '''
    phone=VARCHAR
    role=VARCHAR
    verify_code=VARCHAR
    '''
    class Meta:
        db_table = 'smsregistercode'
        verbose_name = verbose_name_plural = '短信验证码'


# 导入安全模块模型 - 信息安全专业特色功能
from .security_models import (
    SecurityLog,
    UserSecurityInfo,
    DataEncryptionRecord,
    RecommendationRecord,
    UserBehaviorLog
)

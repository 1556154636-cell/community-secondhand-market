#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邻里闲置 - 推荐算法模块
基于协同过滤的商品推荐系统
"""

import math
from collections import defaultdict
from datetime import datetime, timedelta


class CollaborativeFiltering:
    """协同过滤推荐算法"""
    
    def __init__(self):
        self.user_items = defaultdict(set)
        self.item_users = defaultdict(set)
        self.user_item_scores = defaultdict(dict)
    
    def add_user_behavior(self, user_id, item_id, score=1.0):
        """
        添加用户行为数据
        score: 行为权重（浏览=0.5, 收藏=1.0, 购买=2.0）
        """
        self.user_items[user_id].add(item_id)
        self.item_users[item_id].add(user_id)
        self.user_item_scores[user_id][item_id] = score
    
    def calculate_similarity(self, user1, user2):
        """
        计算两个用户的相似度（余弦相似度）
        """
        items1 = self.user_items[user1]
        items2 = self.user_items[user2]
        
        common_items = items1 & items2
        if not common_items:
            return 0.0
        
        numerator = sum(
            self.user_item_scores[user1].get(item, 0) * 
            self.user_item_scores[user2].get(item, 0)
            for item in common_items
        )
        
        sum1 = sum(score ** 2 for score in self.user_item_scores[user1].values())
        sum2 = sum(score ** 2 for score in self.user_item_scores[user2].values())
        
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        return numerator / denominator if denominator > 0 else 0.0
    
    def recommend_items(self, user_id, top_n=10):
        """
        为用户推荐商品
        返回: [(item_id, 推荐分数), ...]
        """
        if user_id not in self.user_items:
            return []
        
        user_similarities = []
        for other_user in self.user_items:
            if other_user != user_id:
                similarity = self.calculate_similarity(user_id, other_user)
                if similarity > 0:
                    user_similarities.append((other_user, similarity))
        
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        top_users = user_similarities[:20]
        
        item_scores = defaultdict(float)
        for other_user, similarity in top_users:
            for item_id in self.user_items[other_user]:
                if item_id not in self.user_items[user_id]:
                    item_scores[item_id] += similarity * self.user_item_scores[other_user].get(item_id, 1.0)
        
        recommended = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return recommended


class HotItemsAlgorithm:
    """热门商品排序算法"""
    
    @staticmethod
    def calculate_hot_score(item_data):
        """
        计算商品热度分数
        综合考虑：浏览量、收藏数、时间衰减
        """
        views = item_data.get('views', 0)
        favorites = item_data.get('favorites', 0)
        created_time = item_data.get('created_time', datetime.now())
        
        time_decay = HotItemsAlgorithm.time_decay_factor(created_time)
        
        score = (views * 0.3 + favorites * 0.7) * time_decay
        
        return score
    
    @staticmethod
    def time_decay_factor(created_time, decay_rate=0.95):
        """
        时间衰减因子
        商品越新，权重越高
        """
        now = datetime.now()
        days = (now - created_time).days if isinstance(created_time, datetime) else 0
        
        return decay_rate ** days
    
    @staticmethod
    def get_hot_items(items_list, top_n=10):
        """
        获取热门商品列表
        """
        items_with_score = [
            (item, HotItemsAlgorithm.calculate_hot_score(item))
            for item in items_list
        ]
        
        items_with_score.sort(key=lambda x: x[1], reverse=True)
        
        return [item for item, score in items_with_score[:top_n]]


class UserBehaviorAnalyzer:
    """用户行为分析算法"""
    
    def __init__(self):
        self.behaviors = []
    
    def add_behavior(self, user_id, item_id, behavior_type, timestamp=None):
        """
        添加用户行为
        behavior_type: view/favorite/purchase
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        self.behaviors.append({
            'user_id': user_id,
            'item_id': item_id,
            'type': behavior_type,
            'timestamp': timestamp
        })
    
    def analyze_user_interests(self, user_id):
        """
        分析用户兴趣偏好
        返回: {category: interest_score}
        """
        user_behaviors = [b for b in self.behaviors if b['user_id'] == user_id]
        
        interest_scores = defaultdict(float)
        
        for behavior in user_behaviors:
            weight = {'view': 0.5, 'favorite': 1.0, 'purchase': 2.0}.get(behavior['type'], 0.5)
            interest_scores[behavior['item_id']] += weight
        
        return dict(sorted(interest_scores.items(), key=lambda x: x[1], reverse=True))
    
    def get_user_activity_level(self, user_id):
        """
        获取用户活跃度等级
        返回: active/normal/inactive
        """
        recent_days = 30
        cutoff_time = datetime.now() - timedelta(days=recent_days)
        
        recent_behaviors = [
            b for b in self.behaviors
            if b['user_id'] == user_id and b['timestamp'] > cutoff_time
        ]
        
        activity_count = len(recent_behaviors)
        
        if activity_count >= 20:
            return 'active'
        elif activity_count >= 5:
            return 'normal'
        else:
            return 'inactive'


class RecommendationEngine:
    """推荐引擎 - 整合多种推荐算法"""
    
    def __init__(self):
        self.cf = CollaborativeFiltering()
        self.analyzer = UserBehaviorAnalyzer()
    
    def train(self, user_behaviors):
        """
        训练推荐模型
        user_behaviors: [{user_id, item_id, type, score}, ...]
        """
        for behavior in user_behaviors:
            user_id = behavior['user_id']
            item_id = behavior['item_id']
            score = behavior.get('score', 1.0)
            
            self.cf.add_user_behavior(user_id, item_id, score)
            self.analyzer.add_behavior(user_id, item_id, behavior.get('type', 'view'))
    
    def recommend(self, user_id, items_pool=None, top_n=10):
        """
        综合推荐
        结合协同过滤和热门推荐
        """
        cf_recommendations = self.cf.recommend_items(user_id, top_n=top_n)
        
        if items_pool:
            hot_items = HotItemsAlgorithm.get_hot_items(items_pool, top_n=top_n)
            
            cf_items = set(item_id for item_id, score in cf_recommendations)
            hot_items_filtered = [item for item in hot_items if item.get('id') not in cf_items]
            
            final_recommendations = cf_recommendations[:int(top_n * 0.7)]
            final_recommendations.extend([(item.get('id'), item.get('hot_score', 0)) for item in hot_items_filtered[:int(top_n * 0.3)]])
            
            return final_recommendations[:top_n]
        
        return cf_recommendations


if __name__ == '__main__':
    print("=" * 60)
    print("邻里闲置 - 推荐算法测试")
    print("=" * 60)
    
    print("\n【1】协同过滤推荐测试")
    cf = CollaborativeFiltering()
    
    behaviors = [
        ('user1', 'item1', 2.0),
        ('user1', 'item2', 1.0),
        ('user1', 'item3', 1.5),
        ('user2', 'item1', 2.0),
        ('user2', 'item2', 1.0),
        ('user2', 'item4', 1.5),
        ('user3', 'item1', 1.0),
        ('user3', 'item5', 2.0),
    ]
    
    for user_id, item_id, score in behaviors:
        cf.add_user_behavior(user_id, item_id, score)
    
    print("为user1推荐商品:")
    recommendations = cf.recommend_items('user1', top_n=5)
    for item_id, score in recommendations:
        print(f"  商品ID: {item_id}, 推荐分数: {score:.2f}")
    
    print("\n【2】热门商品算法测试")
    items = [
        {'id': 'item1', 'views': 100, 'favorites': 20, 'created_time': datetime.now() - timedelta(days=1)},
        {'id': 'item2', 'views': 200, 'favorites': 15, 'created_time': datetime.now() - timedelta(days=5)},
        {'id': 'item3', 'views': 50, 'favorites': 30, 'created_time': datetime.now()},
    ]
    
    hot_items = HotItemsAlgorithm.get_hot_items(items, top_n=3)
    print("热门商品排行:")
    for item in hot_items:
        score = HotItemsAlgorithm.calculate_hot_score(item)
        print(f"  商品ID: {item['id']}, 热度分数: {score:.2f}")
    
    print("\n【3】用户行为分析测试")
    analyzer = UserBehaviorAnalyzer()
    
    for i in range(25):
        analyzer.add_behavior('user1', f'item{i}', 'view')
    for i in range(5):
        analyzer.add_behavior('user1', f'item{i}', 'favorite')
    
    print(f"用户活跃度: {analyzer.get_user_activity_level('user1')}")
    interests = analyzer.analyze_user_interests('user1')
    print(f"用户兴趣TOP3: {list(interests.items())[:3]}")
    
    print("\n" + "=" * 60)
    print("所有推荐算法测试完成！")
    print("=" * 60)

-- 创建数据库
CREATE DATABASE IF NOT EXISTS community_market DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE community_market;

-- 用户表
CREATE TABLE IF NOT EXISTS yonghu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    avatar TEXT,
    phone VARCHAR(255) UNIQUE,
    balance FLOAT DEFAULT 0,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 二手商品表
CREATE TABLE IF NOT EXISTS ershoushangpin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(255) UNIQUE,
    product_name VARCHAR(255),
    product_image TEXT,
    product_type VARCHAR(255),
    product_description TEXT,
    favorite_count INT DEFAULT 0,
    click_time DATETIME,
    price FLOAT DEFAULT 0,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户商品表（待审核）
CREATE TABLE IF NOT EXISTS yonghushangpin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(255) UNIQUE,
    product_name VARCHAR(255),
    product_image TEXT,
    product_type VARCHAR(255),
    product_description TEXT,
    favorite_count INT DEFAULT 0,
    price FLOAT,
    is_approved VARCHAR(255) DEFAULT '待审核',
    approval_note TEXT,
    username VARCHAR(255),
    user_name VARCHAR(255),
    publish_time DATETIME,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品类型表
CREATE TABLE IF NOT EXISTS shangpinleixing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255),
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 论坛表
CREATE TABLE IF NOT EXISTS forum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT NOT NULL,
    parent_id BIGINT DEFAULT 0,
    user_id BIGINT NOT NULL,
    username VARCHAR(255),
    avatar_url TEXT,
    status VARCHAR(255) DEFAULT '开放',
    is_top INT DEFAULT 0,
    top_time DATETIME,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 新闻表
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    image TEXT,
    content TEXT,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 购物车表
CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(255) DEFAULT 'product',
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255),
    product_image TEXT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price FLOAT,
    discount_price FLOAT,
    user_id BIGINT NOT NULL,
    product_type VARCHAR(255),
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_code VARCHAR(255) NOT NULL UNIQUE,
    table_name VARCHAR(255) DEFAULT 'product',
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255),
    product_image TEXT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price FLOAT,
    discount_price FLOAT,
    total_price FLOAT,
    discount_total FLOAT,
    payment_type VARCHAR(255),
    order_status VARCHAR(255) DEFAULT '待付款',
    shipping_address VARCHAR(255),
    phone VARCHAR(255),
    receiver_name VARCHAR(255),
    remark VARCHAR(255),
    logistics TEXT,
    user_role VARCHAR(255),
    create_time DATETIME,
    user_id BIGINT NOT NULL,
    product_type VARCHAR(255),
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 收藏表
CREATE TABLE IF NOT EXISTS storeup (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ref_id BIGINT,
    table_name VARCHAR(255),
    product_name VARCHAR(255) NOT NULL,
    product_image TEXT NOT NULL,
    collect_type VARCHAR(255) DEFAULT '1',
    intel_type VARCHAR(255),
    remark VARCHAR(255),
    user_id BIGINT NOT NULL,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 收货地址表
CREATE TABLE IF NOT EXISTS address (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_address VARCHAR(255) NOT NULL,
    receiver_name VARCHAR(255),
    phone_number VARCHAR(255),
    is_default INT DEFAULT 0,
    user_id BIGINT NOT NULL,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 轮播图表
CREATE TABLE IF NOT EXISTS config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value TEXT,
    url TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 菜单表
CREATE TABLE IF NOT EXISTS menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    menu_json TEXT NOT NULL,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 管理员表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) DEFAULT '管理员',
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 系统公告表
CREATE TABLE IF NOT EXISTS system_notice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 短信验证码表
CREATE TABLE IF NOT EXISTS smsregistercode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    verify_code VARCHAR(255) NOT NULL,
    addtime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 安全日志表
CREATE TABLE IF NOT EXISTS security_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    target_user VARCHAR(255),
    ip_address VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    description TEXT,
    log_time DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户安全信息表
CREATE TABLE IF NOT EXISTS user_security_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(255) NOT NULL,
    password_salt VARCHAR(64) NOT NULL,
    last_login_time DATETIME,
    last_login_ip VARCHAR(50),
    login_failed_count INT DEFAULT 0,
    security_level VARCHAR(10) DEFAULT 'MEDIUM',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据加密记录表
CREATE TABLE IF NOT EXISTS data_encryption_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_type VARCHAR(50),
    original_length INT,
    encrypted_length INT,
    encryption_type VARCHAR(20),
    operation VARCHAR(10),
    status VARCHAR(20),
    error_message TEXT,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 推荐记录表
CREATE TABLE IF NOT EXISTS recommendation_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recommendation_list TEXT,
    algorithm_type VARCHAR(50),
    score FLOAT,
    execution_time FLOAT,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户行为日志表
CREATE TABLE IF NOT EXISTS user_behavior_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(255),
    behavior_type VARCHAR(20),
    target_type VARCHAR(50),
    target_id INT,
    target_name VARCHAR(255),
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 登录失败记录表
CREATE TABLE IF NOT EXISTS failed_login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    attempt_time DATETIME NOT NULL,
    lock_until DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入商品类型数据
INSERT INTO shangpinleixing (category_name, addtime) VALUES
('数码产品', NOW()),
('家具家电', NOW()),
('服装鞋帽', NOW()),
('图书教材', NOW()),
('体育用品', NOW()),
('其他', NOW());

-- 插入管理员账号
INSERT INTO users (username, password, role, addtime) VALUES
('admin', 'sha256$salt$hashed_password', '管理员', NOW());

-- 插入示例二手商品
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P001', 'iPhone 12 Pro 256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=iPhone%2012%20Pro%20smartphone%20product%20photo&image_size=square', '数码产品', '自用iPhone 12 Pro，成色95新，电池健康度89%，无磕碰', 23, 3500, NOW()),
('P002', '小米13 12+256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Xiaomi%2013%20smartphone%20product%20photo&image_size=square', '数码产品', '小米13旗舰手机，骁龙8 Gen2处理器，使用半年', 18, 2800, NOW()),
('P003', '实木书桌', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=wooden%20desk%20furniture%20minimalist&image_size=square', '家具家电', '1.2米实木书桌，带抽屉，搬家转让', 15, 450, NOW()),
('P004', '海尔冰箱', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Haier%20refrigerator%20white%20modern&image_size=square', '家具家电', '海尔三门冰箱，容量215L，使用3年，功能正常', 8, 600, NOW()),
('P005', 'Nike运动鞋 42码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Nike%20running%20shoes%20sport%20wear&image_size=square', '服装鞋帽', 'Nike Air Zoom跑鞋，穿过几次，几乎全新', 12, 350, NOW()),
('P006', '考研数学全套教材', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=math%20textbooks%20study%20books&image_size=square', '图书教材', '张宇考研数学一全套，含真题和练习题', 28, 80, NOW()),
('P007', '羽毛球拍套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=badminton%20racket%20sports%20equipment&image_size=square', '体育用品', '尤尼克斯羽毛球拍，含球和包', 10, 150, NOW()),
('P008', 'MacBook Air M2', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=MacBook%20Air%20laptop%20silver%20apple&image_size=square', '数码产品', 'MacBook Air M2 8+256GB，成色99新，保修期内', 35, 6800, NOW()),
('P009', '宜家书架', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=IKEA%20bookshelf%20white%20modern&image_size=square', '家具家电', '宜家BILLY书架，白色，高度2米', 14, 200, NOW()),
('P010', '羽绒服', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=down%20jacket%20winter%20coat%20blue&image_size=square', '服装鞋帽', '波司登羽绒服，L码，穿过一个冬天', 9, 300, NOW());

-- 插入示例用户
INSERT INTO yonghu (name, age, username, password, phone, balance, addtime) VALUES
('张三', '28', 'zhangsan', 'sha256$salt1$hash1', 'encrypted_phone_1', 1000, NOW()),
('李四', '25', 'lisi', 'sha256$salt2$hash2', 'encrypted_phone_2', 500, NOW()),
('王五', '30', 'wangwu', 'sha256$salt3$hash3', 'encrypted_phone_3', 2000, NOW()),
('赵六', '22', 'zhaoliu', 'sha256$salt4$hash4', 'encrypted_phone_4', 0, NOW());

-- 插入示例论坛帖子
INSERT INTO forum (title, content, parent_id, user_id, username, status, addtime) VALUES
('二手交易注意事项', '大家在进行二手交易时一定要注意以下几点：\n1. 选择安全的交易地点\n2. 仔细检查商品质量\n3. 保留交易凭证\n希望大家都能有愉快的交易体验！', 0, 1, 'zhangsan', '开放', NOW()),
('推荐一款性价比超高的笔记本', '最近入手了一款笔记本，性价比非常高，推荐给大家！配置是i5-1240P + 16GB + 512GB，价格只要4000出头，非常适合学生党。', 0, 2, 'lisi', '开放', NOW()),
('关于帖子1的回复', '同意楼主的观点，确实要注意安全！', 1, 3, 'wangwu', '开放', NOW()),
('求购：二手显示器', '求购一台27寸显示器，预算500元以内，要求成色好，无坏点。有意向的小伙伴可以私信我。', 0, 4, 'zhaoliu', '开放', NOW());

-- 插入示例新闻
INSERT INTO news (title, summary, image, content, addtime) VALUES
('社区二手交易平台新版上线', '社区二手交易平台全新版本正式上线，新增智能推荐功能！', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=community%20marketplace%20launch%20banner&image_size=square', '<h1>社区二手交易平台新版上线</h1><p>尊敬的用户，感谢您一直以来对我们平台的支持！经过团队的不懈努力，我们很高兴地宣布，社区二手交易平台全新版本正式上线！</p><h2>新增功能</h2><ul><li>智能推荐系统：根据您的浏览记录为您推荐感兴趣的商品</li><li>安全交易保障：新增交易担保功能</li><li>移动端优化：优化移动端用户体验</li></ul>', NOW()),
('春季闲置物品交易会', '本周末将举办春季闲置物品交易会，欢迎大家踊跃参与！', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=spring%20flea%20market%20community&image_size=square', '<h1>春季闲置物品交易会</h1><p>亲爱的社区居民：</p><p>为促进社区居民之间的闲置物品流转，我们将于本周六（4月15日）上午9:00-下午4:00，在社区活动中心举办春季闲置物品交易会。</p><p>欢迎大家携带家中闲置物品前来交易，让闲置物品焕发新的价值！</p>', NOW());

-- 插入示例收货地址
INSERT INTO address (full_address, receiver_name, phone_number, is_default, user_id, addtime) VALUES
('北京市朝阳区XX街道XX小区1号楼101室', '张三', 'encrypted_phone_1', 1, 1, NOW()),
('北京市海淀区XX路XX号', '李四', 'encrypted_phone_2', 1, 2, NOW()),
('北京市西城区XX胡同XX号', '王五', 'encrypted_phone_3', 0, 3, NOW());

-- 插入示例收藏记录
INSERT INTO storeup (ref_id, table_name, product_name, product_image, collect_type, user_id, addtime) VALUES
(1, 'ershoushangpin', 'iPhone 12 Pro 256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=iPhone%2012%20Pro%20smartphone&image_size=square', '1', 1, NOW()),
(8, 'ershoushangpin', 'MacBook Air M2', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=MacBook%20Air%20laptop&image_size=square', '1', 1, NOW()),
(6, 'ershoushangpin', '考研数学全套教材', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=math%20textbooks&image_size=square', '1', 2, NOW());

-- 创建索引
CREATE INDEX idx_yonghu_username ON yonghu(username);
CREATE INDEX idx_ershoushangpin_type ON ershoushangpin(product_type);
CREATE INDEX idx_forum_parent ON forum(parent_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_storeup_user ON storeup(user_id);
CREATE INDEX idx_security_log_time ON security_log(log_time);

-- 创建视图
CREATE VIEW v_user_activity AS
SELECT u.id, u.username, u.name, 
       COUNT(DISTINCT f.id) as forum_count,
       COUNT(DISTINCT o.id) as order_count,
       COUNT(DISTINCT s.id) as favorite_count
FROM yonghu u
LEFT JOIN forum f ON u.id = f.user_id
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN storeup s ON u.id = s.user_id
GROUP BY u.id, u.username, u.name;

CREATE VIEW v_hot_products AS
SELECT id, product_name, product_type, price, 
       favorite_count, addtime,
       favorite_count * 10 + (DATEDIFF(NOW(), addtime) * -1) as hot_score
FROM ershoushangpin
ORDER BY hot_score DESC;

-- 创建存储过程
DELIMITER //
CREATE PROCEDURE GetUserRecommendations(IN user_id INT, IN limit_num INT)
BEGIN
    SELECT p.id, p.product_name, p.product_image, p.price, p.product_type
    FROM ershoushangpin p
    JOIN storeup s ON p.id = s.ref_id
    WHERE s.user_id = user_id
    ORDER BY p.favorite_count DESC
    LIMIT limit_num;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE RecordUserBehavior(IN user_id INT, IN behavior_type VARCHAR(20), IN target_type VARCHAR(50), IN target_id INT, IN target_name VARCHAR(255), IN ip_address VARCHAR(50))
BEGIN
    INSERT INTO user_behavior_log (user_id, behavior_type, target_type, target_id, target_name, ip_address, created_at)
    VALUES (user_id, behavior_type, target_type, target_id, target_name, ip_address, NOW());
END //
DELIMITER ;

-- 创建触发器
DELIMITER //
CREATE TRIGGER trg_after_order_create
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE cart SET quantity = quantity - NEW.quantity 
    WHERE user_id = NEW.user_id AND product_id = NEW.product_id;
    
    DELETE FROM cart WHERE user_id = NEW.user_id AND product_id = NEW.product_id AND quantity <= 0;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_after_favorite_add
AFTER INSERT ON storeup
FOR EACH ROW
BEGIN
    UPDATE ershoushangpin 
    SET favorite_count = favorite_count + 1 
    WHERE id = NEW.ref_id AND NEW.collect_type = '1';
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_after_favorite_delete
AFTER DELETE ON storeup
FOR EACH ROW
BEGIN
    UPDATE ershoushangpin 
    SET favorite_count = favorite_count - 1 
    WHERE id = OLD.ref_id AND OLD.collect_type = '1' AND favorite_count > 0;
END //
DELIMITER ;

-- 创建事件
SET GLOBAL event_scheduler = ON;

DELIMITER //
CREATE EVENT event_clean_failed_logins
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    DELETE FROM failed_login_attempts WHERE attempt_time < NOW() - INTERVAL 1 HOUR;
END //
DELIMITER ;

DELIMITER //
CREATE EVENT event_update_hot_scores
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    UPDATE ershoushangpin 
    SET click_time = NOW() 
    WHERE id IN (SELECT id FROM v_hot_products LIMIT 10);
END //
DELIMITER ;

COMMIT;

SELECT '数据库初始化完成' AS result;

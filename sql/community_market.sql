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
('美妆护肤', NOW()),
('母婴用品', NOW()),
('其他', NOW());

-- 插入管理员账号
INSERT INTO users (username, password, role, addtime) VALUES
('admin', 'sha256$salt$hashed_password', '管理员', NOW());

-- 插入示例二手商品（数码产品）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P001', 'iPhone 12 Pro 256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=iPhone%2012%20Pro%20smartphone%20professional%20product%20photo%20white%20background&image_size=square', '数码产品', '自用iPhone 12 Pro，成色95新，电池健康度89%，无磕碰划痕，配件齐全', 23, 3500, NOW()),
('P002', '小米13 12+256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Xiaomi%2013%20smartphone%20black%20professional%20product%20photo%20studio%20lighting&image_size=square', '数码产品', '小米13旗舰手机，骁龙8 Gen2处理器，使用半年，保修期内', 18, 2800, NOW()),
('P003', 'MacBook Air M2 8+256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=MacBook%20Air%20M2%20laptop%20silver%20apple%20professional%20product%20photo&image_size=square', '数码产品', 'MacBook Air M2，成色99新，保修期到2025年，附带原装充电器', 35, 6800, NOW()),
('P004', 'iPad Pro 12.9寸 2022款', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=iPad%20Pro%2012.9%20inch%20tablet%20with%20apple%20pencil%20professional%20photo&image_size=square', '数码产品', 'iPad Pro 12.9寸 M2芯片，256GB，带Apple Pencil 2代', 28, 5500, NOW()),
('P005', 'AirPods Pro 2代', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Apple%20AirPods%20Pro%202%20wireless%20earbuds%20white%20case%20professional&image_size=square', '数码产品', 'AirPods Pro第二代，USB-C充电盒，使用3个月', 15, 1400, NOW()),
('P006', 'Sony WH-1000XM5耳机', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Sony%20WH-1000XM5%20wireless%20headphones%20black%20premium%20product&image_size=square', '数码产品', '索尼旗舰降噪耳机WH-1000XM5，黑色，带原装盒', 12, 1800, NOW()),
('P007', 'Switch OLED版', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Nintendo%20Switch%20OLED%20gaming%20console%20neon%20professional%20photo&image_size=square', '数码产品', '任天堂Switch OLED版，带3个游戏卡带', 22, 2200, NOW()),
('P008', '华为Mate 60 Pro', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Huawei%20Mate%2060%20Pro%20smartphone%20green%20professional%20product%20photo&image_size=square', '数码产品', '华为Mate 60 Pro 12+512GB，昆仑玻璃，成色95新', 38, 4800, NOW()),
('P009', '联想小新Pro16 2023', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Lenovo%20laptop%20Xiaoxin%20Pro16%20silver%20professional%20product%20photo&image_size=square', '数码产品', '联想小新Pro16，i7-13700H+RTX4060，16+1TB', 20, 5200, NOW()),
('P010', '机械键盘RGB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=RGB%20mechanical%20keyboard%20black%20gaming%20professional%20lighting&image_size=square', '数码产品', 'Cherry轴机械键盘，RGB背光，青轴手感', 8, 350, NOW()),
('P011', '罗技MX Master 3鼠标', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Logitech%20MX%20Master%203%20wireless%20mouse%20graphite%20professional&image_size=square', '数码产品', '罗技MX Master 3无线鼠标，蓝牙+优联双模式', 11, 450, NOW()),
('P012', '三星Galaxy S23 Ultra', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Samsung%20Galaxy%20S23%20Ultra%20smartphone%20purple%20professional%20photo&image_size=square', '数码产品', '三星S23 Ultra 12+256GB，成色95新，带原装壳', 25, 5200, NOW());

-- 插入示例二手商品（家具家电）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P013', '实木书桌 1.2米', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=wooden%20desk%201.2m%20minimalist%20modern%20furniture%20white%20background&image_size=square', '家具家电', '北欧风格实木书桌，带抽屉，搬家转让，成色很好', 15, 450, NOW()),
('P014', '海尔三门冰箱 215L', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Haier%20refrigerator%20three%20doors%20white%20modern%20kitchen%20appliance&image_size=square', '家具家电', '海尔三门冰箱，容量215L，使用3年，功能正常，无维修史', 8, 600, NOW()),
('P015', '宜家BILLY书架', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=white%20bookshelf%20modern%20IKEA%20style%20minimalist%20furniture&image_size=square', '家具家电', '宜家BILLY书架，白色，高度2米，五层隔板', 14, 200, NOW()),
('P016', '小米电视55寸4K', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Xiaomi%20TV%2055%20inch%204K%20smart%20television%20modern%20sleek&image_size=square', '家具家电', '小米电视55英寸4K，语音遥控，使用2年，画面清晰', 16, 1500, NOW()),
('P017', '美的空调1.5匹', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Midea%20air%20conditioner%20white%20wall%20mounted%20modern%20design&image_size=square', '家具家电', '美的变频空调1.5匹，冷暖两用，节能静音', 9, 1200, NOW()),
('P018', '折叠餐桌', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=foldable%20dining%20table%20wooden%20small%20space%20saving%20modern&image_size=square', '家具家电', '可折叠餐桌，节省空间，适合小户型，实木材质', 10, 350, NOW()),
('P019', '九阳豆浆机', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Joyoung%20soy%20milk%20machine%20white%20kitchen%20appliance%20modern&image_size=square', '家具家电', '九阳全自动豆浆机，多功能，使用半年', 7, 150, NOW()),
('P020', '布艺沙发三人位', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=fabric%20sofa%20three%20seater%20gray%20modern%20living%20room&image_size=square', '家具家电', '北欧风格布艺沙发，三人位，浅灰色，可拆洗', 13, 800, NOW()),
('P021', '单人床带床垫', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=single%20bed%20frame%20with%20mattress%20wooden%20simple%20bedroom&image_size=square', '家具家电', '1.2米单人床架+床垫，松木材质，结实耐用', 11, 500, NOW()),
('P022', '微波炉', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=microwave%20oven%20white%20compact%20kitchen%20appliance%20modern&image_size=square', '家具家电', '格兰仕微波炉，20L容量，机械旋钮操作', 6, 180, NOW()),
('P023', '落地台灯', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=floor%20lamp%20modern%20minimalist%20design%20reading%20light%20white&image_size=square', '家具家电', '简约风格落地台灯，三档调光，护眼设计', 8, 120, NOW()),
('P024', '衣柜', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=wardrobe%20closet%20white%20modern%20bedroom%20furniture%20four%20doors&image_size=square', '家具家电', '四门衣柜，白色烤漆，带镜子，内部空间大', 12, 650, NOW());

-- 插入示例二手商品（服装鞋帽）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P025', 'Nike Air Zoom跑鞋 42码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Nike%20Air%20Zoom%20running%20shoes%20black%20white%20athletic%20professional&image_size=square', '服装鞋帽', 'Nike Air Zoom跑鞋，42码，穿过几次，几乎全新', 12, 350, NOW()),
('P026', '波司登羽绒服 L码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Bosideng%20down%20jacket%20blue%20men%20winter%20fashion%20professional&image_size=square', '服装鞋帽', '波司登男士羽绒服，L码，深蓝色，穿过一个冬天', 9, 300, NOW()),
('P027', '优衣库羽绒服女款', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Uniqlo%20down%20jacket%20women%20pink%20lightweight%20fashion&image_size=square', '服装鞋帽', '优衣库女款轻薄羽绒服，M码，粉色，九成新', 10, 150, NOW()),
('P028', 'Adidas运动套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Adidas%20sportswear%20tracksuit%20black%20white%20athletic%20wear&image_size=square', '服装鞋帽', 'Adidas运动套装，上衣+裤子，XL码，黑色', 7, 200, NOW()),
('P029', '皮鞋男款43码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=men%20leather%20shoes%20black%20formal%20business%20professional&image_size=square', '服装鞋帽', '商务皮鞋，43码，黑色，真皮材质', 6, 250, NOW()),
('P030', '牛仔裤男32码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=mens%20jeans%20blue%20denim%20straight%20leg%20fashion&image_size=square', '服装鞋帽', '李维斯牛仔裤，32码，经典直筒款', 8, 180, NOW()),
('P031', '羊毛大衣男', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=wool%20coat%20men%20gray%20winter%20formal%20elegant&image_size=square', '服装鞋帽', '羊毛大衣，XXL码，灰色，保暖性好', 5, 450, NOW()),
('P032', '运动鞋女38码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=womens%20sneakers%20white%20pink%20Nike%20athletic%20fashion&image_size=square', '服装鞋帽', 'Nike女款运动鞋，38码，白粉配色', 9, 300, NOW()),
('P033', '围巾羊绒', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=cashmere%20scarf%20beige%20elegant%20winter%20accessory&image_size=square', '服装鞋帽', '纯羊绒围巾，米色，手感柔软', 11, 200, NOW()),
('P034', '棒球帽', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=baseball%20cap%20black%20streetwear%20fashion%20minimalist&image_size=square', '服装鞋帽', 'New Era棒球帽，黑色，可调节大小', 4, 120, NOW());

-- 插入示例二手商品（图书教材）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P035', '考研数学一全套', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=math%20textbooks%20postgraduate%20exam%20study%20books%20stack&image_size=square', '图书教材', '张宇考研数学一全套，含真题和练习题，有少量笔记', 28, 80, NOW()),
('P036', '英语四级真题', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=CET4%20English%20exam%20books%20study%20materials%20blue%20cover&image_size=square', '图书教材', '星火英语四级真题，2023年版，附听力音频', 15, 35, NOW()),
('P037', 'Python编程从入门到精通', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Python%20programming%20book%20yellow%20cover%20coding%20textbook&image_size=square', '图书教材', 'Python零基础入门书籍，适合初学者', 22, 45, NOW()),
('P038', '计算机网络自顶向下', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=computer%20network%20textbook%20professional%20blue%20cover&image_size=square', '图书教材', '计算机网络经典教材，第七版，英文原版', 18, 120, NOW()),
('P039', '高等数学同济七版', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=calculus%20textbook%20Chinese%20university%20math%20book&image_size=square', '图书教材', '同济大学高等数学上下册，第七版', 35, 60, NOW()),
('P040', '数据结构与算法分析', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=data%20structures%20algorithm%20book%20red%20cover%20programming&image_size=square', '图书教材', '数据结构经典教材，C语言版', 24, 55, NOW()),
('P041', '经济学原理曼昆', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=economics%20principles%20textbook%20Mankiw%20green%20cover&image_size=square', '图书教材', '曼昆经济学原理宏观+微观分册', 16, 80, NOW()),
('P042', '新概念英语全套', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=New%20Concept%20English%20books%201-4%20language%20learning&image_size=square', '图书教材', '新概念英语1-4册全套，附练习册', 20, 50, NOW()),
('P043', '现代汉语词典', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Chinese%20dictionary%20modern%20language%20reference%20book&image_size=square', '图书教材', '现代汉语词典第七版，商务印书馆', 12, 65, NOW()),
('P044', '考研英语词汇', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=English%20vocabulary%20book%20red%20cover%20exam%20preparation&image_size=square', '图书教材', '考研英语词汇红宝书，附带MP3音频', 26, 40, NOW());

-- 插入示例二手商品（体育用品）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P045', '尤尼克斯羽毛球拍', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Yonex%20badminton%20racket%20professional%20sports%20equipment&image_size=square', '体育用品', '尤尼克斯羽毛球拍NR-D11，含球和包', 10, 150, NOW()),
('P046', '篮球斯伯丁', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Spalding%20basketball%20orange%20outdoor%20sports%20professional&image_size=square', '体育用品', '斯伯丁室外篮球，7号标准球，手感好', 8, 120, NOW()),
('P047', '乒乓球拍套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=ping%20pong%20paddle%20set%20professional%20red%20black&image_size=square', '体育用品', '红双喜乒乓球拍套装，含拍套和球', 6, 80, NOW()),
('P048', '登山背包', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=hiking%20backpack%20outdoor%20camping%20green%20professional&image_size=square', '体育用品', '探路者登山背包，40L容量，防水面料', 7, 200, NOW()),
('P049', '瑜伽垫套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=yoga%20mat%20set%20purple%20fitness%20exercise%20equipment&image_size=square', '体育用品', '瑜伽垫+瑜伽球+拉力带套装，几乎全新', 9, 100, NOW()),
('P050', '运动水壶', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=sports%20water%20bottle%20stainless%20steel%20outdoor%20fitness&image_size=square', '体育用品', 'Contigo运动水壶，500ml，防漏设计', 5, 80, NOW()),
('P051', '健身手套', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=weightlifting%20gloves%20black%20fitness%20training%20professional&image_size=square', '体育用品', '健身手套，防滑耐磨，M码', 4, 50, NOW()),
('P052', '跳绳专业', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=jump%20rope%20professional%20fitness%20exercise%20black&image_size=square', '体育用品', '专业跳绳，负重款，可调节长度', 3, 30, NOW()),
('P053', '足球', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=soccer%20ball%20black%20white%20classic%20professional&image_size=square', '体育用品', '标准5号足球，黑白经典款', 6, 80, NOW()),
('P054', '游泳装备', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=swimming%20goggles%20cap%20pool%20gear%20professional&image_size=square', '体育用品', '游泳眼镜+泳帽+耳塞套装', 5, 60, NOW());

-- 插入示例二手商品（美妆护肤）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P055', 'SK-II神仙水', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=SK-II%20facial%20treatment%20essence%20bottle%20luxury%20skincare&image_size=square', '美妆护肤', 'SK-II神仙水230ml，余量80%，专柜购买', 14, 500, NOW()),
('P056', '雅诗兰黛小棕瓶', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Estee%20Lauder%20serum%20brown%20bottle%20luxury%20skincare&image_size=square', '美妆护肤', '雅诗兰黛小棕瓶精华50ml，全新未开封', 16, 450, NOW()),
('P057', '兰蔻粉水', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Lancome%20toner%20pink%20bottle%20luxury%20skincare%20cosmetics&image_size=square', '美妆护肤', '兰蔻粉水400ml，全新', 12, 280, NOW()),
('P058', '口红套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=lipstick%20set%20luxury%20cosmetics%20red%20pink%20professional&image_size=square', '美妆护肤', 'MAC口红3支套装，经典色号', 18, 400, NOW()),
('P059', '面膜礼盒', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=face%20mask%20gift%20box%20skincare%20beauty%20products&image_size=square', '美妆护肤', '韩国面膜礼盒，多种功效，共20片', 10, 150, NOW()),
('P060', '防晒霜', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=sunscreen%20cream%20bottle%20skincare%20beauty%20summer%20protection&image_size=square', '美妆护肤', '安热沙小金瓶防晒霜60ml，全新', 13, 200, NOW());

-- 插入示例二手商品（母婴用品）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P061', '婴儿推车', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=baby%20stroller%20blue%20modern%20design%20baby%20equipment&image_size=square', '母婴用品', '好孩子婴儿推车，可折叠，轻便型', 8, 300, NOW()),
('P062', '婴儿安全座椅', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=baby%20car%20seat%20black%20safety%20professional%20baby&image_size=square', '母婴用品', 'Britax婴儿安全座椅，适合0-4岁', 6, 500, NOW()),
('P063', '宝宝餐椅', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=baby%20high%20chair%20white%20adjustable%20feeding%20chair&image_size=square', '母婴用品', '宜家宝宝餐椅，可调节高度，易清洗', 7, 150, NOW()),
('P064', '儿童绘本套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=childrens%20picture%20books%20colorful%20kids%20reading&image_size=square', '母婴用品', '儿童绘本套装，20本，适合3-6岁', 11, 120, NOW()),
('P065', '玩具积木', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=building%20blocks%20colorful%20toy%20kids%20educational&image_size=square', '母婴用品', '乐高式积木，500颗粒，益智玩具', 9, 80, NOW()),
('P066', '奶瓶消毒器', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=bottle%20sterilizer%20white%20baby%20feeding%20equipment&image_size=square', '母婴用品', '飞利浦新安怡奶瓶消毒器，蒸汽消毒', 5, 200, NOW());

-- 插入示例二手商品（其他）
INSERT INTO ershoushangpin (product_code, product_name, product_image, product_type, product_description, favorite_count, price, addtime) VALUES
('P067', '行李箱24寸', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=luggage%20suitcase%2024%20inch%20blue%20travel%20hard%20case&image_size=square', '其他', '小米行李箱24寸，万向轮，轻便耐用', 12, 350, NOW()),
('P068', '充电宝20000mAh', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=power%20bank%2020000mAh%20white%20portable%20charger%20tech&image_size=square', '其他', '罗马仕充电宝20000mAh，支持快充', 15, 100, NOW()),
('P069', '雨伞', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=umbrella%20black%20automatic%20folding%20modern%20design&image_size=square', '其他', '全自动折叠雨伞，防风设计', 4, 50, NOW()),
('P070', '收纳盒套装', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=storage%20boxes%20organizer%20set%20colorful%20home%20organization&image_size=square', '其他', '收纳盒套装，多尺寸，塑料材质', 6, 30, NOW()),
('P071', '台灯护眼', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=desk%20lamp%20LED%20eye%20protection%20study%20modern%20white&image_size=square', '其他', 'LED护眼台灯，三档色温调节', 8, 80, NOW()),
('P072', '保温杯', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=thermos%20cup%20stainless%20steel%20silver%20insulated%20drinkware&image_size=square', '其他', '膳魔师保温杯，500ml，保温效果好', 7, 150, NOW());

-- 插入示例用户
INSERT INTO yonghu (name, age, username, password, phone, balance, addtime) VALUES
('张三', '28', 'zhangsan', 'sha256$salt1$hash1', 'encrypted_phone_1', 1000, NOW()),
('李四', '25', 'lisi', 'sha256$salt2$hash2', 'encrypted_phone_2', 500, NOW()),
('王五', '30', 'wangwu', 'sha256$salt3$hash3', 'encrypted_phone_3', 2000, NOW()),
('赵六', '22', 'zhaoliu', 'sha256$salt4$hash4', 'encrypted_phone_4', 0, NOW()),
('钱七', '26', 'qianqi', 'sha256$salt5$hash5', 'encrypted_phone_5', 1500, NOW()),
('孙八', '29', 'sunba', 'sha256$salt6$hash6', 'encrypted_phone_6', 800, NOW());

-- 插入示例论坛帖子
INSERT INTO forum (title, content, parent_id, user_id, username, status, addtime) VALUES
('二手交易注意事项', '大家在进行二手交易时一定要注意以下几点：\n1. 选择安全的交易地点\n2. 仔细检查商品质量\n3. 保留交易凭证\n希望大家都能有愉快的交易体验！', 0, 1, 'zhangsan', '开放', NOW()),
('推荐一款性价比超高的笔记本', '最近入手了一款笔记本，性价比非常高，推荐给大家！配置是i5-1240P + 16GB + 512GB，价格只要4000出头，非常适合学生党。', 0, 2, 'lisi', '开放', NOW()),
('关于帖子1的回复', '同意楼主的观点，确实要注意安全！', 1, 3, 'wangwu', '开放', NOW()),
('求购：二手显示器', '求购一台27寸显示器，预算500元以内，要求成色好，无坏点。有意向的小伙伴可以私信我。', 0, 4, 'zhaoliu', '开放', NOW()),
('闲置物品交换活动', '有没有小伙伴想交换闲置物品的？可以在这里留言，看看有没有合适的交换！', 0, 1, 'zhangsan', '开放', NOW()),
('笔记本选购指南', '最近想入手一台笔记本，预算5000左右，主要用于编程和学习，有没有推荐的型号？', 0, 5, 'qianqi', '开放', NOW()),
('回复：笔记本选购', '推荐联想小新Pro16，性价比很高！', 6, 2, 'lisi', '开放', NOW()),
('二手交易防骗指南', '分享一些二手交易防骗经验，希望能帮到大家！', 0, 6, 'sunba', '开放', NOW());

-- 插入示例新闻
INSERT INTO news (title, summary, image, content, addtime) VALUES
('社区二手交易平台新版上线', '社区二手交易平台全新版本正式上线，新增智能推荐功能！', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=community%20marketplace%20launch%20banner%20colorful%20modern&image_size=square', '<h1>社区二手交易平台新版上线</h1><p>尊敬的用户，感谢您一直以来对我们平台的支持！经过团队的不懈努力，我们很高兴地宣布，社区二手交易平台全新版本正式上线！</p><h2>新增功能</h2><ul><li>智能推荐系统：根据您的浏览记录为您推荐感兴趣的商品</li><li>安全交易保障：新增交易担保功能</li><li>移动端优化：优化移动端用户体验</li></ul>', NOW()),
('春季闲置物品交易会', '本周末将举办春季闲置物品交易会，欢迎大家踊跃参与！', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=spring%20flea%20market%20community%20event%20colorful&image_size=square', '<h1>春季闲置物品交易会</h1><p>亲爱的社区居民：</p><p>为促进社区居民之间的闲置物品流转，我们将于本周六（4月15日）上午9:00-下午4:00，在社区活动中心举办春季闲置物品交易会。</p><p>欢迎大家携带家中闲置物品前来交易，让闲置物品焕发新的价值！</p>', NOW()),
('安全交易指南', '平台发布安全交易指南，保障用户交易安全', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=security%20guide%20safety%20shopping%20icon%20blue%20shield&image_size=square', '<h1>安全交易指南</h1><p>为保障用户的交易安全，平台整理了以下安全交易建议：</p><ul><li>尽量选择当面交易</li><li>仔细检查商品质量</li><li>使用平台担保交易</li><li>保留聊天记录和交易凭证</li></ul>', NOW()),
('平台用户突破1000人', '热烈庆祝平台注册用户突破1000人！', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=celebration%201000%20users%20milestone%20party%20confetti&image_size=square', '<h1>平台用户突破1000人</h1><p>感谢所有用户的支持与信任！我们会继续努力，为大家提供更好的服务！</p>', NOW());

-- 插入示例收货地址
INSERT INTO address (full_address, receiver_name, phone_number, is_default, user_id, addtime) VALUES
('北京市朝阳区XX街道XX小区1号楼101室', '张三', 'encrypted_phone_1', 1, 1, NOW()),
('北京市海淀区XX路XX号', '李四', 'encrypted_phone_2', 1, 2, NOW()),
('北京市西城区XX胡同XX号', '王五', 'encrypted_phone_3', 0, 3, NOW()),
('北京市东城区XX大街XX号', '赵六', 'encrypted_phone_4', 1, 4, NOW());

-- 插入示例收藏记录
INSERT INTO storeup (ref_id, table_name, product_name, product_image, collect_type, user_id, addtime) VALUES
(1, 'ershoushangpin', 'iPhone 12 Pro 256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=iPhone%2012%20Pro%20smartphone%20professional%20product%20photo&image_size=square', '1', 1, NOW()),
(3, 'ershoushangpin', 'MacBook Air M2 8+256GB', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=MacBook%20Air%20M2%20laptop%20silver%20professional&image_size=square', '1', 1, NOW()),
(35, 'ershoushangpin', '考研数学一全套', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=math%20textbooks%20postgraduate%20exam%20books&image_size=square', '1', 2, NOW()),
(8, 'ershoushangpin', '华为Mate 60 Pro', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Huawei%20Mate%2060%20Pro%20smartphone%20green&image_size=square', '1', 3, NOW()),
(14, 'ershoushangpin', '海尔三门冰箱 215L', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Haier%20refrigerator%20white%20modern&image_size=square', '1', 3, NOW()),
(25, 'ershoushangpin', 'Nike Air Zoom跑鞋 42码', 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Nike%20running%20shoes%20black%20white%20athletic&image_size=square', '1', 4, NOW());

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

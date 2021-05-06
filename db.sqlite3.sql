BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "main_loaisanpham" (
	"id"	integer NOT NULL,
	"MaLoai"	varchar(30) NOT NULL,
	"TenLoai"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "main_sanpham" (
	"id"	integer NOT NULL,
	"MaSP"	varchar(30) NOT NULL,
	"TenSP"	varchar(100) NOT NULL,
	"MoTa"	text NOT NULL,
	"MaLoai_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("MaLoai_id") REFERENCES "main_loaisanpham"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "main_url" (
	"id"	integer NOT NULL,
	"Url"	varchar(200) NOT NULL,
	"Gia"	real NOT NULL,
	"GiaCu"	real NOT NULL,
	"MaSP_id"	integer NOT NULL,
	"Domain"	varchar(200),
	"UrlImage"	varchar(200),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("MaSP_id") REFERENCES "main_sanpham"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2021-05-02 16:23:09.922130');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2021-05-02 16:23:09.970090');
INSERT INTO "django_migrations" VALUES (3,'admin','0001_initial','2021-05-02 16:23:10.013069');
INSERT INTO "django_migrations" VALUES (4,'admin','0002_logentry_remove_auto_add','2021-05-02 16:23:10.085025');
INSERT INTO "django_migrations" VALUES (5,'admin','0003_logentry_add_action_flag_choices','2021-05-02 16:23:10.111008');
INSERT INTO "django_migrations" VALUES (6,'contenttypes','0002_remove_content_type_name','2021-05-02 16:23:10.155043');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2021-05-02 16:23:10.206999');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2021-05-02 16:23:10.276956');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2021-05-02 16:23:10.333955');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2021-05-02 16:23:10.402885');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2021-05-02 16:23:10.413878');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2021-05-02 16:23:10.443874');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2021-05-02 16:23:10.513821');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2021-05-02 16:23:10.547807');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2021-05-02 16:23:10.592746');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2021-05-02 16:23:10.610739');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2021-05-02 16:23:10.652712');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2021-05-02 16:23:10.708679');
INSERT INTO "django_migrations" VALUES (19,'main','0001_initial','2021-05-03 08:49:56.727815');
INSERT INTO "django_migrations" VALUES (20,'main','0002_auto_20210503_1615','2021-05-03 09:15:37.136773');
INSERT INTO "django_migrations" VALUES (21,'main','0003_auto_20210503_1650','2021-05-03 09:50:47.655454');
INSERT INTO "django_migrations" VALUES (22,'main','0004_auto_20210504_1151','2021-05-04 04:51:20.149302');
INSERT INTO "django_admin_log" VALUES (1,'2021-05-03 09:22:01.625778','1','LoaiSanPham object (1)','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (2,'2021-05-03 09:22:13.529131','2','LoaiSanPham object (2)','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (3,'2021-05-03 09:49:16.475899','1','SanPham object (1)','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (4,'2021-05-03 09:51:28.648082','1','Url object (1)','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (5,'2021-05-04 03:17:53.106287','2','Samsung 1','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (6,'2021-05-04 03:18:48.451972','2','https://vaunshop.com','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (7,'2021-05-04 06:24:37.698480','3','http://ngoaithat.com/','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (8,'2021-05-04 14:53:38.291617','3','iPhone 12 Pro Max','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (9,'2021-05-04 14:54:09.076454','4','https://cellphones.com.vn/iphone-12-pro-max.html','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (10,'2021-05-04 14:55:40.535196','5','https://fptshop.com.vn/dien-thoai/iphone-12-pro-max?dung-luong=128gb','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (11,'2021-05-04 14:58:04.331159','6','https://viettelstore.vn/dien-thoai/iphone-12-pro-max-128gb-pid159099.html','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (12,'2021-05-04 14:59:57.089463','7','https://www.nguyenkim.com/dien-thoai-iphone-12-pro-128gb-bac.html','[{"added": {}}]',8,1,1);
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_content_type" VALUES (7,'main','nguonban');
INSERT INTO "django_content_type" VALUES (8,'main','url');
INSERT INTO "django_content_type" VALUES (9,'main','sanpham');
INSERT INTO "django_content_type" VALUES (10,'main','loaisanpham');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_nguonban','Can add nguon ban');
INSERT INTO "auth_permission" VALUES (26,7,'change_nguonban','Can change nguon ban');
INSERT INTO "auth_permission" VALUES (27,7,'delete_nguonban','Can delete nguon ban');
INSERT INTO "auth_permission" VALUES (28,7,'view_nguonban','Can view nguon ban');
INSERT INTO "auth_permission" VALUES (29,8,'add_url','Can add url');
INSERT INTO "auth_permission" VALUES (30,8,'change_url','Can change url');
INSERT INTO "auth_permission" VALUES (31,8,'delete_url','Can delete url');
INSERT INTO "auth_permission" VALUES (32,8,'view_url','Can view url');
INSERT INTO "auth_permission" VALUES (33,9,'add_sanpham','Can add san pham');
INSERT INTO "auth_permission" VALUES (34,9,'change_sanpham','Can change san pham');
INSERT INTO "auth_permission" VALUES (35,9,'delete_sanpham','Can delete san pham');
INSERT INTO "auth_permission" VALUES (36,9,'view_sanpham','Can view san pham');
INSERT INTO "auth_permission" VALUES (37,10,'add_loaisanpham','Can add loai san pham');
INSERT INTO "auth_permission" VALUES (38,10,'change_loaisanpham','Can change loai san pham');
INSERT INTO "auth_permission" VALUES (39,10,'delete_loaisanpham','Can delete loai san pham');
INSERT INTO "auth_permission" VALUES (40,10,'view_loaisanpham','Can view loai san pham');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$216000$ojqcu0Dtgo8R$yjViotxea8IYowuKX9GOkNnd/zdT7Kz52LViIxfcW6M=','2021-05-04 14:30:05.042922',1,'admin','','admin@gmal.com',1,1,'2021-05-03 08:53:27.130663','');
INSERT INTO "django_session" VALUES ('i11depndh4b6w0ayqiarhpzpb8vn97tg','.eJxVjDsOwjAQBe_iGln-xD9Kes5g7XptHEC2FCcV4u4QKQW0b2bei0XY1hq3kZc4EzszyU6_G0J65LYDukO7dZ56W5cZ-a7wgw5-7ZSfl8P9O6gw6rcGUxRYJ5SUZI02aCZnbSAFZJL3TqMMBRFJeExaJDv5kJ3KVopCmhJ7fwDQUDfQ:1ldUKv:Wz89fs4qiud3Gzh-eisrmVY8wbMp054c8mdfvjkStYU','2021-05-17 08:53:53.773904');
INSERT INTO "django_session" VALUES ('78lr83cdvpaqzdgwoglgx4i4102yrozi','.eJxVjDsOwjAQBe_iGln-xD9Kes5g7XptHEC2FCcV4u4QKQW0b2bei0XY1hq3kZc4EzszyU6_G0J65LYDukO7dZ56W5cZ-a7wgw5-7ZSfl8P9O6gw6rcGUxRYJ5SUZI02aCZnbSAFZJL3TqMMBRFJeExaJDv5kJ3KVopCmhJ7fwDQUDfQ:1ldw3p:WtmEHvhgVkyyU4MCPZt280dGfeaf7-LFY76kkYkCa2Q','2021-05-18 14:30:05.063910');
INSERT INTO "main_loaisanpham" VALUES (1,'MT','Máy tính');
INSERT INTO "main_loaisanpham" VALUES (2,'DT','Điện thoại');
INSERT INTO "main_sanpham" VALUES (1,'i11','Iphone11','aaaaaaaaa',2);
INSERT INTO "main_sanpham" VALUES (2,'ss1','Samsung 1','SÚA Á AS Á SAM',2);
INSERT INTO "main_sanpham" VALUES (3,'iPhone 12 Pro Max','iPhone 12 Pro Max','aaaaaaa',2);
INSERT INTO "main_url" VALUES (1,'http://ngoaithatdainam.com/',3.0,6.0,1,'http://ngoaithatdainam.com/','165555732_2548145618823141_1040350366336330740_n.jpg');
INSERT INTO "main_url" VALUES (2,'https://vaunshop.com',5442.0,2424.0,2,'https://vaunshop.com','Screenshot_2021-05-04_084627.png');
INSERT INTO "main_url" VALUES (3,'http://ngoaithat.com/',123.0,12312.0,1,'http://ngoaithatáaaaaaaadainam.com/','http://ngoaithat.com/');
INSERT INTO "main_url" VALUES (4,'https://cellphones.com.vn/iphone-12-pro-max.html',29500000.0,32990000.0,3,'https://cellphones.com.vn/','https://cdn.cellphones.com.vn/media/catalog/product/cache/7/image/9df78eab33525d08d6e5fb8d27136e95/i/p/iphone-12-pro-max_1__7.jpg');
INSERT INTO "main_url" VALUES (5,'https://fptshop.com.vn/dien-thoai/iphone-12-pro-max?dung-luong=128gb',29990000.0,32990000.0,3,'https://fptshop.com.vn/','https://images.fpt.shop/unsafe/fit-in/585x390/filters:quality(90):fill(white)/fptshop.com.vn/Uploads/Originals/2020/10/14/637382725406081030_ip-12-pro-max-vang-1.png');
INSERT INTO "main_url" VALUES (6,'https://viettelstore.vn/dien-thoai/iphone-12-pro-max-128gb-pid159099.html',29990000.0,31990000.0,3,'https://viettelstore.vn/','https://cdn1.viettelstore.vn/Images/Product/ProductImage/833049682.jpeg');
INSERT INTO "main_url" VALUES (7,'https://www.nguyenkim.com/dien-thoai-iphone-12-pro-128gb-bac.html',27990000.0,30990000.0,3,'https://www.nguyenkim.com/','https://cdn.nguyenkimmall.com/images/detailed/698/10047714-dien-thoai-iphone-12-pro-128gb-bac-1.jpg');
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "main_sanpham_MaLoai_id_f3e54769" ON "main_sanpham" (
	"MaLoai_id"
);
CREATE INDEX IF NOT EXISTS "main_url_MaSP_id_1971c250" ON "main_url" (
	"MaSP_id"
);
COMMIT;

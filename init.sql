CREATE DATABASE IF NOT EXISTS items_db;
USE items_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO items (id, name, stock) VALUES
(100000, 'Long Sleeve T-Shirt', 181),
(123761, 'Cargo Hoodie', 184),
(132872, 'Oversized Jacket', 217),
(298033, 'Baggy Jacket', 470),
(124354, 'Regular Fit Skirt', 391),
(156442, 'Straight Cut Coat', 254),
(234222, 'Oversized Dress', 115),
(156451, 'Baggy Sweater', 497),
(124354, 'Long Sleeve Blazer', 228),
(234553, 'Short Sleeve Sweater', 241),
(234878, 'Regular Fit Hoodie', 51),
(234875, 'Box Fit Dress', 102),
(134500, 'Slim Fit Jacket', 430),
(235885, 'Short Sleeve T-Shirt', 144),
(198062, 'Regular Fit Jeans', 270),
(123042, 'Box Fit Skirt', 180),
(168922, 'Box Fit T-Shirt', 475),
(237922, 'Regular Fit T-Shirt', 484),
(111023, 'Box Fit Sweater', 477),
(126987, 'Short Sleeve Skirt', 217),
(124911, 'Cargo T-Shirt', 66),
(221438, 'Straight Cut Hoodie', 271),
(101836, 'Oversized Blazer', 314),
(134159, 'Regular Fit Coat', 459),
(199131, 'Oversized Skirt', 56),
(112581, 'Long Sleeve Coat', 274)

ON DUPLICATE KEY UPDATE name=VALUES(name), stock=VALUES(stock);
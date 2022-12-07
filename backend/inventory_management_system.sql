-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 07, 2022 at 07:08 AM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_management_system`
--

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `del_null`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `del_null` ()  BEGIN
	DECLARE vid int;
	DECLARE finished INTEGER DEFAULT 0;
	DECLARE del_null CURSOR FOR
		SELECT DISTINCT vendor.vendor_id FROM vendor INNER JOIN invoice WHERE vendor.vendor_id = invoice.vendor_id and vendor.product_id IS NULL;

	DECLARE CONTINUE HANDLER
	FOR NOT FOUND SET finished = 1; 
    
	OPEN del_null;
		getRows: LOOP
			FETCH del_null INTO vid;
			IF finished THEN
				LEAVE getRows;
			END IF;
			DELETE FROM vendor WHERE vendor.vendor_id = vid AND vendor.product_id IS NULL;
		END LOOP;
	CLOSE del_null;
END$$

DROP PROCEDURE IF EXISTS `insert_invoice`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_invoice` (IN `pqty` INT, IN `pid` INT)  BEGIN
	UPDATE stock SET stock.pqty = stock.pqty - pqty WHERE stock.pid = pid;
END$$

DROP PROCEDURE IF EXISTS `update_qty`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_qty` (IN `qty` INT)  BEGIN
	UPDATE stock SET stock.pqty = qty, stock.purchase_date = CURRENT_DATE WHERE stock.pqty < 50;
END$$

--
-- Functions
--
DROP FUNCTION IF EXISTS `check_stock`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `check_stock` (`qty` INT) RETURNS VARCHAR(50) CHARSET utf8 BEGIN
	DECLARE refill VARCHAR(50);
	IF qty < 50 THEN
    	SET refill = "re-fill needed";
	ELSE
    	SET refill = "no re-fill needed";
    END IF;
   	RETURN refill;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `cust_id` int(10) NOT NULL,
  `phone_no` bigint(10) NOT NULL,
  `cust_email_id` varchar(50) NOT NULL,
  `cust_name` varchar(50) NOT NULL,
  `str_no` int(11) DEFAULT NULL,
  `str_name` varchar(50) DEFAULT NULL,
  `pincode` int(6) DEFAULT NULL,
  PRIMARY KEY (`cust_id`,`phone_no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
CREATE TABLE IF NOT EXISTS `invoice` (
  `prod_id` int(10) NOT NULL,
  `invoice_no` int(10) NOT NULL,
  `invoice_date` date NOT NULL,
  `selling_price` float NOT NULL,
  `prod_qty` int(11) DEFAULT '0',
  `discount` float DEFAULT NULL,
  `phone_no` bigint(10) DEFAULT NULL,
  `vendor_id` int(11) NOT NULL,
  PRIMARY KEY (`prod_id`,`invoice_no`),
  KEY `phone_no` (`phone_no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `email_id` varchar(50) NOT NULL,
  `pass` varchar(50) NOT NULL,
  PRIMARY KEY (`email_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `product_id` int(10) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `cost_price` float NOT NULL,
  `manufacturer` varchar(50) NOT NULL,
  `mrp` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

DROP TABLE IF EXISTS `stock`;
CREATE TABLE IF NOT EXISTS `stock` (
  `pid` int(10) NOT NULL,
  `purchase_date` date NOT NULL,
  `mfg_date` date NOT NULL,
  `pqty` int(11) DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Triggers `stock`
--
DROP TRIGGER IF EXISTS `on_insert_stock`;
DELIMITER $$
CREATE TRIGGER `on_insert_stock` BEFORE INSERT ON `stock` FOR EACH ROW BEGIN
	DECLARE err_msg1 varchar(100);
    DECLARE err_msg2 varchar(100);
    DECLARE err_msg3 varchar(100);
    SET err_msg1 = "Mfg/Purchase Date must be before the current date";
    SET err_msg2 = "Mfg Date should be before Purchase Date";
    SET err_msg3 = "Product quantity should be minimum 50";
    IF (new.purchase_date > CURRENT_DATE OR new.mfg_date > CURRENT_DATE) THEN
    	SIGNAL SQLSTATE '45000'
 		SET MESSAGE_TEXT = err_msg1;
	ELSEIF  new.mfg_date > new.purchase_date THEN
    	SIGNAL SQLSTATE '45000'
 		SET MESSAGE_TEXT = err_msg2;
	ELSEIF new.pqty < 50 THEN
    	SIGNAL SQLSTATE '45000'
 		SET MESSAGE_TEXT = err_msg3;
	END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
CREATE TABLE IF NOT EXISTS `vendor` (
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `product_id` int(10) DEFAULT NULL,
  `cust_id` int(10) DEFAULT NULL,
  KEY `email_id` (`email_id`),
  KEY `cust_id` (`cust_id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

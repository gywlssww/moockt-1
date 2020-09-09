SET NAMES utf8 ;

DROP TABLE IF EXISTS `moockt`;
SET character_set_client = utf8mb4;

CREATE TABLE `chatbotuser`(
    `id` INT(4) NOT NULL DEFAULT nextval(`chatbotuser_id_seq`::regclass),
    `user_id` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    `exp_date` TIMESTAMPTZ,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `chatbotuser` VALUES(1,`wogurrhtn`,CURRENT_TIMESTAMP());
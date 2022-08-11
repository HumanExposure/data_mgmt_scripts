SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE SCHEMA IF NOT EXISTS `prod_chemical_release` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
USE `prod_chemical_release` ;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`datasource` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `SourceName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`datadocument` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datasource_id` INT(11) NOT NULL,
  `SourceFileName` VARCHAR(200) NULL DEFAULT NULL,
  `SourceType` VARCHAR(25) NULL DEFAULT NULL,
  `SourceYear` INT(4) NULL DEFAULT NULL,
  `SourceURL` VARCHAR(200) NULL DEFAULT NULL,
  `SourceVersion` VARCHAR(50) NULL DEFAULT NULL,
  `StEWI_version` VARCHAR(10) NULL DEFAULT NULL,
  `SourceAcquisitionTime` VARCHAR(45) NULL DEFAULT NULL,
  `uploadComplete` INT(1) NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  INDEX `fk_datadocument_datasource1_idx` (`datasource_id` ASC) VISIBLE,
  CONSTRAINT `fk_datadocument_datasource1`
    FOREIGN KEY (`datasource_id`)
    REFERENCES `prod_chemical_release`.`datasource` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 64
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`facility` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `FacilityID` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `FacilityID_UNIQUE` (`FacilityID` ASC) VISIBLE,
  INDEX `FacilityID` (`FacilityID` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 379860
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`naics_info` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `NAICS_code` VARCHAR(6) NULL DEFAULT NULL,
  `keyword` VARCHAR(200) NULL DEFAULT NULL,
  `description` VARCHAR(10000) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4096
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`facility_info` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `FacilityName` VARCHAR(500) NULL DEFAULT NULL,
  `CompanyName` VARCHAR(100) NULL DEFAULT NULL,
  `State` VARCHAR(5) NULL DEFAULT NULL,
  `County` VARCHAR(45) NULL DEFAULT NULL,
  `Latitude` VARCHAR(45) NULL DEFAULT NULL,
  `Longitude` VARCHAR(45) NULL DEFAULT NULL,
  `Address` VARCHAR(200) NULL DEFAULT NULL,
  `City` VARCHAR(100) NULL DEFAULT NULL,
  `Zip` VARCHAR(45) NULL DEFAULT NULL,
  `facility_id` VARCHAR(25) NOT NULL,
  `datadocument_id` INT(10) UNSIGNED NOT NULL,
  `NAICS_id` INT(11) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_factility_info_facility1_idx` (`facility_id` ASC) VISIBLE,
  INDEX `fk_facility_info_datadocument1_idx` (`datadocument_id` ASC) VISIBLE,
  INDEX `fk_facility_info_NAICS_info1_idx` (`NAICS_id` ASC) VISIBLE,
  CONSTRAINT `fk_facility_info_NAICS_info1`
    FOREIGN KEY (`NAICS_id`)
    REFERENCES `prod_chemical_release`.`naics_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facility_info_datadocument1`
    FOREIGN KEY (`datadocument_id`)
    REFERENCES `prod_chemical_release`.`datadocument` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_factility_info_facility1`
    FOREIGN KEY (`facility_id`)
    REFERENCES `prod_chemical_release`.`facility` (`FacilityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1974221
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`flow` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `FlowName` VARCHAR(1000) NULL DEFAULT NULL,
  `FlowID` VARCHAR(25) NULL DEFAULT NULL,
  `datadocument_id` INT(10) UNSIGNED NOT NULL,
  `CAS` VARCHAR(25) NULL DEFAULT NULL,
  `rid` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_flow_datadocument1_idx` (`datadocument_id` ASC) VISIBLE,
  CONSTRAINT `fk_flow_datadocument1`
    FOREIGN KEY (`datadocument_id`)
    REFERENCES `prod_chemical_release`.`datadocument` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 20283079
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`flowbyfacility` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `FlowAmount` VARCHAR(45) NULL DEFAULT NULL,
  `ReliabilityScore` VARCHAR(25) NULL DEFAULT NULL,
  `flow_id` INT(11) NOT NULL,
  `Compartment` VARCHAR(25) NULL DEFAULT NULL,
  `Unit` VARCHAR(10) NULL DEFAULT NULL,
  `facility_id` VARCHAR(25) NOT NULL,
  `datadocument_id` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_flowbyfacility_flow1_idx` (`flow_id` ASC) VISIBLE,
  INDEX `fk_flowbyfacility_facility1_idx` (`facility_id` ASC) VISIBLE,
  INDEX `fk_flowbyfacility_datadocument1_idx` (`datadocument_id` ASC) VISIBLE,
  CONSTRAINT `fk_flowbyfacility_datadocument1`
    FOREIGN KEY (`datadocument_id`)
    REFERENCES `prod_chemical_release`.`datadocument` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_flowbyfacility_facility1`
    FOREIGN KEY (`facility_id`)
    REFERENCES `prod_chemical_release`.`facility` (`FacilityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_flowbyfacility_flow1`
    FOREIGN KEY (`flow_id`)
    REFERENCES `prod_chemical_release`.`flow` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 20283079
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
CREATE TABLE IF NOT EXISTS `prod_chemical_release`.`validation` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `Inventory_Amount` VARCHAR(25) NULL DEFAULT NULL,
  `Reference_Amount` VARCHAR(25) NULL DEFAULT NULL,
  `Percent_Difference` VARCHAR(45) NULL DEFAULT NULL,
  `Conclusion` VARCHAR(45) NULL DEFAULT NULL,
  `flow_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_validation_flow1_idx` (`flow_id` ASC) VISIBLE,
  CONSTRAINT `fk_validation_flow1`
    FOREIGN KEY (`flow_id`)
    REFERENCES `prod_chemical_release`.`flow` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 20283079
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

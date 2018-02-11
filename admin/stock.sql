
--DROP TABLE IF EXISTS `trade`;
CREATE TABLE IF NOT EXISTS `trade` (
	`id`		integer PRIMARY KEY autoincrement,
	`user`		integer,
	`date`		varchar(32),
	`deal`		varchar(32),
	`code`		varchar(32),
	`price`		real,
	`volume`	integer,
	`amount`	real,
	`message`	text
);
CREATE INDEX IF NOT EXISTS ix_trade_user ON `trade` (`user`, `date`);


--#DROP TABLE IF EXISTS `monitor`;
CREATE TABLE IF NOT EXISTS `monitor` (
	`id`		integer PRIMARY KEY autoincrement,
	`user`		integer,
	`date`		varchar(32),
	`code`		varchar(32) NOT NULL,
	`volume`	integer,
	`amount`	real,
	`message`	text
);
INSERT INTO monitor(code, volume) values ('600300', 1);


DROP TABLE IF EXISTS `baseinfo`;
CREATE TABLE IF NOT EXISTS `baseinfo` (
	`id` 		integer PRIMARY KEY autoincrement,
	`code` 		varchar(32) NOT NULL,
	`name` 		varchar(32),
	`industry` 	varchar(32),
	`concept` 	varchar(32),
	`area` 		varchar(32),
	`issme` 	integer DEFAULT 0,
	`isgem` 	integer DEFAULT 0,
	`isst`  	integer DEFAULT 0,
	`ishs300`	integer DEFAULT 0,
	`issz50`	integer DEFAULT 0,
	`iszz500`	integer DEFAULT 0
);
CREATE INDEX IF NOT EXISTS `ix_baseinfo_code` ON `baseinfo` (`code`);


--DROP TABLE IF EXISTS `hist`;
CREATE TABLE IF NOT EXISTS `hist` (
	`id`		integer PRIMARY KEY autoincrement,
	`date`		varchar(32) NOT NULL,
	`code`		varchar(32) NOT NULL,
	`open`		real,
	`close`		real,
	`high`		real,
	`low`		real,
	`volume`	real,

	`price_change`	real,
	`p_change`		real,
	`ma5`			real,
	`ma10`			real,
	`ma20`			real,
	`v_ma5`			real,
	`v_ma10`		real,
	`v_ma20`		real,
	`turnover`		real,

	`hfq`			real,
	`qfq`			real,
	`curve`			integer DEFAULT 0
);
CREATE INDEX IF NOT EXISTS `ix_hist_date`	ON `hist` (`date`, `curve`);
CREATE INDEX IF NOT EXISTS `ix_hist_code`	ON `hist` (`code`, `curve`);


DROP TABLE IF EXISTS `ndata`;
CREATE TABLE IF NOT EXISTS `ndata` (
	`id`		integer PRIMARY KEY autoincrement,
	`date`		varchar(32),
	`code`		varchar(32),
	`changepercent`	real,
	`trade`			real,
	`open`			real,
	`high`			real,
	`low`			real,
	`settlement`	real,
	`volume`		real,
	`turnoverratio`	real,
	`amount`		real,
	`per`			real,
	`pb`			real,
	`mktcap`		real,
	`nmc`			real,

	`start`		varchar(32),
	`mhdate`	varchar(32),
	`maxhigh`	real,
	`mldate`	varchar(32),
	`minlow`	real,

);


DROP TABLE IF EXISTS `kdata`;
CREATE TABLE IF NOT EXISTS `kdata` (
	`id`		integer PRIMARY KEY autoincrement,
	`date`		varchar(32) NOT NULL,
	`code`		varchar(32) NOT NULL,
	`open`		real,
	`close`		real,
	`high`		real,
	`low`		real,
	`volume`	real,

	`pc`		real,
	`pcr`		real,
	`vc`		real,
	`vcr`		real,

	`ma5`		real,
	`ma10`		real,
	`ma20`		real,
	`ma30`		real,
	`ma60`		real,

	`va5`		real,
	`va10`		real,
	`va20`		real,
	`va30`		real,
	`va60`		real,

	`istop`		integer,
	`isbottom`	integer
);
CREATE INDEX IF NOT EXISTS `ix_kdata_date`	ON `kdata` (`date`);
CREATE INDEX IF NOT EXISTS `ix_kdata_code`	ON `kdata` (`code`, `date`);


DROP TABLE IF EXISTS `log`;
CREATE TABLE IF NOT EXISTS `log` (
	`id`		integer PRIMARY KEY autoincrement,
	`datetime`	datetime default (datetime(CURRENT_TIMESTAMP, 'localtime')),
	`operate`	text,
	`result`	text,
	`message`	text
);
CREATE INDEX IF NOT EXISTS `ix_log_operate` ON `log` (`operate`, `datetime`);


-- CREATE TABLE [dbo].[brokers](
--     [id] BIGINT IDENTITY(1,1) NOT NULL,
-- 	[brokerName] [varchar](64) NOT NULL,
--     [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	PRIMARY KEY CLUSTERED (id ASC),
-- 	UNIQUE NONCLUSTERED (brokerName ASC)
-- )

-- CREATE TABLE [dbo].[users](
--     [id] BIGINT IDENTITY(1,1) NOT NULL,
-- 	[email] [varchar](64) NOT NULL,
-- 	[password] [varchar](255) NOT NULL,
-- 	[role] [varchar](8) NOT NULL,
-- 	[adminBrokerID] BIGINT NULL,
--     [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	PRIMARY KEY CLUSTERED (id ASC),
-- 	FOREIGN KEY (adminBrokerID) REFERENCES brokers(id) ON DELETE NO ACTION,
-- )
-- CREATE UNIQUE NONCLUSTERED INDEX uidx_u ON [dbo].[users] (email ASC);

-- CREATE TABLE [dbo].[clients](
--     [id] [varchar](64) NOT NULL,
-- 	[brokerID] BIGINT NOT NULL,
--     [owner] [nvarchar](64) NOT NULL,
--     [fee] [FLOAT] NOT NULL,
--     [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	PRIMARY KEY CLUSTERED (id ASC),
-- 	FOREIGN KEY (brokerID) REFERENCES brokers(id) ON DELETE NO ACTION
-- )

-- CREATE TABLE [dbo].[userClientMemberships](
--     [id] [varchar](64) NOT NULL,
-- 	[userID] BIGINT NOT NULL,
-- 	[clientID] [varchar](64) NOT NULL,
--     [role] [varchar](10) NOT NULL,
--     [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	PRIMARY KEY CLUSTERED (id ASC),
-- 	FOREIGN KEY (userID) REFERENCES users(id) ON DELETE CASCADE,
-- 	FOREIGN KEY (clientID) REFERENCES clients(id) ON DELETE CASCADE
-- )
-- CREATE UNIQUE NONCLUSTERED INDEX ucmidx_uc ON [dbo].[userClientMemberships] (userID ASC, clientID ASC);

CREATE TABLE [dbo].[users](
    [id] BIGINT IDENTITY(1,1) NOT NULL,
	[email] [varchar](64) NOT NULL,
	[password] [varchar](255) NOT NULL,
	[role] [varchar](8) NOT NULL,
	[adminNameBroker] [varchar](64) NULL,
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
	-- FOREIGN KEY (adminBrokerID) REFERENCES brokers(id) ON DELETE NO ACTION,
)
CREATE UNIQUE NONCLUSTERED INDEX uidx_u ON [dbo].[users] (email ASC);

CREATE TABLE [dbo].[userClientMemberships](
    [id] BIGINT IDENTITY(1,1) NOT NULL,
	[userID] BIGINT NOT NULL,
	[idClient] [varchar](64) NOT NULL,
    [role] [varchar](10),
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
	FOREIGN KEY (userID) REFERENCES users(id) ON DELETE CASCADE,
	-- FOREIGN KEY (clientID) REFERENCES clients(id) ON DELETE CASCADE
)
CREATE UNIQUE NONCLUSTERED INDEX ucmidx_uc ON [dbo].[userClientMemberships] (userID ASC, idClient ASC);

CREATE TABLE [dbo].[broker] (
	[__createdAt__] nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT format(switchoffset(sysutcdatetime(),'+07:00'),'yyyy-MM-dd HH:mm:ss') NOT NULL,
	[__updatedAt__] nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT format(switchoffset(sysutcdatetime(),'+07:00'),'yyyy-MM-dd HH:mm:ss') NOT NULL,
	[id] BIGINT IDENTITY(1,1) NOT NULL,
	nameBroker nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	typeBroker nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__broker__3213E83F1291F419 PRIMARY KEY (id),
	CONSTRAINT UQ__broker__24987FF09DB6010D UNIQUE (nameBroker)
);

CREATE TABLE [dbo].[client] (
	[__createdAt__] nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT format(switchoffset(sysutcdatetime(),'+07:00'),'yyyy-MM-dd HH:mm:ss') NOT NULL,
	[__updatedAt__] nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT format(switchoffset(sysutcdatetime(),'+07:00'),'yyyy-MM-dd HH:mm:ss') NOT NULL,
	[id] BIGINT IDENTITY(1,1) NOT NULL,
	nameBroker nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	idClient nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nameClient nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	interestRate float NULL,
	costBuy float NULL,
	costSell float NULL,
	CONSTRAINT PK__client__3213E83FE054415B PRIMARY KEY (id),
	CONSTRAINT UQ__client__A6A610D56CB44C7C UNIQUE (idClient)
);

ALTER TABLE master.dbo.client ADD CONSTRAINT FK__client__nameBrok__573DED66 FOREIGN KEY (nameBroker) REFERENCES master.dbo.broker(nameBroker) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE [dbo].[brokers](
    id BIGINT IDENTITY(1,1) NOT NULL,
	brokerName [varchar](64) NOT NULL,
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
	UNIQUE NONCLUSTERED (brokerName ASC)
)

CREATE TABLE [dbo].[users](
    id BIGINT IDENTITY(1,1) NOT NULL,
	userName [varchar](64) NOT NULL,
	password [varchar](64) NOT NULL,
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
)
CREATE UNIQUE NONCLUSTERED INDEX uidx_u ON [dbo].[users] (userName ASC);

CREATE TABLE [dbo].[clients](
    id [varchar](64) NOT NULL,
	brokerID BIGINT NOT NULL,
    owner [nvarchar](64) NOT NULL,
    fee [FLOAT] NOT NULL,
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
	FOREIGN KEY (brokerID) REFERENCES brokers(id) ON DELETE NO ACTION
)

CREATE TABLE [dbo].[userClientMemberships](
    id [varchar](64) NOT NULL,
	userID BIGINT NOT NULL,
	clientID [varchar](64) NOT NULL,
	permission [varchar](10) NOT NULL,
    role [varchar](10) NOT NULL,
    [createdAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NOT NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	PRIMARY KEY CLUSTERED (id ASC),
	FOREIGN KEY (userID) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (clientID) REFERENCES clients(id) ON DELETE CASCADE
)
CREATE UNIQUE NONCLUSTERED INDEX ucmidx_uc ON [dbo].[userClientMemberships] (userID ASC, clientID ASC);

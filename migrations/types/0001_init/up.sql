CREATE TYPE [dbo].[brokers] AS TABLE(
    id BIGINT NULL,
	brokerName [varchar](64) NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)

CREATE TYPE [dbo].[users] AS TABLE(
    id BIGINT NULL,
	userName [varchar](64) NULL,
	password [varchar](255) NULL,
	[role] [varchar](8) NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)


CREATE TYPE [dbo].[clients] AS TABLE(
    id [varchar](64) NULL,
	brokerID BIGINT NULL,
    owner [nvarchar](64) NULL,
    fee [FLOAT] NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)

CREATE TYPE [dbo].[userClientMemberships] AS TABLE(
    id [varchar](64) NULL,
	userID BIGINT NULL,
	clientID [varchar](64) NULL,
	permission [varchar](10) NULL,
    role [varchar](10) NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)

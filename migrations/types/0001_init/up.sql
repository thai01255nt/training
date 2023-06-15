-- CREATE TYPE [trading].[brokers] AS TABLE(
--     [id] BIGINT NULL,
-- 	[brokerName] [varchar](64) NULL,
--     [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
-- )

CREATE TYPE [trading].[users] AS TABLE(
    [id] BIGINT NULL,
	[email] [varchar](64) NULL,
	[password] [varchar](255) NULL,
	[role] [varchar](8) NULL,
	[adminNameBroker] [varchar](64) NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)

-- CREATE TYPE [trading].[clients] AS TABLE(
--     [id] [varchar](64) NULL,
-- 	[brokerID] BIGINT NULL,
--     [owner] [nvarchar](64) NULL,
--     [fee] [FLOAT] NULL,
--     [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
-- 	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
-- )

CREATE TYPE [trading].[userClientMemberships] AS TABLE(
    [id] [varchar](64) NULL,
	[userID] BIGINT NULL,
	[idClient] [varchar](64) NULL,
	[permission] [varchar](10) NULL,
    [role] [varchar](10) NULL,
    [createdAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00'),
	[updatedAt] DATETIME NULL DEFAULT switchoffset(sysutcdatetime(),'+07:00')
)

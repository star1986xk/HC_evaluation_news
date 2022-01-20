-- ----------------------------
-- Table structure for evaluation_news
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[evaluation_news]') AND type IN ('U'))
	DROP TABLE [dbo].[evaluation_news]
GO

CREATE TABLE [dbo].[evaluation_news] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [title] nvarchar(1000) COLLATE Chinese_PRC_CI_AS  NULL,
  [release_time] datetime2(7)  NULL,
  [url] nvarchar(1000) COLLATE Chinese_PRC_CI_AS  NULL,
  [uid] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[evaluation_news] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'标题',
'SCHEMA', N'dbo',
'TABLE', N'evaluation_news',
'COLUMN', N'title'
GO

EXEC sp_addextendedproperty
'MS_Description', N'发布时间',
'SCHEMA', N'dbo',
'TABLE', N'evaluation_news',
'COLUMN', N'release_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'网址',
'SCHEMA', N'dbo',
'TABLE', N'evaluation_news',
'COLUMN', N'url'
GO

EXEC sp_addextendedproperty
'MS_Description', N'uid',
'SCHEMA', N'dbo',
'TABLE', N'evaluation_news',
'COLUMN', N'uid'
GO


-- ----------------------------
-- Auto increment value for evaluation_news
-- ----------------------------
DBCC CHECKIDENT ('[dbo].[evaluation_news]', RESEED, 4)
GO


-- ----------------------------
-- Indexes structure for table evaluation_news
-- ----------------------------
CREATE UNIQUE NONCLUSTERED INDEX [index]
ON [dbo].[evaluation_news] (
  [uid] ASC
)
GO


-- ----------------------------
-- Primary Key structure for table evaluation_news
-- ----------------------------
ALTER TABLE [dbo].[evaluation_news] ADD CONSTRAINT [PK__evaluati__3213E83F0F624AF8] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


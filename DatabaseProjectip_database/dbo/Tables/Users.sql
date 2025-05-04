CREATE TABLE [dbo].[Users] (
    [Id]               INT            IDENTITY (1, 1) NOT NULL,
    [Username]         NVARCHAR (100) NOT NULL,
    [Email]            NVARCHAR (255) NOT NULL,
    [Password]         NVARCHAR (255) NOT NULL,
    [Permissions_Tier] INT            DEFAULT ((0)) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);


GO


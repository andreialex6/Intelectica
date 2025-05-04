CREATE TABLE [dbo].[Parinti] (
    [Id]       INT            NOT NULL,
    [Username] NVARCHAR (100) NOT NULL,
    [Nume]     NVARCHAR (100) NOT NULL,
    [Prenume]  NVARCHAR (100) NOT NULL,
    [CopilId]  INT            NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);


GO


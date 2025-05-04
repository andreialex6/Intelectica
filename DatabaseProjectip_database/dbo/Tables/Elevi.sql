CREATE TABLE [dbo].[Elevi] (
    [Id]       INT            NOT NULL,
    [Username] NVARCHAR (100) NOT NULL,
    [Nume]     NVARCHAR (100) NOT NULL,
    [Prenume]  NVARCHAR (100) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);


GO


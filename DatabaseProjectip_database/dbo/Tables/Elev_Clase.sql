CREATE TABLE [dbo].[Elev_Clase] (
    [ElevId]  INT NOT NULL,
    [ClasaId] INT NOT NULL,
    PRIMARY KEY CLUSTERED ([ElevId] ASC, [ClasaId] ASC),
    FOREIGN KEY ([ClasaId]) REFERENCES [dbo].[Clase] ([Id]),
    FOREIGN KEY ([ElevId]) REFERENCES [dbo].[Elevi] ([Id])
);


GO


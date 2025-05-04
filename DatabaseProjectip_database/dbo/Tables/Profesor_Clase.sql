CREATE TABLE [dbo].[Profesor_Clase] (
    [ProfesorId] INT NOT NULL,
    [ClasaId]    INT NOT NULL,
    PRIMARY KEY CLUSTERED ([ProfesorId] ASC, [ClasaId] ASC),
    FOREIGN KEY ([ClasaId]) REFERENCES [dbo].[Clase] ([Id]),
    FOREIGN KEY ([ProfesorId]) REFERENCES [dbo].[Profesori] ([Id])
);


GO


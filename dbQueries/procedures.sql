-- Stored procedures for common queries
CREATE PROCEDURE GetElementByNumber
    @AtomicNumber INT
AS
BEGIN
    SELECT * FROM Elements WHERE AtomicNumber = @AtomicNumber;
END;
GO

CREATE PROCEDURE GetElementBySymbol
    @Symbol NVARCHAR(2)
AS
BEGIN
    SELECT * FROM Elements WHERE Symbol = @Symbol;
END;
GO

CREATE PROCEDURE GetElementsByBlock
    @Block CHAR(1)
AS
BEGIN
    SELECT * FROM Elements WHERE Block = @Block ORDER BY AtomicNumber;
END;
GO

CREATE PROCEDURE GetElementsByPeriod
    @Period INT
AS
BEGIN
    SELECT * FROM Elements WHERE Period = @Period ORDER BY AtomicNumber;
END;
G
-- Create database
CREATE DATABASE PeriodicTableDB;
GO

USE PeriodicTableDB;
GO

-- Create table for elements
CREATE TABLE Elements (
    AtomicNumber INT PRIMARY KEY,
    Symbol NVARCHAR(2) NOT NULL UNIQUE,
    Name NVARCHAR(50) NOT NULL,
    AtomicMass DECIMAL(10,4) NOT NULL,
    Block CHAR(1) NOT NULL,
    GroupNumber INT,
    Period INT NOT NULL,
    ElectronConfiguration NVARCHAR(100) NOT NULL
);
GO

-- Insert S and P block elements
INSERT INTO Elements VALUES
-- S-block elements
(1, 'H', 'Hydrogen', 1.0078, 's', 1, 1, '1s1'),
(2, 'He', 'Helium', 4.0026, 's', 18, 1, '1s2'),
(3, 'Li', 'Lithium', 6.9410, 's', 1, 2, '1s2 2s1'),
(4, 'Be', 'Beryllium', 9.0122, 's', 2, 2, '1s2 2s2'),
(11, 'Na', 'Sodium', 22.9898, 's', 1, 3, '[Ne] 3s1'),
(12, 'Mg', 'Magnesium', 24.3050, 's', 2, 3, '[Ne] 3s2'),
(19, 'K', 'Potassium', 39.0983, 's', 1, 4, '[Ar] 4s1'),
(20, 'Ca', 'Calcium', 40.0780, 's', 2, 4, '[Ar] 4s2'),

-- P-block elements
(5, 'B', 'Boron', 10.8110, 'p', 13, 2, '1s2 2s2 2p1'),
(6, 'C', 'Carbon', 12.0107, 'p', 14, 2, '1s2 2s2 2p2'),
(7, 'N', 'Nitrogen', 14.0067, 'p', 15, 2, '1s2 2s2 2p3'),
(8, 'O', 'Oxygen', 15.9994, 'p', 16, 2, '1s2 2s2 2p4'),
(9, 'F', 'Fluorine', 18.9984, 'p', 17, 2, '1s2 2s2 2p5'),
(10, 'Ne', 'Neon', 20.1797, 'p', 18, 2, '1s2 2s2 2p6');


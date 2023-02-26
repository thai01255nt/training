CREATE TABLE customers (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    name varchar(255) NOT NULL,
    phone varchar(25) NOT NULL UNIQUE,
    createdAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    updatedAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
)

CREATE TABLE employees (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    identityNumber varchar(25) NOT NULL,
    name varchar(25) NOT NULL,
    address varchar(255) NOT NULL,
    phone varchar(25) NOT NULL,
    createdAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    updatedAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
)

CREATE TABLE bills (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    soldDate date NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    customerID INT NOT NULL,
    employeeID INT NOT NULL,
    createdAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    updatedAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    FOREIGN KEY (customerID) REFERENCES customers(id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (employeeID) REFERENCES employees(id) ON DELETE NO ACTION ON UPDATE NO ACTION,
)

CREATE TABLE drugs (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    name varchar(25) NOT NULL,
    description varchar(512) NOT NULL,
    mfgDate date NOT NULL,
    expDate date NOT NULL,
    createdAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    updatedAt datetime NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
)

CREATE TABLE billDrugs (
    soldDate date NOT NULL default SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'),
    billID INT NOT NULL,
    drugID INT NOT NULL,
    FOREIGN KEY (billID) REFERENCES bills(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (drugID) REFERENCES drugs(id) ON DELETE CASCADE ON UPDATE CASCADE,
)

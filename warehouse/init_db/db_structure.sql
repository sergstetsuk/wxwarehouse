--https://gitlab.com/Screwtapello/sqlite-schema-diagram

--CREATE SCHEMA oblik;

DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS ledger;
DROP TABLE IF EXISTS operations;
DROP TABLE IF EXISTS looses;
DROP VIEW IF EXISTS current_distribution;


CREATE TABLE IF NOT EXISTS equipment(
id INTEGER PRIMARY KEY,
subaccount TEXT,
name TEXT,
year INTEGER,
measurement_unit TEXT,
price NUMERIC,
amortization NUMERIC);

CREATE TABLE IF NOT EXISTS units(
id INTEGER PRIMARY KEY,
short_name TEXT UNIQUE,
name TEXT,
sort_order INTEGER);

CREATE TABLE IF NOT EXISTS ledger(
id INTEGER PRIMARY KEY,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
document TEXT,
status INTEGER,
person TEXT,
scan BLOB);

CREATE TABLE IF NOT EXISTS operations(
id INTEGER PRIMARY KEY,
ledger_id INTEGER,
unit_id ITEGER,
equipment_id INTEGER,
quantity INTEGER,
serial_number TEXT,
FOREIGN KEY(ledger_id) REFERENCES ledger(id),
FOREIGN KEY(unit_id) REFERENCES units(id),
FOREIGN KEY(equipment_id) REFERENCES equipment(id)
);

CREATE TABLE IF NOT EXISTS looses(
id INTEGER PRIMARY KEY,
ledger_id INTEGER,
unit_id ITEGER,
equipment_id INTEGER,
quantity INTEGER,
serial_number TEXT,
FOREIGN KEY(ledger_id) REFERENCES ledger(id),
FOREIGN KEY(unit_id) REFERENCES units(id),
FOREIGN KEY(equipment_id) REFERENCES equipment(id)
);

CREATE VIEW current_distribution (unit_id, equipment_id, serial_number, quantity)
AS SELECT op.unit_id, op.equipment_id, op.serial_number, SUM(quantity) as quantity
FROM operations op GROUP BY op.unit_id, op.equipment_id, op.serial_number HAVING SUM(quantity) > 0;


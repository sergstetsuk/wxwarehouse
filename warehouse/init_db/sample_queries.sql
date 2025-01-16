SELECT u.short_name, e.name, e.price, e.amortization, SUM(op.quantity), SUM(op.quantity)*e.price, SUM(op.quantity)*e.amortization FROM operations op LEFT JOIN units u ON op.unit_id = u.id LEFT JOIN equipment e ON op.equipment_id = e.id GROUP BY op.unit_id, op.equipment_id;

SELECT u.short_name, e.name, e.id, e.measurement_unit, op.quantity, SUM(op.quantity), SUM(op.quantity)*e.price, SUM(op.quantity)*e.amortization FROM operations op LEFT JOIN units u ON op.unit_id = u.id LEFT JOIN equipment e ON op.equipment_id = e.id GROUP BY op.unit_id, op.equipment_id;

CREATE VIEW current_distribution (unit_id, equipment_id, serial_number, quantity) AS SELECT op.unit_id, op.equipment_id, op.serial_number, SUM(quantity) FROM operations op GROUP BY op.unit_id, op.equipment_id, op.serial_number;

SELECT u.short_name, e.name, e.id, GROUP_CONCAT(NULLIF(op.serial_number,"")), e.measurement_unit, SUM(op.quantity), SUM(op.quantity)*e.price, SUM(op.quantity)*e.amortization FROM current_distribution op LEFT JOIN units u ON op.unit_id = u.id LEFT JOIN equipment e ON op.equipment_id = e.id GROUP BY op.unit_id, op.equipment_id;

BEGIN TRANSACTION;
INSERT INTO ledger (document, person) VALUES ("Накладна №2 від 10.01.2025", "Стецюк С.О.");
INSERT INTO operations (ledger_id, unit_id, equipment_id, serial_number, quantity) VALUES (last_insert_rowid(), 129, 111602236, "КІТ300891012", -1);
INSERT INTO operations (ledger_id, unit_id, equipment_id, serial_number, quantity) VALUES ((SELECT ledger_id FROM operations WHERE id = last_insert_rowid()), 128, 111602236, "КІТ300891012", 1);
COMMIT TRANSACTION;

sqlite3 ./experiment.sqlite -init sqlite-schema-diagram.sql "" > schema.dot
dot -Tpng schema.dot > schema.png
dot -Tsvg schema.dot > schema.svg

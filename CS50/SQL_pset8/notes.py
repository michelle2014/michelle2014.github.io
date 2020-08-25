# SQL operations: INSERT, DELETE, UPDATE, SELECT

# INSERT
INSERT INTO <table>(<columns>) VALUES(<values>)

# SELECT
SELECT <columns> FROM <table> WHERE <condition> ORDER BY <column>
                              WHERE idnum < 12
							  WHERE name = "Jerry"

# SELECT (JOIN)
SELECT <columns> FROM <table1> JOIN <table2> ON <predicate>

# UPDATE
UPDATE <table> SET <column> = <value> WHERE <predicate>

# DELETE
DELETE FROM <table> WHERE <predicate>

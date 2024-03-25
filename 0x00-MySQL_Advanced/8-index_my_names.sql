-- Creates an index idx_name_first on the table names
-- of the first letter of name.

CREATE INDEX idx_name_first
ON names(name(1));

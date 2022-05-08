CREATE OR REPLACE FUNCTION getEfficiency(Bname text)
RETURNS integer AS $total$
declare
	total integer;
BEGIN
	 EXECUTE format('CREATE VIEW Result AS SELECT eff_factor FROM Building WHERE name= ' || quote_nullable(Bname));
	CREATE VIEW Prod AS SELECT sum(Usage) FROM meter_entry WHERE EXTRACT(MONTH FROM Start_date) = 3;
	CREATE VIEW Total as SELECT * FROM Prod, Result;
	SELECT sum * eff_Factor INTO total FROM Total;
	DROP VIEW Total;
	DROP VIEW Prod;
	DROP VIEW Result;
	RETURN total;
END;
$total$ LANGUAGE plpgsql;

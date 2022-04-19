CREATE OR REPLACE FUNCTION getMonthUsage(theMonth integer)
RETURNS integer AS $total$
declare
	total integer;
BEGIN
	SELECT SUM(Usage) INTO total From METER_ENTRY
	WHERE EXTRACT(MONTH FROM Start_date) = theMonth;
	RETURN total;
END;
$total$ LANGUAGE plpgsql;

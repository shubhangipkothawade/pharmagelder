START TRANSACTION;
UPDATE transaction SET tra_fk_recipient = 10490 WHERE tra_fk_recipient = 10485;
DELETE FROM recipient WHERE rec_id = 10485;
COMMIT;

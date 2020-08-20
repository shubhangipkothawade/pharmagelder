START TRANSACTION;
ALTER TABLE pharma DROP IF EXISTS pha_note;
ALTER TABLE pharma ADD pha_note TEXT NULL;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Actelion Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Janssen-Cilag enthalten.", "fr": "XXXNOTEXXX"}' WHERE pha_id = 2;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Alcon Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Novartis enthalten.", "fr": "XXXNOTEXXX"}' WHERE pha_id = 3;
UPDATE pharma SET pha_note = '{"de": "Basilea hat den Pharma-Kooperations-Kodex nicht unterzeichnet, Veröffentlichungen geschehen auf freiwilliger Basis. Für 2019 hat das Unternehmen noch keine Zahlen veröffentlicht.", "fr": "XXXNOTEXXX"}' WHERE pha_id = 25;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Teva Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Mepha enthalten.", "fr": "XXXNOTEXXX"}' WHERE pha_id = 55;
COMMIT;

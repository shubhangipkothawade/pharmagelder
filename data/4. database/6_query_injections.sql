START TRANSACTION;
ALTER TABLE pharma DROP IF EXISTS pha_note;
ALTER TABLE pharma ADD pha_note TEXT NULL;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Actelion Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Janssen-Cilag enthalten.", "fr": "Depuis 2019, les rapports de transparence d'Actelion ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l'entreprise Janssen-Cilag."}' WHERE pha_id = 2;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Alcon Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Novartis enthalten.", "fr": "Depuis 2019, les rapports de transparence d'Alcon ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l'entreprise Novartis."}' WHERE pha_id = 3;
UPDATE pharma SET pha_note = '{"de": "Basilea hat den Pharma-Kooperations-Kodex nicht unterzeichnet, Veröffentlichungen geschehen auf freiwilliger Basis. Für 2019 hat das Unternehmen noch keine Zahlen veröffentlicht.", "fr": "Basilea n'est pas signataire du Code de coopération pharmaceutique, ses publications de rapports se font sur une base volontaires. L'entreprise n'a pas communiqué de chiffres pour 2019."}' WHERE pha_id = 25;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Teva Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Mepha enthalten.", "fr": "Depuis 2019, les rapports de transparence de Teva ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l'entreprise Mepha."}' WHERE pha_id = 55;
UPDATE recipient SET rec_name = 'Novartis Pharma AG (als Empfänger)' WHERE rec_id = 10008;
COMMIT;

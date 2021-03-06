START TRANSACTION;
UPDATE transaction SET tra_fk_recipient = 10490 WHERE tra_fk_recipient = 10485;
DELETE FROM recipient WHERE rec_id = 10485;
UPDATE transaction SET tra_fk_recipient = 762 WHERE tra_fk_recipient = 10749;
DELETE FROM recipient WHERE rec_id = 10749;
UPDATE transaction SET tra_fk_recipient = 6719 WHERE tra_fk_recipient = 6720;
DELETE FROM recipient WHERE rec_id = 6720;
ALTER TABLE pharma ADD COLUMN pha_note TEXT NULL;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Actelion Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Janssen-Cilag enthalten.", "fr": "Depuis 2019, les rapports de transparence d\'Actelion ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l\'entreprise Janssen-Cilag."}' WHERE pha_id = 2;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Alcon Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Novartis enthalten.", "fr": "Depuis 2019, les rapports de transparence d\'Alcon ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l\'entreprise Novartis."}' WHERE pha_id = 3;
UPDATE pharma SET pha_note = '{"de": "Basilea hat den Pharma-Kooperations-Kodex nicht unterzeichnet, Veröffentlichungen geschehen auf freiwilliger Basis. Für 2019 hat das Unternehmen noch keine Zahlen veröffentlicht.", "fr": "Basilea n\'est pas signataire du Code de coopération pharmaceutique, ses publications de rapports se font sur une base volontaires. L\'entreprise n\'a pas communiqué de chiffres pour 2019."}' WHERE pha_id = 25;
UPDATE pharma SET pha_note = '{"de": "Seit 2019 weist Teva Offenlegungen nicht mehr gesondert aus. Die Daten sind neu in den Veröffentlichungen der Firma Mepha enthalten.", "fr": "Depuis 2019, les rapports de transparence de Teva ne sont plus publiés à part. Les données sont désormais intégrées dans les rapports de l\'entreprise Mepha."}' WHERE pha_id = 55;
UPDATE pharma SET pha_note = '{"de": "Baxalta wurde 2016 verkauft und später in das Unternehmen Takeda integriert.", "fr": "Baxalta a été vendu en 2016 et était intégré dans l\'entreprise Takeda plus tard."}' WHERE pha_id = 9;
UPDATE recipient SET rec_name = 'Novartis Pharma AG (als Empfänger)' WHERE rec_id = 10008;
UPDATE recipient SET rec_location = 'Estavayer-Le-Lac' WHERE rec_id = 239;
UPDATE recipient SET rec_location = 'Chêne-Bougeries' WHERE rec_id = 496;
UPDATE recipient SET rec_location = 'Carouge' WHERE rec_id = 976;
UPDATE recipient SET rec_location = 'Stans' WHERE rec_id = 1136;
UPDATE recipient SET rec_location = 'La Chaux-de-Fonds' WHERE rec_location = 'La Chaux-de- Fonds';
UPDATE recipient SET rec_location = 'Baden' WHERE rec_location = 'Baden-Dättwil';
UPDATE recipient SET rec_location = 'Basel' WHERE rec_location = 'Basel UniSpital';
UPDATE recipient SET rec_location = 'Zürich' WHERE rec_location = 'Zuerich';
UPDATE recipient SET rec_location = 'Le Grand-Saconnex' WHERE rec_location = 'Le Grand- Saconnex';
UPDATE recipient SET rec_location = 'Yverdon-Les-Bains' WHERE rec_location = 'Yverdon-Les- Bains';
UPDATE recipient SET rec_location = 'Estavayer-Le-Lac' WHERE rec_location = 'Estavayer-Ie-Lac';
UPDATE recipient SET rec_location = 'Frauenfeld' WHERE rec_location = 'Frauenfeid';
UPDATE recipient SET rec_location = 'Wallisellen' WHERE rec_location = 'Glattzentrum';
UPDATE recipient SET rec_location = 'Sainte-Croix' WHERE rec_location = 'Sainte Croix';
UPDATE recipient SET rec_location = 'Neuchâtel' WHERE rec_location = 'Neuchätel';
UPDATE recipient SET rec_location = 'Olten' WHERE rec_location = 'Oiten';
UPDATE pharma SET pha_name = 'Nordic Pharma' WHERE pha_id = 41;
COMMIT;

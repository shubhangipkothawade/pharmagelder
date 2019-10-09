START TRANSACTION;
INSERT INTO pharma_source (`phs_fk_pharma`, `phs_source`) VALUES 
('60', 'http://recordati.ch/de/home/transparenz-pharma-kooperations-kodex/'), 
('41', 'https://www.nordicpharma.ch/about-us/transparency/');
COMMIT;

START TRANSACTION;
INSERT INTO pharma_source (`phs_fk_pharma`, `phs_source`) VALUES 
('61', 'https://www.mt-pharma-de.com/aktuelles/transparenz.html'), 
('62', 'https://www.five.ch/futurehealth-declaration/'), 
('63', 'https://www.ipsen.com/germany/uber-uns/'), 
('64', 'https://www.sunovion.eu/corporate-social-responsibility/responsible-practices/hcp-payment-disclosure.html');
COMMIT;

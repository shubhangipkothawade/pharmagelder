START TRANSACTION;
INSERT INTO transaction_category (`trc_id`, `trc_name`) VALUES 
('1', 'donations_grants'), 
('2', 'sponsorship'), 
('3', 'registration_fees'), 
('4', 'travel_accommodation'), 
('5', 'fees'), 
('6', 'related_expenses'), 
('7', 'total');
COMMIT;

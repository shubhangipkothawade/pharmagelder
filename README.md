## Formatierungsregeln
* Name: `Vorname Nachname`
* Land: `Switzerland`
* Type: `hcp` oder `hco`
* Zahlen: Tausendertrenner. Dezimaltrenner = Punkt

## Nützliche Funktionen

**replace_apostrophe**  
`df_export = replace_apostrophe(df_export)`  
Entfernt Tausendertrenner in den (zur Zeit noch als String vorliegenden) Nummernfelder**

**amounts_to_number**  
`df_export = amounts_to_number(df_export)`  
Wandelt String-Kolumnen in Zahlen um. Bedingt, dass die entsprechenden Kolumnen bereits korrekt heissen

**sum_amounts**  
`df_export = sum_amounts(df_export)`  
Summiert die entsprechenden Werte und schreibt sie ins Total

**set_type_by_alphabetical_order**  
`df_export = set_type_by_alphabetical_order(df_export)`  
Geht durch die Liste mit Namen. Sobald ein Bruch in der Reihenfolge gefunden wird, nimmt die Funktion an, dass ab jetzt ein anderer Type (hcp oder hco) starten muss.  
Default: Ersten Zeilen hcp, danach hcp. Falls die ersten hcp sein sollen, mit Parameter ergänzen:  
`df_export = set_type_by_alphabetical_order(df_export, hcp_before_hco = False)`

**basic_string_conversion**  
`df_export = basic_string_conversion(df_export)`  
Nimmt die gängisten Umformungen vor wie:  
* `CH` zu `Switzerland`

**remove_carination**  
`df_export = remove_carination(df_export)`  
Entfernt alle Umbrüche (\r) in **allen** Columns

**add_uci**  
`df_export = add_uci()`  
Fügt die UCI an entsprechender Stelle ein
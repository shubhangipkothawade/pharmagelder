## Formatierungsregeln
* Name: `Vorname Nachname`
* Land: `Switzerland`
* Type: `hcp` oder `hco`
* Zahlen: Tausendertrenner. Dezimaltrenner = Punkt

## Nützliche Funktionen

### Zwingende Funktionen

**basic_string_conversion**  
`df_export = basic_string_conversion(df_export)`  
Nimmt die gängisten Umformungen vor wie:  
* `Switzerland` zu `CH`

**write_to_excel**  
`df_export = write_to_excel(df_export, 'export.xlsx)`  
Speichert das Dataframe als Excel. Überprüft zusätzlich das Dataframe

### Zahlen formatieren

**cleanup_number**  
`df_export = cleanup_number(df_export)`  
Ruft folgende Funktionen auf:
* replace_apostrophe
* remove_chf
* remove_spaces

**replace_apostrophe**  
`df_export = replace_apostrophe(df_export)`  
Entfernt Tausendertrenner in den (zur Zeit noch als String vorliegenden) Zahlenfeldern**

**remove_chf**  
`df_export = remove_chf(df_export)`  
Entfernt `CHF` in  allen Zahlenfeldern

**remove_spaces**  
`df_export = remove_spaces(df_export)`  
Entfernt Leerzeichen in allen Zahlenfeldern

**replace_comma_to_dot**  
`df_export = replace_comma_to_dot(df_export)`  
Ersetzt Kommas mit Punkt in allen Zahlenfeldern

**remove_dots**  
`df_export = remove_dots(df_export)`  
Entfernt alle Punkte in allen Zahlenfeldern

**amounts_to_number**  
`df_export = amounts_to_number(df_export)`  
Wandelt String-Kolumnen in Zahlen um. Bedingt, dass die entsprechenden Kolumnen bereits korrekt heissen

### Type hinzufügen

**set_type_by_alphabetical_order**  
`df_export = set_type_by_alphabetical_order(df_export)`  
Geht durch die Liste mit Namen. Sobald ein Bruch in der Reihenfolge gefunden wird, nimmt die Funktion an, dass ab jetzt ein anderer Type (hcp oder hco) starten muss.  
Default: Ersten Zeilen hcp, danach hcp. Falls die ersten hcp sein sollen, mit Parameter ergänzen:  
`df_export = set_type_by_alphabetical_order(df_export, hcp_before_hco = False)`

**add_type_by_index**  
`add_type_by_index(df_export, 220, [type_before = 'hcp', type_after = 'hco'])`  
Fügt allen Zellen mit Index kleiner als 220 den Typ "hcp" hinzu. Den anderen "hco"

### Anderes

**sum_amounts**  
`df_export = sum_amounts(df_export)`  
Summiert die entsprechenden Werte und schreibt sie ins Total

**remove_carination**  
`df_export = remove_carination(df_export)`  
Entfernt alle Umbrüche (\r) in **allen** Columns

**add_uci**  
`df_export = add_uci()`  
Fügt die UCI an entsprechender Stelle ein

**remove_empty_columns**  
`df_export = remove_empty_columns(df_export)`  
Entfernt alle Collumns, die leer sind
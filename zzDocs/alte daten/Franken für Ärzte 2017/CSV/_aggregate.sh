rm ~/_aggregate.csv
for f in *.csv ; do sed 1d "$f" | sed "s/^/\"$f\",/" >> ~/_aggregate.csv ; done

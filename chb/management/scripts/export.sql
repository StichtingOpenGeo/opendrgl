\COPY (SELECT * FROM chb.current_stopplace) TO '/tmp/opendrgl_stopplace.csv' WITH CSV HEADER;
\COPY (SELECT * FROM chb.current_quay) TO '/tmp/opendrgl_quay.csv' WITH CSV HEADER;
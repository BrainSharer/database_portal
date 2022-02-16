
curl --header "Content-Type: application/json" \
--request POST \
--data '{
"prep":"DK54",
"structure_id":"SC",
"x":"10000",
"y":"9000",
"section":"200" }' \
http://localhost:8000/alignatlas

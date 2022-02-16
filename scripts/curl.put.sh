curl --header "Content-Type: application/json" \
--request PUT \
--data '{
"neuroglancer_state":"url for 129", 
"user_date":"123", 
"comments":"update 1 for ID=6", 
"lab": "NA",
"owner_id":"1"}' \
http://localhost:8000/neuroglancer/6

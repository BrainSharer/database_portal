#!/bin/bash

ID=$1
echo ""
curl -X GET "http://localhost:8000/urldata?id=$ID"
echo "\n"

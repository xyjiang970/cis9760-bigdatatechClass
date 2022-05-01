This project is an an introduction to using Amazon Web Services' OpenSearch software and visualizations were made using Kibana.

The goal is to fetch and upload anywhere between 300K-500K rows of data from NYC Open Data's Open Parking and Camera Violations dataset and explore the data using Kibana to help answer the following four questions:

1) Which license type receives the most violaitons?
2) Cars from what state (other than New York) received the most fines?
3) What is the most common violation?
4) What was the most common fine amount given out?

Docker build and Instructions:

docker build -t bigdataproject1:1.0 .

docker run \
-e INDEX_NAME="bigdataproject1" \
-e DATASET_ID="nc67-uf89" \
-e APP_TOKEN="<YOUR APP_TOKEN>" \
-e ES_HOST="<YOUR DOMAIN ENDPOINT>" \
-e ES_USERNAME="<YOUR USERNAME>" \
-e ES_PASSWORD="YOUR PASSWORD" \
bigdataproject1:1.0 --page_size=<YOUR DESIRED PAGESIZE> --num_pages=<OPTIONAL>

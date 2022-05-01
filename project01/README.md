# CIS 9760 Big Data Technologies: Project 1 - OpenSearch & Kibana

## :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
- [EC2 and OpenSearch Configurations](#hammer_and_wrench-EC2-and-OpenSearch-Configurations)
  * [EC2](#ec2)
  * [OpenSearch](#opensearch)
- [Docker Build and Instructions](#docker-build-and-instructions)
- [Outputs](#clipboard-Outputs)
- [Warnings](#bangbang-Warnings)
- [Kibana Charts](#bar_chart-Kibana-Charts)
- [Conclusion](#checkered_flag-conclusion)

<br></br>

## :star2: About the Project
This project is an an introduction to using Amazon Web Services' [OpenSearch](https://aws.amazon.com/opensearch-service/the-elk-stack/what-is-opensearch/) software and visualizations were made using [Kibana](https://aws.amazon.com/opensearch-service/the-elk-stack/kibana/).

The goal is to fetch and upload anywhere between <b>300K-500K</b> rows of data from NYC Open Data's [Open Parking and Camera Violations dataset](https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89) and explore the data using Kibana to help answer the following four questions:

<ol>
  <li>Which license type receives the most violaitons? (You can find what each license code corresponds to <a href="https://dmv.ny.gov/registration/registration-class-codes" target="_blank">here</a>)</li>
  <li>Cars from what state (other than New York) received the most fines?</li>
  <li>What is the most common violation?</li>
  <li>What was the most common fine amount given out?</li>
</ol>

<br></br>

## :hammer_and_wrench: EC2 and OpenSearch Configurations
### EC2:
<img width="1341" alt="image" src="https://user-images.githubusercontent.com/76984271/162643451-a990e4e3-61e7-4df8-8f64-14aea8ef6beb.png">
<img width="1236" alt="image" src="https://user-images.githubusercontent.com/76984271/162643470-7012a02c-f736-4831-97f1-d0d8f48db2d8.png">
<img width="1000" alt="image" src="https://user-images.githubusercontent.com/76984271/162643867-e22ef523-a163-499f-960e-9ed2e821664e.png">

### OpenSearch
![image](https://user-images.githubusercontent.com/76984271/162645625-54325ad8-ba69-401a-8b9c-a1b71e1855ed.png)
![image](https://user-images.githubusercontent.com/76984271/162643304-72aa19c7-a363-4691-80af-62840dfdc7b2.png)
![image](https://user-images.githubusercontent.com/76984271/162643619-8d0a1403-7ef1-421f-bd14-6490e355c8ee.png)
![image](https://user-images.githubusercontent.com/76984271/162643649-4c653284-8aa4-4608-a648-2e539fe8e645.png)

<br></br>

## Docker build and Instructions:

:gear: First build the imagine using:
```
docker build -t bigdataproject1:1.0 .
```

:running: Then run the following, replacing < > with your own respective information:
```
docker run \
-e INDEX_NAME="bigdataproject1" \
-e DATASET_ID="nc67-uf89" \
-e APP_TOKEN="<YOUR APP_TOKEN>" \
-e ES_HOST="<YOUR DOMAIN ENDPOINT>" \
-e ES_USERNAME="<YOUR USERNAME>" \
-e ES_PASSWORD="YOUR PASSWORD" \
bigdataproject1:1.0 --page_size=<YOUR DESIRED PAGESIZE> --num_pages=<OPTIONAL>
```
<b>:warning: Note:</b> when inputting the DOMAIN ENDPOINT, remember to remove the trailing "/" at the end of the URL!

<br></br>

## :clipboard: Outputs
If you were to run the code again, you should expect to see a 
```
Index already exists! Skipping
``` 
output <i>if you did not change the "INDEX_NAME" environment variable</i>. After putting in all the environment variables, and once the specified amount of data is fetched from the API and uploaded to OpenSearch, you will see:
```
Finished Uploading to OpenSearch!
```
If a field contains no information - that row is skipped. Other than that you will not see any other outputs while as the code fetches and uploads data into OpenSearch.

We need to be careful here because for some reason my setup and code can't seem to fetch more than 500K rows (in more detail in the next section).

<br></br>

## :bangbang: Warnings
The current code and configuration does not enable me to grab more than 500K rows of data. For now, please limit the number of records to below this limit. If you exceed 500K there is a good possibility your EC2 instance will time out and will need to be stopped (rebooting does not work from what I've tried)

<br></br>

## :bar_chart: Kibana Charts
Question 1: Which license type receives the most violaitons?
<img width="950" alt="image" src="https://user-images.githubusercontent.com/76984271/162653649-7ef8c649-92ee-442a-9356-7cb8ccf606bd.png">


Question 2: Cars from what state (other than New York) received the most fines?
<img width="1079" alt="image" src="https://user-images.githubusercontent.com/76984271/162654747-5d08641a-0c69-45ac-95a7-74e48c5a44b2.png">


Question 3: What is the most common violation?
<img width="1100" alt="image" src="https://user-images.githubusercontent.com/76984271/162653930-668dedb6-999a-4b5e-a99b-d237fa53a0bc.png">


Question 4: What was the most common fine amount given out?
<img width="610" alt="image" src="https://user-images.githubusercontent.com/76984271/162654464-f5a0f189-674e-4b69-b69d-6e590b272be7.png">

Overall Dashboard:
<img width="913" alt="image" src="https://user-images.githubusercontent.com/76984271/162655013-dd4ef5c1-9071-44ed-babe-adf9021212ea.png">

<br></br>

## :checkered_flag: Conclusion
For this project I was able to pull 341,725 rows of data:
<img width="1636" alt="image" src="https://user-images.githubusercontent.com/76984271/162652825-1c20f49d-9baf-4c8e-8320-60b6ba6e2515.png">

![image](https://user-images.githubusercontent.com/76984271/162654820-1cb5240d-663d-49d3-837b-e8e1dae91f05.png)


Moving forward, I'll try and optimize my python code along with any configurations to see how I can fetch and upload more rows into OpenSearch. In python, I want to specifically look into threading so I can split up the API request among say, 10 "workers". Overall, this was a great introduction for me into AWS EC2 and OpenSearch and the overall project cost me less than $30 to complete.

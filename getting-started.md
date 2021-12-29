# Getting Started

## Install via Docker-Compose

```
mkdir -p ~/cuebook
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/docker-compose-prod.yml -q -O ~/cuebook/docker-compose-prod.yml
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/.env -q -O ~/cuebook/.env
cd ~/cuebook
```

```
docker-compose -f docker-compose-prod.yml --env-file .env up -d
```

Now visit [localhost:3000](http://localhost:3000) in your browser.&#x20;

## Add Connection

Go to the Connections screen to create a connection.

![](<.gitbook/assets/AddConnection (1).png>)

## Add Dataset

Next, create a dataset using your connection. See [Datasets](datasets.md) for details.

## Define and Run Anomaly job

Create an anomaly detection job on your dataset. See [Anomaly Definitions](anomaly-definitions.md) for details.

Once you have created an anomaly job, click on the \`Run\` icon button to trigger the anomaly job. It might take a few seconds for the job to execute.

![](.gitbook/assets/AnomalyDefinitions.png)

Once the job is successful, go to the Anomalies screen to view your anomalies.

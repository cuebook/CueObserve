# Installation

## Install via Docker

```
mkdir -p ~/cueobserve
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/docker-compose-prod.yml -q -O ~/cueobserve/docker-compose-prod.yml
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/.env -q -O ~/cueobserve/.env
cd ~/cueobserve
```

```
docker-compose -f docker-compose-prod.yml --env-file .env up -d
```

Now visit [localhost:3000](http://localhost:3000) in your browser.&#x20;

## Use Postgres as the application database

SQLite is the default storage database for CueObserve. However, it might not be suitable for production. To use Postgres instead, do the following:

Uncomment given variable in `.env` file:

```
POSTGRES_DB_SCHEMA=cueobserve
POSTGRES_DB_USERNAME=postgres
POSTGRES_DB_PASSWORD=postgres
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
```

## Authentication

CueObserve comes with built-in authentication (powered by Django). By default authentication is disabled, to enable authentication uncomment given variables.

```
DJANGO_SUPERUSER_USERNAME=<USER_NAME>
DJANGO_SUPERUSER_PASSWORD=<PASSWORD>
DJANGO_SUPERUSER_EMAIL=<YOUR_EMAIL@DOMAIN.COM>
IS_AUTHENTICATION_REQUIRED=True
```

If authentication is enabled you can access the [Django Admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/) console to do the database operations with a nice UI. To access Django Admin go to [http://localhost:3000/admin](http://localhost:3000/admin) and enter the username and password provided in the `.env` file.

## Email Notification

CueObserve comes with built-in email alert notification system(powered by Django). By default email notifications are disabled, to enable notifications uncomment given variables.

```
EMAIL_HOST="smtp.gmail.com" 
EMAIL_HOST_USER=<YOUR_EMAIL@gmail.com>
EMAIL_HOST_PASSWORD=<YOUR_EMAIL_PASSWORD>
```

Allow less secure apps: ON for your given EMAIL\_HOST\_USER email Id, click on [enable access to less secure app](https://myaccount.google.com/lesssecureapps?pli=1\&rapt=AEjHL4N7wse3vhCsvRv-aWy8kKeEGDZS2YDbW1SfTL17HVhtemi7zZW5gzbZSBnrNgknL\_gPBDn3xVo0qUj-W6NuaYTSU7agQQ)

Unlock Captcha for your gmail account, click on [Unlock Captcha](https://accounts.google.com/b/0/UnlockCaptcha)

## Scaling Anomaly Detection using AWS Lambda

By default Anomaly Detection tasks run on a celery workers, which are limited by CPU cores hence, limiting the parallelisation. For running 1000's of anomaly detection tasks simultaneously one available option is [AWS Lambda](https://aws.amazon.com/lambda/). For configuring CueObserve to use AWS Lambda follow the steps:

### Requirements

1. [AWS ECR](https://aws.amazon.com/ecr/) - Image Registry for lambda service
2. [AWS Lambda](https://aws.amazon.com/lambda/)&#x20;

### Steps

#### Building and Deploying Image to ECR

Ensure you have `aws-cli` installed

Run below script after installing `aws-cli` and updating variable values&#x20;

```bash
aws_region=<your-region>
aws_account_id=<your-aws-account-id>
git clone https://github.com/cuebook/cueobserve
cd cueobserve
./aws_lambda_setup.sh
```

#### Setting up Lambda

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.
2. Choose **Create function**.
3. Choose the **Container image** option.
4. Under **Basic information,**&#x20;
   1. For **function name,** enter "cueObserveAnomalyDetection".
   2. For **Container image URI** select "cueobserve-lambda-image" repository & 'latest" tag.
5. Choose **Create function**.
6. Go to "cueObserveAnomalyDetection" function's details page & in **Function Overview** select **+ Add Trigger.**
7. Select **API Gateway**
8. Select **Create an API** > "Rest API" with "open" **security**.
9. Choose **Add**.
10. In function details page, select **Configuration** > **General Configuration** and update **Memory** to "512 MB" & **Timeout** to "30 sec".

#### Configuring CueObserve

Update variables in _.env_ and _.env.dev_ file&#x20;

```
DETECTION_SERVICE_PLATFORM=AWS
AWS_LAMBDA_URL=<lambda function API gateway endpoint>
```

## Infra Requirements

The minimum infrastructure requirement for CueObserve is _1 GB RAM/ 1 CPU_. If Multiple CPUs(cores) are provided, they can be utilized by tasks like Anomaly Detection & Root Cause Analysis for faster processing.

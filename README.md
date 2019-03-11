# flask-api-key-manager
This project is a very basic flask project with API key route protection. It includes a mongodb setup script, API key generator, and email notification for expiring api keys.

<h1>Requirements</h1>


1. MongoDB access to store API keys
2. Python 3.7


<h1> Installation </h1>

```
# Python3 required
> python --version
Python 3.7.2

# make sure you have virtualenv installed 
> virtualenv --version

# install virtualenv if not installed
> pip3 install virtualenv

# create virtualenv
> virtualenv -p python3 env

# activate virtualenv
> source env/bin/activate

# install dependencies
> pip install -r requirements.txt

```

<h1>Configuration</h1>

```
# template config: src/api_key_manager/example.config.json
# first copy the example.config.json to config.json and begin configuration

{
  "api_key_length": 32, // API key length
  "check_expiration_freq": 10, // the frequency at which the API keys are checked in seconds
  "seconds_till_expiration": 40, // how long API keys are kept before expiration
  "email": {
    "notification_email": "test@gmail.com", // the address used to notify users about expiring API keys
    "smtp_server": "localhost", 
    "smtp_port": "1025"
  },
  "notifications": {
    "notice1": {
      "seconds_till_expiration": 30, // seconds till expiration notice 1 will be sent out
      "subject": "Your Super Awesome Flask API key will expire in 3 seconds. \nPlease contact support@superawesome.com to get a new key!",
      "body": "Important: Your API key is about to expire"
    },
    "notice2": {
      "seconds_till_expiration": 20,
      "subject": "Your Super Awesome Flask API key will expire in 7 seconds. \nPlease contact support@superawesome.com to get a new key!",
      "body": "Important: Your API key is about to expire"
    },
    "final_notice": {
      "seconds_till_expiration": 10,
      "subject": "Your Super Awesome Flask API key will expire in 14 seconds. \nPlease contact support@superawesome.com to get a new key!",
      "body": "Important: Your API key is about to expire"
    }
  },
  "mongodb": {
    "host": "localhost",
    "port": 27017,
    "user": "",
    "password": "",
    "db": "api-db",
    "api_key_collection": "api-keys"
  }
}

```

<h1>Setup MongoDB db and collection</h1>

```
> python src/api_key_manager/setup/mongo_setup.py
```

<h1>Generate API keys</h1>

```
# This script will generate an API key it outputs the key to console and stores it in the keys directory
> python src/api_key_manager/setup/create_app_key.py user email project_name
```
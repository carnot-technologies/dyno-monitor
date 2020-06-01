![Heroku Dyno Management](https://github.com/carnot-technologies/dyno-monitor/blob/master/heroku.png)

# Heroku Dyno Monitoring & Alerting

**Your Cloudwatch for Heroku.**   
**Monitor dyno errors and performance across all your heroku apps and take automated actions!**

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg?style=flat-square)](https://www.python.org/dev/peps/pep-0008/)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](./LICENSE.md)


## Motivation

This simple python / django application is aimed towards making the post-deployment lifecycle easy and automated for the end users. Here are the main use-cases we came across that motivated us to build this app:

- **Elusive Dyno Level Errors**  
  Certain heroku dyno level errors (`R13`, `R14`, `H12`, `H10`) are not easy to auto-identify as they show up only in application logs and the metrics dashboard of your heroku app. But they heavily impact app performance, so quickly identifying and acting on them can be critical
- **Memory Leaking Applications**  
  Sometimes you may have an app that is occasionally or gradually leaking memory and you do not have the time and / or resources to debug the source of the leak. A quicker fix can be to restart the dyno when its RAM quota exceeds
- **Watchdog**  
  It is important to have a watchdog app that constantly looks at the status of your critical web services, or databases so that you are alerted in case of SOS and automatically takes corrective actions where possible
- **Dyno Metrics**  
  Heroku outputs dyno metrics like `%CPU` and `memory` when you enable them, but we do not get access to the historical data in a queryable format for our own analysis or visualization


## Features

In its final form, the monitoring suite will contain the following:

#### Error Monitoring

- :heavy_check_mark: Monitor and catch **Generic Dyno Errors** (R13, R14 memory errors and other Rxx errors). You can configure the Rxx Error Rules from the admin interface
- :heavy_check_mark: Monitor and catch **Web Specific Dyno Error** (H12, H13, H18 and other Hxx errors). Configuration via admin interface
- :hourglass_flowing_sand: Monitor **Web Dyno Failed Requests** (5xx errors)

#### Alerting

- :heavy_check_mark: **Email alerts** Setup email by entering your SMTP server details and recipients. Then configure your alert rules from the admin dashboard
- :hourglass_flowing_sand: **SMS alerts** Configure SMS alerts by entering your Infobip SMS provider details. If you use some other service (twilio, msg91 etc) you can easily plugin your own implementation

#### Actions

- :heavy_check_mark: **Restart actions** Perform basic recovery actions like dyno restart or app restart when a certain alert is breached

#### Status Checks

- :soon: **Web server** up / down status checks. Specify the *endpoint* to check, *frequency* and *timeout*
- :soon: **Redis instance** availability status checks. Specify *redis url*, *list* name & *threshold* (for list / queue length monitoring if required), *frequency* and *timeout*
- :soon: **Postgres instance** availability status check. Specify the *database url*, *table* name (to check for existence if required), *frequency* and *timeout*

#### Metrics Collection

- :soon: **RAM usage** metric per dyno type. Collection and logging
- :soon: **Load %CPU** per dyno type. Collection and logging

> Metrics Collection only applies to dynos that have metrics logging enabled

## Quick Start

#### Deploy to Heroku

To quickly get started and test the app, you can deploy this application on your heroku account servers. Fill up the pre-requisite environment variables and your app should be up within 5 minutes

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/carnot-technologies/dyno-monitor/tree/master)

- Post deployment, the app creates all the required tables and the superuser account
- It auto-detects all your heroku apps and dynos. This process can take upto a minute depending on the number of apps in your account
- You can then visit your app's admin page at https://<your-app-name>.herokuapp.com/admin/ and start adding `Hxx Error` and `Rxx Error` rules against your dynos

#### Configure the Environment

- Required environment variables
  - `HEROKU_API_KEY` - To access the logs from different heroku apps in your accounts for which alerts have been configured
  - `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` - These three variables are required at the start to create a superuser

- To enable emails, make sure the following environment variables are exported
  ```bash
  heroku config:set ENABLE_EMAILS=1
  heroku config:set EMAIL_HOST=email-server.abc.com --app <YOUR_APP_NAME>
  heroku config:set EMAIL_PORT=587 --app <YOUR_APP_NAME>
  heroku config:set EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxxxxxxx --app <YOUR_APP_NAME>
  heroku config:set EMAIL_HOST_USER=xxxxxxxxxxxxxxxxxxxxx --app <YOUR_APP_NAME>
  heroku config:set SERVER_EMAIL=postmaster@abc.com --app <YOUR_APP_NAME>
  heroku config:set RECIPIENTS=admin.one@abc.com,admin.two@abc.com --app <YOUR_APP_NAME>
  ```

#### Add Rules & Actions

- Login to the admin panel - it will located at `https://<your-app-name>.herokuapp.com/admin/` using the credentials you provided earlier
- You should see the auto-detected `apps` and `dynos` in your heroku account
- You can now add rules. To detect and act on an `R14` error on a certain dyno, add an `Rxx Error`
  - Pick the **dyno** on which you want to apply the error
  - Pick the error **category**. In our case `R14`
  - Enter the **least count** which is the minimum number of occurrences required for the rule to be considered breached, within the **time window** number of seconds
  - Check **email alert** if you want email alerts when this happens (Requires mail to be configured)
  - Pick the **action** to be taken when the alert condition is breached. Possible options are `no-action`, `restart-dyno` and `restart-app`
- Save the rule and you are done! The **log source** and **log dyno** is assigned based on your input dyno type and error category

> For email sending per topic (app + dyno + error category), a cooling period applies which can be configured from the `EMAIL_COOLING_PERIOD_PER_TOPIC` environment variable   
> Also for app restart and dyno restart actions respective cooling periods apply. They can be configured via `APP_RESTART_COOLING_PERIOD` and `DYNO_RESTART_COOLING_PERIOD` respectively

#### Done!



## Configuration and Usage

This is a python / django based application. Broadly you need the following to set it up:
- `Python 3` - we have verified it on Python 3.6
- `virtualenv` - or similar program to create and manage your virtual environment
- `postgres` - access to a small postgres server instance for data logging and storage. RAM required less than 1GB
- `redis` - a small fast-access cache for storing certain details. Less than 25 MB

### Configure the environment

- Setup the virtualenv and install all dependencies
- Much of the application is controlled by its environment variables. A few variables are necessary, others are optional
- Mandatory environment variables

### Initial setup scripts

- WIP




## FAQs

- **Which logs are accessed to extract this info?**
    - Please refer this **[wiki](https://github.com/carnot-technologies/dyno-monitor/wiki/Log-access-and-samples)** on log access method and log samples



## Team

The following members have actively contributed to the source code and this repository:

- **[Pushkar Limaye](https://github.com/pushkar24)**
- **[Juhi Kulkarni](https://github.com/juhi04)**
- **[Prathamesh Joshi](https://github.com/prathamesh1729)**



## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](./LICENSE.md)**
- Copyright (c) 2020 Carnot Technologies Pvt Ltd

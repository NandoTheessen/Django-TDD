Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* pipenv + pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt instasll nginx git python3 pip3 pipenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g. staging.nando.codes

## Systemd service

* see gunicorn.systemd.template.service
* replace variables

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc

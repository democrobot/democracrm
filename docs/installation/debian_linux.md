# Installation Step 1: Debian Linux

Debian Linux is the server operating system that all software for DemocraCRM runs on. It is recommended to have at least
two Debian servers for deployment: (a) one for the application server, and (b) one for the database server, but
everything can be installed on one server if necessary.

The application server(s) will need to be publicly reachable on the Internet via properly configured network access, but
this is currently not addressed in these instructions. Check with your service provider or cloud hosting provider for
support with that.

!!! note

    The following instructions are designed and tested to work on Debian Linux, with current development running on
    **Debian 12.6.x**. Other configurations may work, but are not officially supported at this time.

sudo nano /etc/apt/sources.list
Add Debian Unstable
sudo apt update
sudo apt install python3.12-venv
mkdir venv
sudo apt install -t unstable gdal-bin libgdal-dev
python3 -m venv/crm
source ~/venv/bin/activate
pip install -r requirements/base.txt

When you have your Linux server(s) up and running, the next step is [installing and configuring the database](postgresql_database.md).

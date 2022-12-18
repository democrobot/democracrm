# Installation Step 2: PostgreSQL Database Server

!!! info

    DemocraCRM requires **PostgreSQL 15 or later**. MySQL or other databases are not supported.

## PostgreSQL Server Installation and Configuration

Instead of using the default Ubuntu installation of PostgreSQL, we will be using the packages from the PostgreSQL
repository. Copy the following commands and paste them into a terminal shell on the Ubuntu server that will serve as the
database server:

    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y install postgresql postgis

This will configure Ubuntu to allow it to install and update packages from the PostgreSQL repository, and then perform
the installation of the PostgreSQL server.

Before moving on, copy and paste the below command into a terminal shell to perform a quick verification that
PostgreSQL has been installed successfully:
    
    psql -V

Now that PostgreSQL has been installed, we may need to perform a few configuration changes:

* Timezone changes on the database server
* Listening address(es) on the database server
* Allowed IP addresses from the application server

## DemocraCRM Database Creation and Configuration

The data for the DemocraCRM application will be stored in a PostgreSQL database, but we must first create and configure
that database. Start by switching to the `postgres` user and enter the PostgreSQL CLI:

    sudo -u postgres psql

Copy and paste the following command to create the `democracrm` user. Be sure to change the password within the
quotes before submitting!

    CREATE USER democracrm WITH PASSWORD 'thisisinsecure-pleasechange!';

!!! danger "Create your own secure password"

    **Do not use the password from the above example!** Choose a strong, random password to ensure secure database
    authentication for your DemocraCRM installation, and store a copy of it somewhere safe and secure for reference.

Next, copy and paste the following commands below to create the `democracrm` database, and assign both ownership and
all administrative privileges to the `democracrm` user:

    CREATE DATABASE democracrm WITH OWNER democracrm ENCODING UTF8;
    GRANT ALL PRIVILEGES ON DATABASE democracrm TO democracrm;

!!! note

    The `democracrm` database user is only used by the server for management of the database. All user accounts will
    be created and managed within the DemocraCRM application.

For the final configuration step, connect to the `democracrm` database by copying and pasting the following command:

    \c democracrm

and enable the PostGIS database extension on the `democracrm` database by copying and pasting the following
command:

    CREATE EXTENSION postgis;

If everything went well, you can now disconnect from the database:

    \q

## Configuration Verification

You can verify that the configuration was successful by running the following commands.

First, execute the `psql` command to enter the PostgreSQL CLI with the username you created above. If 
using a remote database, or testing from the application server (which is a good idea to test), replace `localhost`
with your database server's address after the `--host` flag.

    $ psql --username democracrm --password --host localhost democracrm

You'll be prompted for a password next with a prompt like the one below. Type in the one you personally selected when
creating the `democracrm` user above.

    Password for user democracrm:

If successful, you'll be greeted by the PostgreSQL CLI and a `democracrm` prompt, as shown below. This means you are
now in the DemocraCRM database.

    psql (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
    Type "help" for help.
    
    democracrm=> 

To verify the connection details, type the following command:

    \conninfo

If successful, you'll see output similar to the following shown below. Remember that the address could be different
depending on your database server.

    You are connected to database "democracrm" as user "democracrm" on host "localhost" (address "127.0.0.1") at
    port "5432".
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)

Lastly, verify that PostGIS was successfully installed by running:
    
    \dx

You should see `postgis` listed in the output, similar to the following:

                                    List of installed extensions
      Name   | Version |   Schema   |                        Description                         
    ---------+---------+------------+------------------------------------------------------------
     plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
     postgis | 3.3.2   | public     | PostGIS geometry and geography spatial types and functions
    (2 rows)

At this point, your database server is ready! Job well done. You can log out of the database by running:

    \q

The next step is installing the DemocraCRM application server.


## sawtooth-supply-chain app: carmelopz's basic usage instructions with a db tier example:

### Introduction:

- My Hard specs highlights:

    Intel(R) Core Duo CPU E8500  @ 3.16GHz
    RAM: 8Gb

- My Soft specs highlights:

    Kernel version 4.15.10-300.fc27.x86_64 (Fedora 27)
    Docker version 1.13.1
    docker-compose version 1.17.1


### Intructions:

- Go to some directory, such as "/home/user", using any of these commands (all are the same):

```bash
cd
cd  ~ 
cd /home/user
```

- Use sudo or execute as root, to avoid user rights issues:

```bash
sudo git clone https://github.com/carmelopz/sawtooth-supply-chain
cd sawtooth-supply-chain
sudo docker-compose up
```

- Wait until the output stops and/or in a new terminal use this to verify that the 10 containers are up:

```bash
sudo docker ps
```

- Then, we can see the example FishNet supply chain application running. Using any browser on the host:

http://localhost:8022

- As seen below, I have developed a python program to get access to the database tier, using a new container:
- Go to this subdirectory of /sawtooth-supply-chain

```bash
 cd dbtier
```
- We build the image from the Dockerfile which also imports the needed libraries in requirements.txt:

```bash
sudo docker build -t dbtier .
```

- Then, we run the image as a container. Thanks to the --net=host command, the container can connects with the other containers and be available at the host at the same time, without port conflicts.

```bash
sudo docker run --net=host dbtier
```

- We can see the agents record in browser running in the host:

http://localhost:40080

A last note: I have tried this week also to prepare a docker compose with some replicas of the containers, to show how the queries are balance between them. 

Nevertheless, the docker compose yml file of the supply-chain app is in version 2.1, which does not support the "replicas" command and beside this, we have to decide between using the swarm option in docker versus converting the docker-compose.yml to kubernetes, which I think is clearly winning the race versus docker swarm.

I have also tried the open-source converter Kompose:

https://github.com/kubernetes/kompose

In order to translate the sawtooth supply chain yml compose file to kubernetes, but it is not working out of the box.
So both docker swarm and kubernetes will need me some extra time to test this sawtooth application. 

More details below. Thank you so much for reading this.

--- ooOoo ---

![Hyperledger Sawtooth](images/sawtooth_logo_light_blue-small.png)

# Sawtooth Supply Chain

This is a distributed application to help you trace the provenance and other
contextual information of any asset. It can be used as-is or customized for
different use cases. This distributed application runs on top of Hyperledger
Sawtooth, an enterprise blockchain. To learn more about Hyperledger Sawtooth
please see its
[sawtooth-core repo](https://github.com/hyperledger/sawtooth-core) or its
[published docs](https://sawtooth.hyperledger.org/docs/).

## Contents

- [Components](#components)
- [Usage](#usage)
  - [Start Up](#start-up)
  - [Running Scripts in the Shell](#running-scripts-in-the-shell)
  - [Configuring API Keys and Secrets](#configuring-api-keys-and-secrets)
- [Development](#development)
  - [Restarting Components](#restarting-components)
  - [Manually Building Generated Files](#manually-building-generated-files)
- [Documentation](#documentation)
- [License](#license)

## Components

Running alongside the core components from Hyperledger Sawtooth, Supply Chain
includes a number of elements customizing the blockchain and user interaction
with it:

- a **transaction processor** which handles Supply Chain transaction logic
- a **server** which provides an HTTP/JSON API for Supply Chain actions
- a **ledger sync** which syncs blockchain data to a local database
- the **AssetTrack** example client for tracking generic assets
- the **FishNet** example client for tracking fish from catch to table
- a **shell** container with the dependencies to run any commands and scripts


## Usage

This project utilizes [Docker](https://www.docker.com/what-docker) to simplify
dependencies and deployment. After cloning this repo, follow the instructions
specific to your OS to install and run whatever components are required to use
`docker` and `docker-compose` from your command line. This is only dependency
required to run Supply Chain components.

### Start Up

Once Docker is installed and you've cloned this repo, navigate to the root
project directory and run:

```bash
docker-compose up
```

This will take awhile the first time it runs, but when complete will be running
all required components in separate containers. Many of the components will be
available through HTTP endpoints, including:

- The Supply Chain REST API will be at **http://localhost:8020**
- AssetTrack will be at **http://localhost:8021**
- FishNet will be at **http://localhost:8022**
- RethinkDB's admin panel will be available at **http://localhost:8023**
- Sawtooth's blockchain REST API will be available at **http://localhost:8024**

In bash you can shutdown these components with the key combination: `ctrl-C`.
You can shutdown _and_ remove the containers (destroying their data), with the
command:

```bash
docker-compose down
```

### Running Scripts in the Shell

Running `docker-compose up`, will automatically run all scripts necessary to
use all Supply Chain components. However if you want to run any additional
scripts, such as scripts to automatically update sample blockchain data, a shell
container is provided with all necessary dependencies installed. To enter the
shell, simply open a terminal window and run:

```bash
docker exec -it supply-shell bash
```

Once inside the shell, you might try running the one of the update scripts to
see live updates populate in an example web app. First navigate to the server
directory:

```bash
cd server/
```

Then run one of the two provided npm scripts:

```bash
npm run update-sample-assets
npm run update-sample-fish
```

You can customize how many updates are submitted per minute with the `RATE`
environment variable (default 6), and use `LIMIT` to stop the updates after a
certain number are submitted (default 25):

```bash
RATE=3 LIMIT=10 npm run update-sample-assets
```

If you just want to exit the shell, you can simply run:

```bash
exit
```

### Configuring API Keys and Secrets

While the Server runs out of the box with sensible defaults, there are a number
of secrets and API keys which will not be secure unless set explicitly. While
this is fine for demo purposes, any actual deployment set the following
properties:

- **JWT_SECRET**: can be any random string
- **PRIVATE_KEY**: must be 64 random hexadecimal characters
- **MAPS_API_KEY**: provided by [Google Maps](https://developers.google.com/maps/documentation/javascript/get-api-key)

These properties can be set one of two ways, through an environment variable,
or (preferably) by creating a file named `config.json` file in the `server/`
directory. A file named `config.json.example` is provided which should provide
a template to follow.

## Development

### Restarting Components

The default Docker containers use the `volumes` command to link directly to the
source code on your host machine. As a result any changes you make will
immediately be reflected in Supply Chain components without having to rebuild
them. However, typically you _will_ have to restart a component before it can
take advantage of any changes. Rather than restarting every container, you can
restart a single component from separate terminal using the container name. For
example:

```bash
docker restart supply-server
```

The available container names include:
- supply-shell
- supply-processor
- supply-server
- supply-asset-client
- supply-fish-client
- supply-rethink
- supply-validator
- supply-settings-tp
- supply-rest-api

### Manually Building Generated Files

Files in the `protos/` directory are used to generate classes for other
components. This is done automatically on `up`, but if you make changes to
these files and wish to rebuild the generated files immediately, you can do so
from within the Supply Chain Shell:

```bash
docker exec -it supply-shell bash
```

Once in the shell, you can generate the necessary Python classes simply by
running:

```bash
protogen
```

For the example clients, in addition to rebuilding them on Protobuf changes,
any changes to their source code will require their static files be rebuilt.
However, their containers do _not_ typically need to be restarted in order to
reflect changes, just rebuild the static files and refresh your browser (the
browser cache may have to be emptied):

```bash
cd asset_client/
npm run build
```

```bash
cd fish_client/
npm run build
```

## Documentation

The latest documentation for Sawtooth Supply Chain is available within this
repo in the [docs](docs) subdirectory.

## License

Hyperledger Sawtooth software is licensed under the
[Apache License Version 2.0](LICENSE) software license.

Hyperledger Sawtooth Supply Chain documentation in the [docs](docs)
subdirectory is licensed under a Creative Commons Attribution 4.0 International
License.  You may obtain a copy of the license at:
http://creativecommons.org/licenses/by/4.0/.

![Open Source Award Badge](images/rookies16-small.png)

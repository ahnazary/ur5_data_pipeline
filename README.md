# Run the project

To run the project, follow these steps:


### Create the database

```bash
docker-compose up --build -d
```

This will start a postgres database which will be used to store angles.

### Setup MQTT broker

Using MacOS, you can install and run mosquitto using brew.

```bash
brew install mosquitto
brew services start mosquitto
```

### install python dependencies

```bash
pip install -r requirements.txt
```

### start the publisher

```bash
python publish_angles.py
```

This script will publish random angles to the MQTT broker every 0.1 seconds.

### start the reader

```bash
python read_angles.py
```

This script will read the angles from the MQTT broker. On exit, the script will dump the angles into a postgres database and local csv file. If AWS S3 credentials are provided (by setting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables), the script will also upload the csv file to an S3 bucket.


# stop the project and clean up

To stop the project, you can use docker-compose with the following command:

```bash
docker-compose down --rmi all
```

### Setup mosquitto on macOS

If you are using using macOS, you can install and run mosquitto using brew.

```bash
brew install mosquitto#
brew services start mosquitto
```

or restart it using

```bash
brew services restart mosquitto
```


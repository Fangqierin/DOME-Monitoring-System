# DOME - Dashboard

### Description

Front-end of dashboard for dome project

### Usage

Run `npm install` to get all dependencies

Run `npm start` to serve the app locally



Edit `util/config.js` to enable fake data if you don't have mongodb/server set up.


##### Start from an empty database
> * Create a database named dome
> * Create collections: air, weather, waypoints, grids, images
> * Use `client_script` and create json files in input_folder from the template and publish to mongodb using `zmq_publisher`
> * Or you can manually add the data using `mongodb compass`, below are the example data.
> 
air
```json
{
  "_id": {
    "$oid": "64092e66ce5bb5e08125ae7c"
  },
  "filename": "air2.json",
  "data": "{\r\n\"timestamp\": \"10:23:26\",\r\n\"pm2.5\": 11,\r\n\"pm10\": 45\r\n}"
}

```

weather
```json
{
  "_id": {
    "$oid": "64092fbfce5bb5e08125ae7d"
  },
  "filename": "weather1.json",
  "data": "{\r\n  \"timestamp\": \"10:23:26\",\r\n  \"temperature\": 21,\r\n  \"humidity\": 21.38,\r\n  \"dew_point\": 18.18,\r\n  \"light\": 95.14,\r\n  \"pressure\": 956.6,\r\n  \"wind_speed\": 54,\r\n  \"rain\": 0\r\n}"
}
```

grids
```json
{
  "_id": {
    "$oid": "64093393680d04a886a8f4bf"
  },
  "filename": "grids1.json",
  "data": "{\r\n    \"location\": {\"x\": 0, \"y\": -25, \"z\": 110},\r\n    \"fires\": [\r\n        {\"fx\": -29, \"fy\": 0, \"fw\": 3, \"fh\": 4},\r\n        {\"fx\": -27, \"fy\": -19, \"fw\": 4, \"fh\": 3},\r\n        {\"fx\": 16, \"fy\": 1, \"fw\": 3, \"fh\": 4}\r\n    ],\r\n    \"time\": \"20:52:44\"\r\n}\r\n"
}
```

images
```json
{
  "_id": {
    "$oid": "6403c3a604e5195e39ce7a55"
  },
  "filename": "logo192.jpg",
  "filepath": "images\\logo192.jpg"
}
```

waypoints
```json
{
  "_id": {
    "$oid": "640939474e9159a407825a61"
  },
  "x": 1,
  "y": 2,
  "z": 3,
  "read": 0
}
```

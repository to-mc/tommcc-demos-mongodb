# GRAPH

---
## Setup - Once

__1. Configure Atlas Environment__
* Log-on to your [Atlas account](http://cloud.mongodb.com) (using the MongoDB SA preallocated Atlas credits system) and navigate to your SA project
* In the project's Security tab, choose to add a new user called __main_user__, and for __User Privileges__ specify __Read and write to any database__ (make a note of the password you specify)
* Create an __M10__ based 3 node replica-set in a single AWS region of your choice with default settings
* In the Security tab, add a new __IP Whitelist__ for your laptop's current IP address
* In the Atlas console, for the database cluster you deployed, click the __Connect button__, select __Connect Your Application__, and for the __Node.js 2.12 or later version only__  (the SRV connection string is not supported by the citibike server code) copy the __Connection String Only__ - make a note of this MongoDB URL address to subsequently be used in the _Execution_ section

__2. Configure Laptop__
* Ensure MongoDB version 3.6+ is already installed your laptop, mainly to enable MongoDB command line tools to be used (no MongoDB databases will be run on the laptop for this proof)
* [Download](https://www.mongodb.com/download-center/compass) and install Compass on your laptop
* Ensure Node (version 6+) and NPM are installed your laptop
* Edit the file ```server/app.js``` file and replace the hosts part of the value of the  ```const uri``` with the host part of Node.js Connection String you recorded earlier (ensure you replace **\<password\>** with the password you configured earlier and also for the DB part of the URL, change __test__ to __citibike__ and also ensure the __replicaSet__ part of the URL is correct), similar to:
```js 
const uri='mongodb://main-user:MyPassword@testcluster-shard-00-00-abcde.mongodb.net:27017,testcluster-shard-00-01-abcde.mongodb.net:27017,testcluster-shard-00-02-abcde.mongodb.net:27017/citibike?ssl=true&replicaSet=testcluster-shard-0&authSource=admin';
```

_Note_: be careful to point to __citibike__ database in the above URI, missing this will fail to display points on the map

__3. Load Citibikes Data Set Into A Database In The Atlas Cluster__
* Unpack the file ``citibikes_data.tgz`` (or ``citibikes.zip`` if using MS Windows) in the base folder of this proof (this should create the ``dump`` sub-folder containing _bson_ files
* In the Atlas console, for the deployed cluster, select __.../Command Line Tools__ and in the shown section __Binary Import and Export Tools__ copy and record the __--host__ parameter value for use in the next step (this is required because mongorestore cannot use a _SRV_ style connection string)
* Via a terminal/shell, from the base directory of the proof, run the following MongoDB import command to restore the _stations_ and _rides_ collections (and indexes) into a database called _citibike_, similar to the following, changing the __--host__ field value to the one you captured in the previous step and changing the password accordingly):
  ```bash
  mongorestore --uri "mongodb+srv://${ATLAS_USER}:${ATLAS_PASS}@${ATLAS_CLUSTER_HOSTNAME}"  -d GEOSPATIAL --dir dump
  ```


## Setup - Every time


__1. Start Node Server and Client Parts of the Application__
* In a new terminal/shell, from the ``server`` sub-folder run the following commands to pull in the required Node.js dependency libraries and then start the server part of the application:
  ```bash
  npm install
  npm start
  ```
* In a separate new terminal/shell, from the ``client`` sub-folder run the following commands to pull in the required Node.js dependency libraries and then start the client part of the application:
  ```bash
  npm install
  npm start
  ```


---
## Execution

__TEST 1: Graph Lookup Using the Visual Node.js Application__
* Using a web browser, connect to Node client application at: http://localhost:8080 . This shows a map of New York, with data pulled from the _citibike_ database showing the location of all the _bike stations_ The map can be zoomed in or out by scrolling the mouse, and moved in all directions by dragging. Each time the map is moved, the Node.js application reruns its query to update the graphics (be aware that queries stack and may take several seconds to execute - if it lags too much ```refresh```the browser page). At this point, all that the Node.js application is demonstrating is general MongoDB aggregation capabilities using _faceted searches_.  Clicking on **"show query"** will display the aggregation pipeline executed to display the graphics, as show in the screenshot below. 

![query](img/query.png "query")

&nbsp;&nbsp;&nbsp;_Note:_ Clicking on **"show"** switches back to graphics view, clicking on "home" brings you back to home map.

* To prove the __graph capability__, **click on a station on the map**, which will display the station's statistics, plus the last 3 bikes that passed by as shown in the screenshot below:

![station](img/station.png "station")

* Click on a **bike** to see the path the bike has gone on from station to station, starting at the highlighted station. To generate these visual paths, the Node.js application has executed an aggregation containing a __graph lookup__ stage to walk the linked list of _rides_ records that the bike has been on for a specific day. The visual result displayed will be similar to the screenshot below:

![path](img/path.png "path")

* Click on **Show Query** to display the aggregation pipeline that was constructed by the Node.js application - here you will see the exact __$graphLookup__ stage that was executed against the _stations_ and _rides_ collections to traverse and find all the linked journeys for the bike for the day:

![pipeline](img/pipeline.png "pipeline")

__TEST 2: Graph Lookup Using the Shell__
* In the Atlas console, for the database cluster you deployed, click the __Connect button__, select __Connect with the Mongo Shell__, and in the __Run your connection string in your command line__ section copy the connection command line
* In a new terminal/shell, launch the Mongo Shell against the Atlas database, using the copied command line and entering the password when prompted, for example:
   ```
   mongo "mongodb+srv://test-clusterabcde.mongodb.net/test" --username main_user
   ```
* From the Shell you will build and then execute an aggregation pipeline which, for the starting station _3221_ (_47 Ave & 31 St_), and for bike number _7998_ uses a ``$graphLookup`` aggregation stage to traverse the __rides__ collection for the specific bike, _walking_ the linked rides (the _end station_ in one record will link to the _start station_ in another record) that the bike has been on, on 25-March-2016, showing the result of each ride in order, with how long the ride took. In the Shell, __copy and paste__ the JavaScript excerpt shown below which defines each aggregation stage as a variable, for the sake of readability, before executing the combined pipeline of stages:
```js
match= {  
      $match:{  
         _id: 3221
      }
   }
   
graph= {  
      $graphLookup:{  
         from: "rides",
         startWith: "$_id",
         connectToField: "startStation._id",
         connectFromField: "endStation._id",
         as: "bikePath",
         restrictSearchWithMatch:{  
            bike: 17998,
            "time.0": {$gte:ISODate('2016-03-25'),$lt:ISODate('2016-03-26')}
         }
      }
   }

unwind= {  
      $unwind:"$bikePath"
   }

sort= {  
      $sort:{  
         "bikePath.time":1
      }
   }

project= {
      $project:{
         _id: 0,
         bike: "$bikePath.bike",
         duration_mins: {$toInt: {$divide: ["$bikePath.duration", 60000]}},
         timesRide: "$bikePath.time",
         startStation: "$bikePath.startStation.name",
         endStation: "$bikePath.endStation.name"
      }
   }

use citibike
db.stations.aggregate([match,graph,unwind,sort,project]).pretty()
```


---
## Measurement

For __TEST 1__, the visual output should show a linked set of rides for the bike from the starting station, onwards to other stations, and the generated aggregation pipeline that was executed (including the _graph lookup_ stage) should be displayed, as shown in the screenshot below:

![visualresult](img/visualresult.png "visualresult")

For __TEST 2__, the Shell output of running the _graph lookup_ based aggregation pipeline should list a series of rides for the bike, from the starting station onwards through other stations, matching the output shown below:
```js
{
	"bike" : 17998,
	"duration_mins" : 24,
	"timesRide" : [
		ISODate("2016-03-25T10:55:17Z"),
		ISODate("2016-03-25T11:19:30Z")
	],
	"startStation" : "47 Ave & 31 St",
	"endStation" : "Kent Ave & N 7 St"
}
{
	"bike" : 17998,
	"duration_mins" : 17,
	"timesRide" : [
		ISODate("2016-03-25T12:02:39Z"),
		ISODate("2016-03-25T12:20:22Z")
	],
	"startStation" : "Kent Ave & N 7 St",
	"endStation" : "Emerson Pl & Myrtle Ave"
}
{
	"bike" : 17998,
	"duration_mins" : 10,
	"timesRide" : [
		ISODate("2016-03-25T14:52:39Z"),
		ISODate("2016-03-25T15:03:17Z")
	],
	"startStation" : "Emerson Pl & Myrtle Ave",
	"endStation" : "Johnson St & Gold St"
}
{
	"bike" : 17998,
	"duration_mins" : 6,
	"timesRide" : [
		ISODate("2016-03-25T17:25:13Z"),
		ISODate("2016-03-25T17:31:45Z")
	],
	"startStation" : "Johnson St & Gold St",
	"endStation" : "State St & Smith St"
}

```


# LoopSim
Workflow Framework for Closed-Loop Neuromodulation Control Systems


# Configuring LoopSim

LoopSim is built with is Python-3.7.

## Install Dependencies

$ pip3 install beautifulsoup4

$ pip3 install lxml


## Run Parser
Design a workflow in yEd using yEd's _Shape Nodes_ and their own connectors. Make sure to label all the nodes and edges when you create the graph in yEd. Otherwise, the parser will fail.

Once you have the workflow designed with yEd and saved as a graphml file, you can run the below to parse it into a python dictionary.

Change the line in the GraphParser.py to your reflect your graphml file. By default, it is,

GRAPHML_FILE = "testhg.graphml"

$ python3 GraphParser.py 

Some sample graphs are provided in the graphs folder. 

![Sampple Workflow](https://raw.githubusercontent.com/NISYSLAB/LoopSim/main/docs/testhg.jpg)

The internal LoopSim representation and output format for the above workflow is:

{'U2': ['PM2:pm2.py', ['PM1:pm1.py', 'C:c.py']], 'U1': ['PM1:pm1.py', ['PM2:pm2.py', 'C:c.py']], 'V1': ['C:c.py', ['PM1:pm1.py']], 'V2': ['C:c.py', ['PM2:pm2.py']]}

LoopSim stores the graph internally as a dictionary of edges, with each key representing an edge label and their respective values representing an array of length 2, composed of the source and destination node labels (i.e., the nodes connected by the edge). The destination entry itself is an array as each edge can start from a single source and connect one more destination nodes. As such, LoopSim represents the workflows as a directed hypergraph internally.

Format:
 
edge = [src_node, [dest_nodes]]


# Running LoopSim


Perform Git clone if this is the first time you are configuring LoopSim

$ git clone https://github.com/NISYSLAB/LoopSim.git

Go to the LoopSim folder.

$ cd LoopSim

First build the Docker Container of the Mediator.

$ git pull

$ docker build -t mediator .

If this is the first execution,

$ nohup docker run --name mediator  -p 80:8081 mediator > loopsim.out &

Otherwise,

$ docker stop mediator

$ docker rm mediator

$ nohup docker run --name mediator  -p 80:8081 mediator > loopsim.out &

Check the Server logs.

$ docker logs -f mediator


# Run the clients: CTL and PM.

Run the controller (CTL and CW). This is currently just a python class functioning as CW with a dummy CTL in it.

CW must be run first as it holds the init() that invokes the POST /init/.

$ cd CM

$ python CW.py

$ tail -f u

Run the PM (PM and PW). This is currently just a python class functioning as PW with a dummy PM in it.

$ cd PM

$ python PW.py

$ tail -f ym

The ordering above does not matter.

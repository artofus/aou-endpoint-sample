# Prerequisites

1.	An existing instance running in the cloud (e.g. ubuntu)
2.	Git installed in that instance
3.	Docker installed in that instance

# How to build

1.	Clone the code from the public repository ‘artofus/h2-endpoint-sample’ onto your cloud instance (e.g. git clone https://github.com/artofus/h2-endpoint-sample)
2.	Go into the root of the cloned repository
3.	Build with docker (e.g. docker build . -f Dockerfile -t local/h2-endpoint-sample:public)
4.	The docker image should be now in your local registry

# How to run

Run one of the following commands
a.	HTTP: docker run -p 80:80 --rm -it local/h2-endpoint-sample:public
b.	HTTPS: docker run -p 443:443 --rm -v {full path to public certificate on your local machine}:/endpoint/cert/server.crt -v {full path to private certificate on your local machine}:/endpoint/cert/server.key -it local/h2-endpoint-sample:public

# How to test

This assumes your instance is HTTP.

1.	Retrieve the public IP of your cloud instance
2.	Open the following URL in Chrome http://{INSTANCE_IP}/subscribe where INSTANCE_IP is the public IP of your cloud instance
3.	Run the following from another machine
  curl -v -k POST http://{INSTANCE_IP}/observations  -H "Content-Type: application/json" -H "Connection: keep-alive" -d "@{path to git repo}\test\observations\sample001.txt"
4.	Observe these events in the Chrome browser

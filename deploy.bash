# stops, removes and builds an image for BP
# runs the container on port 5001

sudo docker container stop rnamigos
sudo docker container rm rnamigos 

sudo docker build -t rnamigos .
sudo docker run -p 5003:5003 -d -t --restart on-failure --network=PipelineNetwork  --name rnamigos rnamigos 

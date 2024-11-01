# leaky
minimum reproduction of memory leak


## instructions
after cloning this repo, copy your favorite transfoemrs model from hugging face into a local models/ folder within the repo.
```
git clone https://github.com/jdchmiel/leaky.git
cd leaky
mkdir model
sudo apt-get install git-lfs
git lfs install
cd model
git clone https://huggingface.co/dunzhang/stella_en_400M_v5 .
rm -rf .git
cd ..
```

- extra steps mentioned above may not be necessary depending on how you want to collect a model. removing the .git folder saves a few gigs
- a 'real' image would have model added to the image to be a single artifact to move around environments. this sample we will mount the model folders in order to convert a single time and more easily swap which model is mounted to the running container.

## adjust model config to work on cpu
Stella seems to be built for a GPU so to get around it, some execution paths obey use_memory_efficient_attention=False but the surefire way is to edit mode/config.json
```
 "unpad_inputs": false,
 "use_memory_efficient_attention": false,
```
ensure the 'true' is changed to 'false' before continuing or you will get errors about installing xformers, which become a ~9g image as it drags in cuda



## build the container
docker buildx build --no-cache -f Dockerfile -t leaky:latest .

## single time convert the model to ov
docker run -it --rm \
    -v ./model:/model \
    -v ./model_ov:/model_ov \
    -network leaky \
    leaky:latest python3 /app/convert_to_ov.py 


## run the converted openvino model in seldon-core, this mode leaks memory
port 9000 is not free so use 9999 outside the container

docker run -it --rm -v ./model_ov:/model_ov -p 9999:9000 -p 6000:6000  -network leaky leaky:latest seldon-core-microservice run_ov --service-type MODEL


## run the converted model in seldon core in a way that does not leak memory over REST
we have to add in port 5000 for the gRPC process.  I also add a memory limit of 2500 megs which you can tweak up or down if you have a larger or smaller model.
For stella this seems to allow about 1000 leaky invcations or to be stable with non leaky REST 
```
docker run -it --rm \
    -v ./model_ov:/model_ov \
    -p 9999:9000 \
    -p 6000:6000 \
    -p 5000:5000 \
     --memory 2500m \
    -e SELDON_DEBUG=1 \
    -e FLASK_SINGLE_THREADED=1 \
    leaky:latest seldon-core-microservice run_ov --service-type MODEL
```


## observe the container memory usage
use your choice of memory profiling tools. A simple one is `docker stats`

## to loop over some phrases you can run this in another shell for REST invocations
`pip install httpx`
`python3 external_calls.py`
observe in `docker stats` the memory usgae grow as requests are made, but stay flat when no requests come through.  Also observe a single core is used



## to run the model in the container
running the model in the container you can use the wrapper internal_calls.py
`docker run -it --rm -v ./model_ov:/model_ov  leaky:latest python3 internal_calls.py`
observe in `docker stats` that the memory use stays flat after the initial model load, and that all cores are used.


## run the converted model in seldon core in a way that does not leak memory over REST but still leaks in gRPC
we have to add in port 5000 for the gRPC process.  I also add a memory limit of 2500 megs which you can tweak up or down if you have a larger or smaller model.
For stella this seems to allow about 1000 leaky invcations or to be stable with non leaky REST 
```
docker run -it --rm -v ./model_ov:/model_ov -p 9999:9000 -p 6000:6000 -p 5000:5000  --memory 2500m -e SELDON_DEBUG=1 -e FLASK_SINGLE_THREADED=1 leaky:latest seldon-core-microservice run_ov --service-type MODEL
```
use the same external_calls.py from above and ovserve that now all cores are used and memory usage is flat with no growth.

## use gRPC to show it always leaks
you can install seldon core outside of the container to use the seldon client. You could run it in the container where it is already installed 
but then you need to ensure the network connectivity from one container to another without docker compser or the like.
```
pip install seldon-core
python3 external_grpc.py
```
you should see in your other terminal `docker stats` shoing memory leak no matter how you run the model







# Coming soon
- completing the run_st wrapper to execute the non converted model and see the leak / cores status of it
- test using the nodejs transformers.js method to wrap a model ?


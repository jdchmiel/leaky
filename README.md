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
    leaky:latest python3 /app/convert_to_ov.py 


## run the converted openvino model in seldon-core
port 9000 is not free so use 9999 outside the container

docker run -it --rm -v ./model_ov:/model_ov -p 9999:9000 -p 6000:6000  leaky:latest seldon-core-microservice run_ov --service-type MODEL


## observe the container memory usage
use your choice of memory profiling tools. A simple one is `docker stats`

## to loop over some phrases you can run this in another shell
`pip install httpx`
`python3 external_calls.py`
observe in `docker stats` the memory usgae grow as requests are made, but stay flat when no requests come through.  Also observe a single core is used

## to run the model in the container
running the model in the container you can use the wrapper internal_calls.py
`docker run -it --rm -v ./model_ov:/model_ov  leaky:latest python3 internal_calls.py`
observe in `docker stats` that the memory use stays flat after the initial model load, and that all cores are used.




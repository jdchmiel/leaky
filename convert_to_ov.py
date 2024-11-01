
from optimum.intel import OVSentenceTransformer as OV

model = OV.from_pretrained('/model',
    export=True,
    trust_remote_code=True,
    repo_type="local",
    cache_folder='/model',
    #config_kwargs={"use_memory_efficient_attention":None, "unpad_inputs":False},  #needed for Stella and cpu, remove line for cuda
    #load_in_8bit=True, # 8 bit int, use independently of half() for quantized mode, 2x-8x faster some CPUs
    local_files_only=True,
).half() # half means convert to fp16
model.save_pretrained('/model_fp16')

model = OV.from_pretrained('/model',
    export=True,
    trust_remote_code=True,
    repo_type="local",
    cache_folder='/model',
    #config_kwargs={"use_memory_efficient_attention":None, "unpad_inputs":False},  #needed for Stella and cpu, remove line for cuda
    load_in_8bit=True, # 8 bit int, use independently of half() for quantized mode, 2x-8x faster some CPUs
    local_files_only=True,
)
model.save_pretrained('/model_int8')





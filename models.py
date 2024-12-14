import torch
from diffusers import StableDiffusionPipeline

stable_diffusion_pipeline = StableDiffusionPipeline.from_pretrained(
    "segmind/small-sd",
    torch_dtype=torch.float16,
    allow_pickle=False
)

pipeline = stable_diffusion_pipeline.to('cuda')

pipeline.enable_attention_slicing()
pipeline.enable_sequential_cpu_offload() 
pipeline.enable_model_cpu_offload() 
pipeline.unet.to(memory_format=torch.channels_last)  
torch.cuda.empty_cache()  
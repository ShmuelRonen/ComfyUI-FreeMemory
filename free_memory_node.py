import torch
import gc
import psutil
import os
import ctypes
import comfy.model_management as mm

class FreeMemoryBase:
    def free_memory(self, aggressive=False):
        print("Attempting to free GPU VRAM and system RAM...")
        self.free_gpu_vram(aggressive)
        self.free_system_ram(aggressive)

    def free_gpu_vram(self, aggressive):
        if torch.cuda.is_available():
            initial_memory = torch.cuda.memory_allocated()
            
            if aggressive:
                mm.unload_all_models()
                mm.soft_empty_cache()
            
            torch.cuda.empty_cache()
            
            final_memory = torch.cuda.memory_allocated()
            memory_freed = initial_memory - final_memory
            print(f"GPU VRAM: Initial usage: {initial_memory/1e9:.2f} GB, "
                  f"Final usage: {final_memory/1e9:.2f} GB, "
                  f"Freed: {memory_freed/1e9:.2f} GB")
        else:
            print("CUDA is not available. No GPU VRAM to free.")

    def free_system_ram(self, aggressive):
        initial_memory = psutil.virtual_memory().percent
        
        collected = gc.collect()
        print(f"Garbage collector: collected {collected} objects.")

        if aggressive:
            if os.name == 'posix':  # Unix/Linux
                try:
                    os.system('sync')
                    with open('/proc/sys/vm/drop_caches', 'w') as f:
                        f.write('3')
                    print("Cleared system caches on Linux.")
                except Exception as e:
                    print(f"Failed to clear system caches on Linux: {str(e)}")
            elif os.name == 'nt':  # Windows
                try:
                    ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
                    print("Attempted to clear working set on Windows.")
                except Exception as e:
                    print(f"Failed to clear working set on Windows: {str(e)}")

        final_memory = psutil.virtual_memory().percent
        memory_freed = initial_memory - final_memory
        print(f"System RAM: Initial usage: {initial_memory:.2f}%, "
              f"Final usage: {final_memory:.2f}%, "
              f"Freed: {memory_freed:.2f}%")

class FreeMemoryImage(FreeMemoryBase):
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE",),
            "aggressive": ("BOOLEAN", {"default": False})
        }}
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "free_memory_image"
    CATEGORY = "Memory Management"

    def free_memory_image(self, image, aggressive):
        self.free_memory(aggressive)
        return (image,)

class FreeMemoryLatent(FreeMemoryBase):
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "latent": ("LATENT",),
            "aggressive": ("BOOLEAN", {"default": False})
        }}
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "free_memory_latent"
    CATEGORY = "Memory Management"

    def free_memory_latent(self, latent, aggressive):
        self.free_memory(aggressive)
        return (latent,)

class FreeMemoryModel(FreeMemoryBase):
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model": ("MODEL",),
            "aggressive": ("BOOLEAN", {"default": False})
        }}
    
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "free_memory_model"
    CATEGORY = "Memory Management"

    def free_memory_model(self, model, aggressive):
        self.free_memory(aggressive)
        return (model,)

NODE_CLASS_MAPPINGS = {
    "FreeMemoryImage": FreeMemoryImage,
    "FreeMemoryLatent": FreeMemoryLatent,
    "FreeMemoryModel": FreeMemoryModel,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FreeMemoryImage": "Free Memory (Image)",
    "FreeMemoryLatent": "Free Memory (Latent)",
    "FreeMemoryModel": "Free Memory (Model)",
}
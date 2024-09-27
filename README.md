# ComfyUI-FreeMemory

ComfyUI-FreeMemory is a custom node extension for ComfyUI that provides advanced memory management capabilities within your image generation workflows.

![image](https://github.com/user-attachments/assets/7ac0e896-1b6b-42b0-a729-ed318cae91f5)


## Features

- Three specialized nodes for freeing memory:
  1. Free Memory (Image): Cleans up memory while passing through image data
  2. Free Memory (Latent): Cleans up memory while passing through latent data
  3. Free Memory (Model): Cleans up memory while passing through model data

- Attempts to free both GPU VRAM and system RAM
- Compatible with both Windows and Linux systems
- Seamlessly integrates into existing ComfyUI workflows

## Usage

Insert these nodes at strategic points in your workflow to free up memory, potentially allowing for larger batch sizes or more complex operations without running out of resources.

## Installation

1. Clone this repository into your ComfyUI `custom_nodes` directory:
   ```
   git clone https://github.com/your-username/ComfyUI-FreeMemory.git
   ```
2. Install the required `psutil` library:
   ```
   pip install psutil
   ```
3. Restart ComfyUI or reload custom nodes

## Technical Details

The ComfyUI-FreeMemory nodes employ several techniques to free up memory:

### GPU VRAM Cleaning

1. **CUDA Cache Clearing**: The node uses `torch.cuda.empty_cache()` to free up CUDA memory that is no longer being used by PyTorch but hasn't been released back to the system. This can help reduce fragmentation and free up contiguous blocks of memory.

2. **Memory Usage Reporting**: The node reports the initial and final GPU VRAM usage, as well as the amount freed, providing visibility into the cleaning process.

### System RAM Cleaning

1. **Garbage Collection**: The node triggers Python's garbage collector using `gc.collect()`. This process identifies and frees memory from objects that are no longer in use by the Python runtime.

2. **Operating System-Specific Operations**:
   - On Linux:
     - Executes `sync` to flush file system buffers.
     - Writes to `/proc/sys/vm/drop_caches` to clear pagecache, dentries, and inodes. This operation requires root privileges and may not work in all environments.
   - On Windows:
     - Calls `EmptyWorkingSet` from the Windows API to attempt to reduce the working set size of the current process.

3. **Memory Usage Reporting**: Similar to GPU VRAM, the node reports on system RAM usage before and after the cleaning process.

### Limitations and Considerations

- The effectiveness of memory cleaning can vary depending on the specific state of your system and the nature of your ComfyUI workflow.
- Clearing caches may temporarily slow down operations as caches need to be rebuilt.
- Some cleaning operations, particularly on Linux, may require elevated privileges to be fully effective.
- While these nodes can help manage memory usage, they do not guarantee prevention of out-of-memory errors in all scenarios. They should be used as part of a broader strategy for optimizing your workflows.

## How It Works

When a FreeMemory node is executed in your ComfyUI workflow:

1. It first attempts to free GPU VRAM by clearing the CUDA cache.
2. It then runs the Python garbage collector to free up unused Python objects.
3. Depending on the operating system, it performs additional steps to clear system caches.
4. Throughout the process, it reports on the memory usage and amount freed.
5. Finally, it passes through the input data (image, latent, or model) unchanged, allowing your workflow to continue.

By strategically placing these nodes in your workflow, you can potentially prevent out-of-memory errors and allow for more complex operations or larger batch sizes.

## Contributing

Contributions to improve the efficiency or expand the capabilities of the ComfyUI-FreeMemory nodes are welcome. Please feel free to submit issues or pull requests.

## License

[MIT License](LICENSE)

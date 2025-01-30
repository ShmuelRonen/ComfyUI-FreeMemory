# ComfyUI-FreeMemory

ComfyUI-FreeMemory is a custom node extension for ComfyUI that provides advanced memory management capabilities within your image generation workflows. It aims to help prevent out-of-memory errors and optimize resource usage during complex operations.

![image](https://github.com/user-attachments/assets/4d4f464e-86e9-413b-b227-9078cc01a588)


## Features

- Four specialized nodes for freeing memory:
  1. **Free Memory (Image)**: Cleans up memory while passing through image data
  2. **Free Memory (Latent)**: Cleans up memory while passing through latent data
  3. **Free Memory (Model)**: Cleans up memory while passing through model data
  4. **Free Memory (CLIP)**: Cleans up memory while passing through Clip model data
  5. **Free Memory (String)**: Cleans up memory while passing through String model data

- Attempts to free both GPU VRAM and system RAM
- Compatible with both Windows and Linux systems
- Seamlessly integrates into existing ComfyUI workflows
- Includes an "aggressive" mode for more thorough memory cleaning

## Installation

1. Clone this repository into your ComfyUI `custom_nodes` directory:
   ```
   git clone https://github.com/ShmuelRonen/ComfyUI-FreeMemory.git
   ```
2. Install the required `psutil` library:
   ```
   pip install psutil
   ```
3. Restart ComfyUI or reload custom nodes

## Usage

Insert these nodes at strategic points in your workflow to free up memory. This can potentially allow for larger batch sizes or more complex operations without running out of resources.

### Basic Usage
1. Add a FreeMemory node (Image, Latent, Model, or CLIP) to your workflow.
2. Connect the appropriate input (image, latent, model, or CLIP) to the node.
3. Connect the output to the next step in your workflow.

### Aggressive Mode
Each node includes an "aggressive" boolean input:
1. Set to `False` (default) for standard memory cleaning.
2. Set to `True` for more thorough, aggressive memory cleaning.

## How It Works

When a FreeMemory node is executed:

1. It checks the "aggressive" flag to determine the cleaning intensity.
2. For GPU VRAM:
   - In aggressive mode, it unloads all models and performs a soft cache empty.
   - It then clears the CUDA cache (in both normal and aggressive modes).
3. For System RAM:
   - It runs the Python garbage collector.
   - In aggressive mode, it performs additional system-specific cleaning operations.
4. It reports on the memory usage and amount freed.
5. Finally, it passes through the input data unchanged, allowing your workflow to continue.

## Technical Details

### GPU VRAM Cleaning

1. **Standard Mode**: Uses `torch.cuda.empty_cache()` to free up CUDA memory that is no longer being used by PyTorch but hasn't been released back to the system.
2. **Aggressive Mode**: 
   - Unloads all models using `comfy.model_management.unload_all_models()`
   - Performs a soft cache empty with `comfy.model_management.soft_empty_cache()`
   - Follows with `torch.cuda.empty_cache()`

### System RAM Cleaning

1. **Garbage Collection**: Triggers Python's garbage collector using `gc.collect()`.
2. **Aggressive Mode - OS-Specific Operations**:
   - On Linux:
     - Executes `sync` to flush file system buffers.
     - Writes to `/proc/sys/vm/drop_caches` to clear pagecache, dentries, and inodes.
   - On Windows:
     - Calls `EmptyWorkingSet` from the Windows API to reduce the working set size of the current process.

### Memory Usage Reporting

The nodes report on initial and final memory usage for both GPU VRAM and system RAM, providing visibility into the cleaning process.

## Limitations and Considerations

- The effectiveness of memory cleaning can vary depending on your system's state and workflow nature.
- Aggressive mode may temporarily slow down operations as caches need to be rebuilt and models reloaded.
- Some cleaning operations, particularly on Linux, may require elevated privileges to be fully effective.
- These nodes help manage memory but don't guarantee prevention of all out-of-memory errors.

## Contributing

Contributions to improve efficiency or expand capabilities are welcome. Please feel free to submit issues or pull requests.

## License

[MIT License](LICENSE)

---

For more information or support, please open an issue on the GitHub repository.

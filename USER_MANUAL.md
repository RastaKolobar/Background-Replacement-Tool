# Background Replacement Tool - User Manual

**Author**: Radko Yordanov

Complete guide to using all features and options of the background replacement tool.

---

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Basic Usage](#basic-usage)
4. [Background Options](#background-options)
5. [AI Model Selection](#ai-model-selection)
6. [Output Format Options](#output-format-options)
7. [Image Resizing](#image-resizing)
8. [Color Filters](#color-filters)
9. [Image Enhancements](#image-enhancements)
10. [Web Optimization](#web-optimization)
11. [Batch Processing](#batch-processing)
12. [Advanced Features](#advanced-features)
13. [Professional Workflows](#professional-workflows)
14. [Tips & Best Practices](#tips--best-practices)

---

## Installation

### System Requirements

**Minimum Requirements:**
- Python 3.7 or higher
- 2GB RAM
- 500MB free disk space (for dependencies and AI models)
- Internet connection (for initial model download)

**Recommended:**
- Python 3.10 or higher
- 4GB RAM
- 1GB free disk space
- Fast internet connection

**Supported Operating Systems:**
- Linux (Ubuntu, Debian, Fedora, RHEL, CentOS)

---

### Step 1: Install System Dependencies

#### Ubuntu/Debian:

```bash
# Update package list
sudo apt update

# Install Python 3 and venv
sudo apt install python3 python3-venv python3-pip

# Install build tools (required for some dependencies)
sudo apt install build-essential python3-dev
```

#### Fedora/RHEL/CentOS:

```bash
# Install Python 3 and development tools
sudo dnf install python3 python3-devel python3-pip gcc
```

---

### Step 2: Clone the Repository

```bash
# Clone from Git repository
git clone https://rep1.4s4group.bg/radko/background-replacer.git

# Navigate to project directory
cd background-replacer
```

**Alternative: Download as ZIP**
If you don't have Git:
1. Download the repository as ZIP file
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

---

### Step 3: Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Makes project portable and reproducible

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

---

### Step 4: Install Python Dependencies

**With virtual environment activated:**

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install rembg with CPU support
pip install "rembg[cpu]"
```

**Expected output:**
```
Successfully installed Pillow-12.1.0 rawpy-0.25.1 rembg-2.0.72 numpy-2.3.5 onnxruntime-1.23.2 ...
```

**Installation time:** 2-5 minutes (depending on internet speed)

---

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "Pillow|rawpy|rembg|numpy"

# Test the script (help command)
python background_replacer.py --help
```

**Expected output:**
```
usage: background_replacer.py [-h] [-o OUTPUT] [-d OUTPUT_DIR] ...
```

---

### Step 6: First Run (AI Model Download)

On first run, the AI model will be automatically downloaded (~176MB):

```bash
# Process a test image (model will download automatically)
python background_replacer.py your_image.jpg --color white
```

**First run output:**
```
Downloading u2net model...
Downloaded 176MB in 30-60 seconds
Processing: your_image.jpg
...
```

**Model storage location:**
- `~/.u2net/`

**Subsequent runs** will be much faster as the model is cached locally.

---

### Troubleshooting Installation

#### Error: "ModuleNotFoundError: No module named 'rawpy'"

**Solution:** Virtual environment not activated
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run script
python background_replacer.py image.jpg
```

#### Error: "The virtual environment was not created successfully"

**Solution:** Install python3-venv
```bash
sudo apt install python3.12-venv  # Ubuntu/Debian
```

#### Error: "No onnxruntime backend found"

**Solution:** Install rembg with CPU support
```bash
pip install "rembg[cpu]"
```

#### Error: "Permission denied"

**Solution:** Don't use sudo with pip in virtual environment
```bash
# Wrong
sudo pip install -r requirements.txt

# Correct
source venv/bin/activate
pip install -r requirements.txt
```

#### Error: "Cannot download model" / Timeout

**Solution:** Check internet connection or use proxy
```bash
# Set proxy (if needed)
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

#### Error: Out of memory during processing

**Solution:** Process smaller images or one at a time
```bash
# Resize image first
python background_replacer.py large_image.CR3 --width 2000 --color white

# Process files individually instead of batch
python background_replacer.py image1.CR3 --color white
python background_replacer.py image2.CR3 --color white
```

---

### Updating the Software

To get the latest version:

```bash
# Navigate to project directory
cd background-replacer

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull

# Update dependencies (if requirements changed)
pip install --upgrade -r requirements.txt
```

---

### Uninstallation

To completely remove the software:

```bash
# Deactivate virtual environment (if active)
deactivate

# Remove project directory
rm -rf background-replacer

# Remove AI models (optional)
rm -rf ~/.u2net
```

---

### GPU Acceleration (Optional)

GPU acceleration can dramatically improve processing speed (3-10x faster than CPU).

#### Benefits of GPU Acceleration

- **Speed**: 3-10x faster processing
- **Batch Processing**: Handle large batches efficiently
- **High Resolution**: Process 4K+ images smoothly
- **Real-time**: Near real-time processing for smaller images

**Performance Comparison:**
```
CPU (default):     10-20 seconds per image
GPU (NVIDIA):      2-5 seconds per image
GPU (high-end):    1-3 seconds per image
```

---

#### Requirements for GPU Acceleration

**Hardware:**
- NVIDIA GPU with CUDA support (GTX 1060 or newer recommended)
- AMD GPU with ROCm support (Linux only)
- Minimum 4GB VRAM (8GB+ recommended for large images)

**Software:**
- NVIDIA: CUDA Toolkit 11.x or 12.x
- AMD: ROCm 5.x (Linux only)
- Updated GPU drivers

---

#### Step 1: Check GPU Compatibility

**NVIDIA GPU (most common):**

```bash
# Check if NVIDIA GPU is available
nvidia-smi
```

**Expected output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03   Driver Version: 535.129.03   CUDA Version: 12.2   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
|  0%   45C    P8    15W / 250W |    500MiB /  8192MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

**AMD GPU:**

```bash
# Check if AMD GPU is available (Linux only)
rocm-smi
```

---

#### Step 2: Install CUDA Toolkit (NVIDIA)

**Ubuntu/Debian:**

```bash
# Add NVIDIA package repository
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update

# Install CUDA Toolkit
sudo apt install cuda-toolkit-12-2

# Add CUDA to PATH (add to ~/.bashrc)
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Reload bash configuration
source ~/.bashrc

# Verify installation
nvcc --version
```

---

#### Step 3: Install GPU-Enabled Dependencies

**Activate your virtual environment first:**

```bash
source venv/bin/activate
```

**For NVIDIA GPU (CUDA):**

```bash
# Uninstall CPU-only onnxruntime
pip uninstall onnxruntime

# Install GPU-enabled onnxruntime
pip install onnxruntime-gpu

# Verify CUDA is available
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

**Expected output:**
```python
['CUDAExecutionProvider', 'CPUExecutionProvider']
```

**For AMD GPU (ROCm - Linux only):**

```bash
# Uninstall CPU-only onnxruntime
pip uninstall onnxruntime

# Install ROCm-enabled onnxruntime
pip install onnxruntime-rocm

# Verify ROCm is available
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

**Expected output:**
```python
['ROCMExecutionProvider', 'CPUExecutionProvider']
```

---

#### Step 4: Test GPU Acceleration

**Test with a single image:**

```bash
# Process with GPU acceleration (automatically detected)
python background_replacer.py test_image.CR3 --color white
```

**Monitor GPU usage during processing:**

```bash
# Open new terminal and run:
watch -n 1 nvidia-smi  # NVIDIA
# or
watch -n 1 rocm-smi    # AMD
```

You should see GPU utilization increase to 80-100% during processing.

---

#### Performance Comparison Example

**Process 10 images with CPU:**
```bash
time python background_replacer.py *.CR3 --color white --output-dir ./cpu_test
# Result: ~150 seconds (2.5 minutes)
```

**Process 10 images with GPU:**
```bash
time python background_replacer.py *.CR3 --color white --output-dir ./gpu_test
# Result: ~25 seconds (6x faster!)
```

---

#### GPU Memory Management

**For high-resolution images or batch processing:**

**Check available VRAM:**
```bash
nvidia-smi --query-gpu=memory.free --format=csv
```

**If running out of VRAM:**

```bash
# Option 1: Reduce batch size (process fewer images at once)
python background_replacer.py img1.CR3 img2.CR3 --color white

# Option 2: Resize images before processing
python background_replacer.py large.CR3 --width 2000 --color white

# Option 3: Use lighter AI model
python background_replacer.py image.CR3 --model u2netp --color white
```

---

#### Troubleshooting GPU Acceleration

#### Issue: "CUDAExecutionProvider not available"

**Check CUDA installation:**
```bash
nvcc --version
nvidia-smi
```

**Reinstall onnxruntime-gpu:**
```bash
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-gpu
```

**Verify providers:**
```bash
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

---

#### Issue: "CUDA out of memory"

**Solutions:**

1. **Process smaller batches:**
```bash
# Instead of: python background_replacer.py *.CR3
python background_replacer.py img1.CR3 img2.CR3 img3.CR3
```

2. **Resize images:**
```bash
python background_replacer.py large.CR3 --width 2000 --color white
```

3. **Use lighter model:**
```bash
python background_replacer.py image.CR3 --model u2netp --color white
```

4. **Clear GPU cache:**
```bash
# Restart the script or run:
nvidia-smi --gpu-reset
```

---

#### Issue: Slower than CPU

**Possible causes:**

1. **Small images**: GPU overhead may exceed benefit for tiny images
2. **Old GPU**: GPU too old/weak (GTX 900 series or older)
3. **Wrong drivers**: Update NVIDIA/AMD drivers
4. **CPU bottleneck**: CPU preprocessing takes time before GPU work

**Solution:** GPU acceleration works best for:
- Batch processing (10+ images)
- High-resolution images (4K+)
- Modern GPUs (GTX 1060 or newer)

---

#### GPU Acceleration Tips

**Best practices:**

1. ✅ **Use GPU for batch processing**: Most efficient for 10+ images
2. ✅ **Monitor VRAM usage**: Use `nvidia-smi` or `rocm-smi`
3. ✅ **Keep drivers updated**: Latest drivers = best performance
4. ✅ **Use appropriate models**: Larger models benefit more from GPU
5. ✅ **Process in chunks**: If VRAM limited, process in smaller batches

**GPU vs CPU decision:**

```bash
# Use GPU for:
python background_replacer.py *.CR3 --responsive --color white  # Many outputs
python background_replacer.py huge_8k_image.CR3 --color white   # Large images
python background_replacer.py *.CR3 --model birefnet-massive    # Heavy models

# CPU is fine for:
python background_replacer.py single_small.jpg --color white    # Single small image
python background_replacer.py photo.CR3 --model u2netp          # Light model
```

---

#### Verify GPU is Being Used

**Method 1: Check during processing**

Terminal 1:
```bash
python background_replacer.py *.CR3 --color white
```

Terminal 2:
```bash
watch -n 0.5 nvidia-smi
```

Look for:
- GPU utilization: 80-100%
- Memory usage: Increasing during processing
- Process name: python

**Method 2: Check available providers**

```bash
python -c "
import onnxruntime as ort
print('Available providers:', ort.get_available_providers())
print('GPU available:', 'CUDAExecutionProvider' in ort.get_available_providers())
"
```

**Method 3: Compare processing times**

```bash
# Time with GPU
time python background_replacer.py test.CR3 --color white -o gpu_test.png

# Force CPU only (for comparison)
pip uninstall onnxruntime-gpu
pip install onnxruntime
time python background_replacer.py test.CR3 --color white -o cpu_test.png
```

---

#### Switching Between CPU and GPU

**Use GPU (default after installation):**
```bash
pip install onnxruntime-gpu
python background_replacer.py image.CR3 --color white
```

**Force CPU mode:**
```bash
pip uninstall onnxruntime-gpu
pip install onnxruntime
python background_replacer.py image.CR3 --color white
```

**Keep both (automatic selection):**
```bash
# Install GPU version (CPU fallback is automatic)
pip install onnxruntime-gpu

# Will use GPU if available, CPU if not
python background_replacer.py image.CR3 --color white
```

---

## Getting Started

### Activate Virtual Environment

**Always activate the virtual environment before running the script:**

```bash
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt when activated.

### Basic Syntax

```bash
python background_replacer.py [INPUT_FILES] [OPTIONS]
```

---

## Basic Usage

### Process Single Image

**White background (default):**
```bash
python background_replacer.py IMG_0124.CR3
```
Output: `IMG_0124_no_bg.png`

**Custom output name:**
```bash
python background_replacer.py IMG_0124.CR3 -o result.png
```

**Specify output directory:**
```bash
python background_replacer.py IMG_0124.CR3 --output-dir ./processed
```

---

## Background Options

### 1. Solid Colors

**Named colors:**
```bash
python background_replacer.py photo.CR3 --color white
python background_replacer.py photo.CR3 --color black
python background_replacer.py photo.CR3 --color red
python background_replacer.py photo.CR3 --color blue
```

Supported: `white`, `black`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`

**Hex colors:**
```bash
python background_replacer.py photo.CR3 --color "#FF5733"
python background_replacer.py photo.CR3 --color "#00FF00"
```

**RGB values:**
```bash
python background_replacer.py photo.CR3 --color "255,128,0"
python background_replacer.py photo.CR3 --color "128,128,128"
```

### 2. Custom Background Image

```bash
python background_replacer.py photo.CR3 --bg-image background.jpg
```
The background image will be automatically resized to match your foreground.

### 3. Transparent Background

```bash
python background_replacer.py photo.CR3 --format PNG
```
Omit `--color` option for transparent background (PNG/WebP/AVIF only).

---

## AI Model Selection

Choose the right model for your content type:

### General Purpose Models

**u2net (Default - Recommended for most cases):**
```bash
python background_replacer.py photo.CR3 --model u2net
```
- Best all-around model
- 176MB, balanced speed/accuracy

**u2netp (Fast processing):**
```bash
python background_replacer.py photo.CR3 --model u2netp
```
- Lightweight variant
- Faster but slightly less accurate

**silueta (Compact):**
```bash
python background_replacer.py photo.CR3 --model silueta
```
- Only 43MB
- Maintains u2net quality

### Portrait & Human Models

**birefnet-portrait (Best for portraits):**
```bash
python background_replacer.py portrait.CR3 --model birefnet-portrait
```
- Optimized for human portraits
- Superior edge quality

**u2net_human_seg (Human figures):**
```bash
python background_replacer.py person.jpg --model u2net_human_seg
```
- Specialized for human segmentation

### Specialized Models

**isnet-anime (Anime/artwork):**
```bash
python background_replacer.py anime.png --model isnet-anime
```
- High accuracy for anime characters

**u2net_cloth_seg (Clothing):**
```bash
python background_replacer.py clothing.jpg --model u2net_cloth_seg
```
- Designed for clothing segmentation

### Professional Models

**bria-rmbg (Maximum quality):**
```bash
python background_replacer.py photo.CR3 --model bria-rmbg
```
- State-of-the-art quality
- Best for professional work

**birefnet-massive (Highest accuracy):**
```bash
python background_replacer.py photo.CR3 --model birefnet-massive
```
- Trained on massive dataset
- Maximum accuracy

---

## Output Format Options

### PNG (Lossless, Default)

```bash
python background_replacer.py photo.CR3 --format PNG
```
- **Best for**: Graphics, transparency needed
- **File size**: Largest
- **Quality**: Perfect (lossless)

### JPEG (Lossy, Photo-optimized)

```bash
python background_replacer.py photo.CR3 --format JPG --quality 90 --color white
```
- **Best for**: Photos without transparency
- **File size**: Medium
- **Quality range**: 1-100 (default: 90)
- **Note**: No transparency support

### WebP (Modern, Versatile)

```bash
python background_replacer.py photo.CR3 --format WEBP --quality 85
```
- **Best for**: Web images with/without transparency
- **File size**: 25-35% smaller than PNG
- **Quality range**: 1-100 (default: 90)
- **Browser support**: Excellent (95%+)

### AVIF (Next-generation)

```bash
python background_replacer.py photo.CR3 --format AVIF --quality 80
```
- **Best for**: Modern web applications
- **File size**: 50%+ smaller than PNG
- **Quality range**: 1-100 (default: 90)
- **Browser support**: Growing (Chrome, Firefox, Safari)

### Quality Comparison Examples

```bash
# Maximum quality
python background_replacer.py photo.CR3 --format WEBP --quality 95

# Balanced (recommended for web)
python background_replacer.py photo.CR3 --format WEBP --quality 85

# Optimized for speed/size
python background_replacer.py photo.CR3 --format AVIF --quality 75
```

---

## Image Resizing

### 1. Resize by Width (maintains aspect ratio)

```bash
python background_replacer.py photo.CR3 --width 1920
```
Height is calculated automatically.

### 2. Resize by Height (maintains aspect ratio)

```bash
python background_replacer.py photo.CR3 --height 1080
```
Width is calculated automatically.

### 3. Resize by Scale Factor

```bash
# 50% of original size
python background_replacer.py photo.CR3 --scale 0.5

# 25% (thumbnail)
python background_replacer.py photo.CR3 --scale 0.25

# 200% (upscale)
python background_replacer.py photo.CR3 --scale 2.0
```

### 4. Fit Within Dimensions (maintains aspect)

```bash
python background_replacer.py photo.CR3 --width 1920 --height 1080
```
Image will fit within 1920x1080 while maintaining aspect ratio.

### 5. Exact Dimensions (may distort)

```bash
python background_replacer.py photo.CR3 --width 800 --height 600 --no-aspect
```
Forces exact dimensions, aspect ratio NOT maintained.

### Combining Resize with Other Options

```bash
# Web-optimized resized image
python background_replacer.py photo.CR3 --width 1200 --format WEBP --quality 85

# Thumbnail
python background_replacer.py photo.CR3 --scale 0.2 --format JPG --quality 80
```

---

## Color Filters

Apply artistic color filters for different moods and styles:

### Available Filters

#### 1. **warm** - Golden Hour / Sunset Look
```bash
python background_replacer.py photo.CR3 --filter warm --color white
```
- Increases red and yellow tones
- Decreases blue tones
- Perfect for warm, inviting photos

#### 2. **cool** / **cold** - Winter / Arctic Feel
```bash
python background_replacer.py photo.CR3 --filter cool --color white
```
- Increases blue tones
- Decreases red tones
- Creates cold, crisp atmosphere

#### 3. **sepia** - Classic Vintage
```bash
python background_replacer.py photo.CR3 --filter sepia --color white
```
- Classic brown-toned vintage look
- Timeless, nostalgic feel

#### 4. **vintage** - Film Photography
```bash
python background_replacer.py photo.CR3 --filter vintage --color "#F5F5DC"
```
- Faded colors with warm undertones
- Resembles old film photographs

#### 5. **vibrant** - Bold Colors
```bash
python background_replacer.py photo.CR3 --filter vibrant --color white
```
- Increases color intensity
- Makes colors pop
- Great for product photography

#### 6. **muted** - Desaturated / Pastel
```bash
python background_replacer.py photo.CR3 --filter muted --color white
```
- Soft, desaturated colors
- Elegant, modern aesthetic

### Saturation Control

Fine-tune color intensity:

```bash
# Grayscale / Black & White
python background_replacer.py photo.CR3 --saturation 0.0

# Subtle desaturation
python background_replacer.py photo.CR3 --saturation 0.7

# Original colors (default)
python background_replacer.py photo.CR3 --saturation 1.0

# Enhanced saturation
python background_replacer.py photo.CR3 --saturation 1.5

# Maximum saturation (vivid)
python background_replacer.py photo.CR3 --saturation 2.0
```

### Combining Filters

```bash
# Warm filter with slight desaturation
python background_replacer.py photo.CR3 --filter warm --saturation 0.9 --color white

# Cool filter with enhanced saturation
python background_replacer.py photo.CR3 --filter cool --saturation 1.3 --color white
```

---

## Image Enhancements

### 1. Brightness Adjustment

```bash
# 20% brighter
python background_replacer.py photo.CR3 --brightness 1.2

# Original brightness (default)
python background_replacer.py photo.CR3 --brightness 1.0

# 20% darker
python background_replacer.py photo.CR3 --brightness 0.8
```
Range: 0.0 (black) to 2.0+ (very bright)

### 2. Contrast Adjustment

```bash
# More contrast
python background_replacer.py photo.CR3 --contrast 1.3

# Original contrast (default)
python background_replacer.py photo.CR3 --contrast 1.0

# Less contrast (soft)
python background_replacer.py photo.CR3 --contrast 0.7
```
Range: 0.0 (gray) to 2.0+ (high contrast)

### 3. Sharpness Adjustment

```bash
# Sharper
python background_replacer.py photo.CR3 --sharpness 1.5

# Original sharpness (default)
python background_replacer.py photo.CR3 --sharpness 1.0

# Softer / Blurred
python background_replacer.py photo.CR3 --sharpness 0.5
```
Range: 0.0 (blurred) to 2.0+ (very sharp)

### 4. Edge Feathering

Soften edges with Gaussian blur:

```bash
# Subtle feather (3 pixels)
python background_replacer.py photo.CR3 --feather 3

# Medium feather (5 pixels)
python background_replacer.py photo.CR3 --feather 5

# Strong feather (10 pixels)
python background_replacer.py photo.CR3 --feather 10
```

Perfect for composite images.

### Combining Multiple Enhancements

```bash
python background_replacer.py photo.CR3 \
  --brightness 1.1 \
  --contrast 1.2 \
  --sharpness 1.3 \
  --feather 2 \
  --color white
```

---

## Web Optimization

Optimize images for web deployment with faster loading and smaller file sizes:

### 1. Progressive JPEG

```bash
python background_replacer.py photo.CR3 --format JPG --progressive --color white
```
- Loads images incrementally (low to high quality)
- Improves perceived performance
- **Only works with JPEG format**
- Recommended for hero images and large photos

### 2. Strip Metadata

```bash
python background_replacer.py photo.CR3 --strip-metadata
```
- Removes all EXIF data (camera, GPS, timestamps)
- Reduces file size
- Improves privacy
- **Works with all formats**

### 3. Web-Optimized Preset

```bash
python background_replacer.py photo.CR3 --format JPG --web-optimized --quality 85
```
Enables both progressive JPEG and metadata stripping in one flag.

### 4. Responsive Image Generation

Generate multiple image sizes at standard breakpoints:

```bash
# Standard breakpoints (640, 768, 1024, 1280, 1920, 2560px)
python background_replacer.py photo.CR3 --responsive --format WEBP --color white
```

Output files:
- `photo_640w.webp`
- `photo_768w.webp`
- `photo_1024w.webp`
- `photo_1280w.webp`
- `photo_1920w.webp`
- `photo_2560w.webp`

**Custom breakpoints:**
```bash
python background_replacer.py photo.CR3 --responsive --breakpoints "480,768,1200,1920"
```

**Full web optimization workflow:**
```bash
python background_replacer.py product.CR3 \
  --responsive \
  --format WEBP \
  --web-optimized \
  --quality 85 \
  --color white \
  --output-dir ./web-images
```

### HTML Usage Example

```html
<picture>
  <source srcset="product_640w.webp 640w,
                  product_1024w.webp 1024w,
                  product_1920w.webp 1920w"
          sizes="(max-width: 640px) 100vw,
                 (max-width: 1024px) 80vw,
                 1200px"
          type="image/webp">
  <img src="product_1024w.webp" alt="Product">
</picture>
```

---

## Batch Processing

Process multiple images with consistent settings.

### 1. Wildcard Pattern (Most Convenient)

```bash
# Process all CR3 files
python background_replacer.py *.CR3 --color white --output-dir ./processed

# Process all JPG files
python background_replacer.py *.jpg --format WEBP --quality 85 --output-dir ./webp
```

### 2. Specify Multiple Files

```bash
python background_replacer.py IMG_0124.CR3 IMG_0150.CR3 IMG_0159.CR3 \
  --color white \
  --output-dir ./processed
```

### 3. Batch with Web Optimization

```bash
python background_replacer.py *.CR3 \
  --format WEBP \
  --web-optimized \
  --width 1200 \
  --quality 85 \
  --color white \
  --output-dir ./web-ready
```

### 4. Batch Responsive Images

```bash
python background_replacer.py *.CR3 \
  --responsive \
  --format WEBP \
  --web-optimized \
  --breakpoints "640,1024,1920" \
  --color white \
  --output-dir ./responsive
```

### 5. Create Multiple Formats

```bash
# Export as PNG
python background_replacer.py *.CR3 --format PNG --output-dir ./png

# Export as WebP
python background_replacer.py *.CR3 --format WEBP --quality 85 --output-dir ./webp

# Export as AVIF
python background_replacer.py *.CR3 --format AVIF --quality 80 --output-dir ./avif

# Export as JPG with white background
python background_replacer.py *.CR3 --format JPG --quality 90 --color white --output-dir ./jpg
```

### 6. Create Multiple Sizes

```bash
# Full size
python background_replacer.py *.CR3 --width 1920 --format WEBP --output-dir ./full

# Medium size
python background_replacer.py *.CR3 --width 1200 --format WEBP --output-dir ./medium

# Small size
python background_replacer.py *.CR3 --width 600 --format WEBP --output-dir ./small

# Thumbnails
python background_replacer.py *.CR3 --scale 0.2 --format JPG --output-dir ./thumbs
```

---

## Advanced Features

### 1. Alpha Matting

Enables refined edge detection for smoother cutouts:

```bash
python background_replacer.py photo.CR3 --alpha-matting
```

**Best combined with portrait models:**
```bash
python background_replacer.py portrait.CR3 \
  --model birefnet-portrait \
  --alpha-matting \
  --color white
```

### 2. Mask Output

Export only the segmentation mask:

```bash
python background_replacer.py photo.CR3 --mask-only -o mask.png
```

**Compare different models:**
```bash
python background_replacer.py photo.jpg --model u2net --mask-only -o mask_u2net.png
python background_replacer.py photo.jpg --model birefnet-general --mask-only -o mask_birefnet.png
```

### 3. Custom Output Suffix

Change the default `_no_bg` suffix:

```bash
python background_replacer.py photo.CR3 --suffix "_processed"
```
Output: `photo_processed.png`

```bash
python background_replacer.py photo.CR3 --suffix "_final"
```
Output: `photo_final.png`

---

## Professional Workflows

### Workflow 1: E-commerce Product Photography

```bash
python background_replacer.py product.CR3 \
  --model u2net \
  --alpha-matting \
  --responsive \
  --format WEBP \
  --web-optimized \
  --quality 85 \
  --brightness 1.05 \
  --contrast 1.1 \
  --sharpness 1.2 \
  --filter vibrant \
  --color white \
  --breakpoints "640,1024,1920" \
  --output-dir ./product-images
```

### Workflow 2: Portrait Photography

```bash
python background_replacer.py portrait.CR3 \
  --model birefnet-portrait \
  --alpha-matting \
  --format PNG \
  --brightness 1.08 \
  --contrast 1.05 \
  --feather 2 \
  --filter warm \
  --saturation 1.05 \
  --color white \
  -o final_portrait.png
```

### Workflow 3: Social Media Content

```bash
python background_replacer.py photo.CR3 \
  --model u2net \
  --format AVIF \
  --web-optimized \
  --width 1080 \
  --quality 80 \
  --filter vibrant \
  --saturation 1.2 \
  --color white \
  -o social_media.avif
```

### Workflow 4: Batch Website Images

```bash
python background_replacer.py *.CR3 \
  --responsive \
  --format WEBP \
  --web-optimized \
  --quality 85 \
  --filter vibrant \
  --color white \
  --output-dir ./website
```

### Workflow 5: Print-Ready Images

```bash
python background_replacer.py photo.CR3 \
  --model birefnet-massive \
  --alpha-matting \
  --format PNG \
  --brightness 1.05 \
  --contrast 1.1 \
  --sharpness 1.15 \
  --color white \
  -o print_ready.png
```

### Workflow 6: Vintage Style Photos

```bash
python background_replacer.py photo.CR3 \
  --model u2net \
  --format JPG \
  --quality 90 \
  --filter sepia \
  --saturation 0.8 \
  --contrast 0.9 \
  --feather 5 \
  --color "#F5DEB3" \
  -o vintage_photo.jpg
```

---

## Tips & Best Practices

### Choosing the Right Model

1. **For portraits**: Use `birefnet-portrait` or `u2net_human_seg`
2. **For products**: Use `u2net` (default) or `birefnet-general`
3. **For anime/art**: Use `isnet-anime`
4. **For speed**: Use `u2netp` or `silueta`
5. **For maximum quality**: Use `bria-rmbg` or `birefnet-massive`

### Quality Settings

- **PNG**: Always lossless, no quality setting needed
- **JPEG**: Use 85-95 for high quality, 75-85 for web, 60-75 for small files
- **WebP**: Use 85-90 for excellent quality/size balance
- **AVIF**: Use 75-85 for best results (more efficient than JPEG/WebP)

### Performance Tips

1. **Process in batches**: More efficient than individual files
2. **Use appropriate model**: Lighter models (u2netp, silueta) for speed
3. **Resize during processing**: More efficient than resizing afterwards
4. **Use web-optimized preset**: Combines multiple optimizations

### File Size Optimization

```bash
# Smallest possible (aggressive)
python background_replacer.py photo.CR3 \
  --format AVIF \
  --web-optimized \
  --quality 75 \
  --width 1920

# Balanced quality/size (recommended)
python background_replacer.py photo.CR3 \
  --format WEBP \
  --web-optimized \
  --quality 85 \
  --width 1920

# Maximum quality
python background_replacer.py photo.CR3 \
  --format PNG \
  --strip-metadata
```

### Color Accuracy

- Use `--filter vibrant` for product photography
- Use `--filter warm` for portraits and lifestyle
- Use `--filter cool` for technology and modern aesthetics
- Adjust `--saturation` between 1.0-1.3 for subtle enhancement
- Avoid over-saturation (>1.5) for realistic results

### Edge Quality

1. **Enable alpha matting** for difficult subjects (hair, fur, etc.)
2. **Use appropriate feathering** (2-5 pixels) for composite images
3. **Choose portrait models** for human subjects
4. **Adjust sharpness** slightly higher (1.1-1.2) after background removal

### Responsive Images Best Practices

1. **Use WebP or AVIF** format for best compression
2. **Standard breakpoints** work for most cases: 640, 1024, 1920px
3. **Custom breakpoints** for specific design requirements
4. **Always use --web-optimized** with responsive images
5. **Quality 80-85** provides excellent balance

### Batch Processing Efficiency

```bash
# Bad: Running script multiple times
python background_replacer.py IMG_0124.CR3 --color white
python background_replacer.py IMG_0150.CR3 --color white
python background_replacer.py IMG_0159.CR3 --color white

# Good: Single batch command
python background_replacer.py *.CR3 --color white --output-dir ./processed
```

### Common Mistakes to Avoid

1. ❌ Forgetting to activate virtual environment
2. ❌ Using JPEG without specifying background color (needs RGB)
3. ❌ Over-processing with too many enhancements
4. ❌ Not using web optimization for web images
5. ❌ Processing files individually instead of batch mode
6. ❌ Using PNG for web when WebP/AVIF would be better

### Troubleshooting Tips

**Issue**: Images look too processed
- **Solution**: Reduce enhancement values (1.05-1.1 instead of 1.2-1.5)

**Issue**: Edges look rough
- **Solution**: Enable `--alpha-matting` and add `--feather 2`

**Issue**: Files too large
- **Solution**: Use WebP/AVIF with `--web-optimized` and `--quality 80-85`

**Issue**: Processing too slow
- **Solution**: Use faster model like `u2netp` or `silueta`

**Issue**: Colors look off
- **Solution**: Adjust `--saturation` to 0.9-1.1 or try different filters

---

## Quick Reference

### Most Common Commands

```bash
# Basic white background
python background_replacer.py photo.CR3 --color white

# Web-optimized single image
python background_replacer.py photo.CR3 --format WEBP --web-optimized --quality 85 --color white

# Responsive images for web
python background_replacer.py photo.CR3 --responsive --format WEBP --web-optimized --color white

# Batch process all CR3 files
python background_replacer.py *.CR3 --color white --output-dir ./processed

# High-quality portrait
python background_replacer.py portrait.CR3 --model birefnet-portrait --alpha-matting --color white
```

### All Options Summary

```
Input/Output:
  input                         Input file(s) or pattern (*.CR3)
  -o, --output                  Output file path (single file only)
  -d, --output-dir              Output directory (batch processing)
  -f, --format                  PNG, JPG, WEBP, AVIF (default: PNG)
  --suffix                      Output file suffix (default: _no_bg)
  -q, --quality                 Quality 1-100 for JPG/WEBP/AVIF (default: 90)

Background:
  -c, --color                   Solid color (white, #FFFFFF, 255,255,255)
  -b, --bg-image                Background image file path

AI Model:
  -m, --model                   u2net, birefnet-portrait, isnet-anime, etc.
  -a, --alpha-matting           Enable alpha matting for better edges
  --mask-only                   Output only segmentation mask

Enhancements:
  --brightness                  0.0-2.0+ (default: 1.0)
  --contrast                    0.0-2.0+ (default: 1.0)
  --sharpness                   0.0-2.0+ (default: 1.0)
  --feather                     Edge feathering in pixels (default: 0)

Color Filters:
  --filter                      warm, cool, cold, sepia, vintage, vibrant, muted
  --saturation                  0.0-2.0+ (default: 1.0)

Resize:
  --width                       Target width in pixels
  --height                      Target height in pixels
  --scale                       Scale factor (0.5 = 50%, 2.0 = 200%)
  --no-aspect                   Don't maintain aspect ratio

Web Optimization:
  --progressive                 Progressive JPEG encoding
  --strip-metadata              Remove EXIF/metadata
  --web-optimized               Enable progressive + strip metadata
  --responsive                  Generate multiple sizes
  --breakpoints                 Custom breakpoints (e.g., "640,1024,1920")
```

---

## Getting Help

**Command-line help:**
```bash
python background_replacer.py --help
```

**View this manual:**
```bash
cat USER_MANUAL.md
```

**Check available models:**
```bash
python background_replacer.py --help | grep -A 15 "Available Models"
```

---

**For more information, see README.md for installation and technical details.**

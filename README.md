# Background Replacement Tool - Advanced Edition

Professional AI-powered background removal and replacement tool with 20+ AI models and advanced image processing. Supports Canon RAW (CR3) files and standard image formats.

**Author**: Radko Yordanov

## Overview

This tool uses state-of-the-art AI models to automatically detect and remove backgrounds from images, then replaces them with solid colors or custom background images. Features multiple specialized models, alpha matting, and comprehensive image enhancements. Perfect for product photography, portraits, and professional photo editing.

## Features

### Core Features
- **Multiple AI Models (20+)**: Choose from general, portrait, anime, and professional models
- **RAW Format Support**: Native support for Canon CR3, CR2, NEF, ARW, and DNG files
- **Modern Output Formats**: PNG, JPG, WebP, AVIF with quality control
- **Image Resizing**: Scale, fit to dimensions, or exact size with aspect control
- **Flexible Background Options**:
  - Solid colors (white, black, custom RGB/hex colors)
  - Custom background images
  - Transparent backgrounds (PNG/WebP/AVIF output)
- **Batch Processing**: Process multiple images at once with consistent settings
- **Quality Control**: Adjustable quality for JPG/WebP/AVIF (1-100)

### Advanced Features
- **Alpha Matting**: Refined edge detection for smoother cutouts
- **Mask Output**: Export segmentation masks
- **Image Enhancement**: Adjust brightness, contrast, and sharpness
- **Edge Feathering**: Smooth edge transitions with Gaussian blur
- **Color Filters**: Apply artistic filters (warm, cool, sepia, vintage, vibrant, muted)
- **Saturation Control**: From grayscale to hyper-saturated colors
- **Model Selection**: Choose optimal model for your content type

### Web Optimization Features
- **Progressive JPEG**: Incremental loading for faster perceived performance
- **Metadata Stripping**: Remove EXIF data for privacy and smaller files
- **Web-Optimized Preset**: One-click optimization for web deployment
- **Responsive Image Generation**: Create multiple sizes at standard breakpoints (640-2560px)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- python3-venv (for virtual environment)

### Step 1: Install System Dependencies

On Ubuntu/Debian systems:
```bash
sudo apt install python3.12-venv
```

### Step 2: Set Up Virtual Environment

Create a Python virtual environment to isolate dependencies:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

> **Note**: You need to activate the virtual environment every time you open a new terminal session.

### Step 3: Install Python Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Install rembg with CPU support:
```bash
pip install "rembg[cpu]"
```

> **First Run**: The AI model (~176MB) will be automatically downloaded on first use.

## Available AI Models

The tool supports 20+ specialized AI models for different use cases:

### General Purpose Models
- **u2net** (default): Best general-purpose model, balanced speed and accuracy (~176MB)
- **u2netp**: Lightweight variant, faster processing with reduced size
- **silueta**: Compact version (43MB), maintains u2net quality at smaller size
- **isnet-general-use**: State-of-the-art general segmentation model
- **birefnet-general**: High-performance all-purpose model (latest technology)
- **birefnet-general-lite**: Lightweight variant for resource-constrained environments

### Human & Portrait Models
- **u2net_human_seg**: Specialized for human figure segmentation
- **birefnet-portrait**: Optimized for human portrait photography with superior edge quality

### Specialized Models
- **u2net_cloth_seg**: Designed for clothing segmentation (upper body, lower body, full body)
- **isnet-anime**: High-accuracy segmentation optimized for anime character artwork

### Advanced Models
- **birefnet-massive**: Trained on massive dataset for maximum accuracy
- **birefnet-dis**: Dichotomous image segmentation variant
- **birefnet-hrsod**: High-resolution salient object detection
- **birefnet-cod**: Camouflaged object detection
- **sam**: Segment Anything Model from Meta AI (flexible with prompts)
- **bria-rmbg**: State-of-the-art background removal from BRIA AI

### Model Recommendations
- **Portraits**: `birefnet-portrait` or `u2net_human_seg`
- **Products**: `u2net` or `birefnet-general`
- **Anime/Art**: `isnet-anime`
- **Fast Processing**: `u2netp` or `silueta`
- **Maximum Quality**: `birefnet-massive` or `bria-rmbg`
- **Clothing**: `u2net_cloth_seg`

> **Note**: Models are automatically downloaded (~40MB-300MB each) and cached in `~/.u2net/` on first use.

## Main Components

### 1. `background_replacer.py`
The main script that orchestrates the entire background replacement process with advanced features.

**Key Functions:**
- `read_cr3_image()`: Reads Canon RAW files using rawpy library
- `read_image()`: Universal image reader supporting multiple formats
- `remove_background()`: AI-powered background removal with model selection and alpha matting
- `enhance_image()`: Apply brightness, contrast, sharpness adjustments and edge feathering
- `replace_background()`: Composites foreground over new background
- `process_image()`: End-to-end image processing pipeline with all options
- `parse_color()`: Parses color strings (hex, RGB, named colors)

### 2. `requirements.txt`
Specifies Python dependencies:
- **Pillow**: Image processing and manipulation
- **rawpy**: RAW image file reading
- **rembg**: AI background removal (uses U2-Net model)
- **numpy**: Numerical operations for image arrays

### 3. `venv/` (Virtual Environment)
Isolated Python environment containing all installed packages and dependencies.

### 4. AI Model
The U2-Net model (`~/.u2net/u2net.onnx`) is downloaded automatically on first run:
- **Size**: 176MB
- **Purpose**: Semantic segmentation for background detection
- **Technology**: Deep learning neural network trained on salient object detection

## Usage

### Activate Virtual Environment

Always activate the virtual environment before running the script:
```bash
source venv/bin/activate
```

### Basic Usage

Process a single image with default white background:
```bash
python background_replacer.py IMG_0124.CR3
```

Output: `IMG_0124_no_bg.png`

### Background Color Options

#### Named Colors
```bash
python background_replacer.py IMG_0124.CR3 --color white
python background_replacer.py IMG_0124.CR3 --color black
python background_replacer.py IMG_0124.CR3 --color red
python background_replacer.py IMG_0124.CR3 --color green
python background_replacer.py IMG_0124.CR3 --color blue
```

**Supported named colors**: white, black, red, green, blue, yellow, cyan, magenta

#### Hex Colors
```bash
python background_replacer.py IMG_0124.CR3 --color "#00FF00"
python background_replacer.py IMG_0124.CR3 --color "#FF5733"
```

#### RGB Values
```bash
python background_replacer.py IMG_0124.CR3 --color "255,0,0"
python background_replacer.py IMG_0124.CR3 --color "128,128,128"
```

### Custom Background Image

Replace background with another image:
```bash
python background_replacer.py IMG_0124.CR3 --bg-image /path/to/background.jpg
```

The background image will be automatically resized to match the foreground dimensions.

### Transparent Background

Omit the `--color` option to create a transparent PNG:
```bash
python background_replacer.py IMG_0124.CR3
```

### Batch Processing

Process all CR3 files in the current directory:
```bash
python background_replacer.py *.CR3 --output-dir ./processed
```

Process all CR3 files with green background:
```bash
python background_replacer.py *.CR3 --color green --output-dir ./processed
```

### Output Format Options

The tool supports multiple modern image formats with quality control:

**PNG (Lossless, Default):**
```bash
python background_replacer.py IMG_0124.CR3 --format PNG
```
- Best for graphics and images requiring transparency
- Lossless compression
- Larger file sizes

**JPEG (Lossy):**
```bash
python background_replacer.py IMG_0124.CR3 --format JPG --quality 90
```
- Best for photographs without transparency
- Smaller file sizes
- Quality: 1-100 (default: 90)

**WebP (Modern):**
```bash
python background_replacer.py IMG_0124.CR3 --format WEBP --quality 85
```
- Modern format with excellent compression
- Supports transparency
- ~25-35% smaller than PNG
- Wide browser support

**AVIF (Next-Gen):**
```bash
python background_replacer.py IMG_0124.CR3 --format AVIF --quality 80
```
- Latest format with best compression
- Supports transparency
- ~50% smaller than PNG
- Growing browser support

**Quality Comparison Example:**
```bash
# High quality (larger files)
python background_replacer.py IMG_0124.CR3 --format WEBP --quality 95

# Balanced quality (recommended)
python background_replacer.py IMG_0124.CR3 --format WEBP --quality 85

# Smaller files (web optimized)
python background_replacer.py IMG_0124.CR3 --format AVIF --quality 75
```

**Other Options:**

Specify custom output path (single file only):
```bash
python background_replacer.py IMG_0124.CR3 -o result.png
```

Change output file suffix (default is `_no_bg`):
```bash
python background_replacer.py IMG_0124.CR3 --suffix "_edited"
```
Output: `IMG_0124_edited.png`

### Image Resizing

Resize images while processing for optimized output:

**Resize by Width (maintains aspect ratio):**
```bash
python background_replacer.py IMG_0124.CR3 --width 1920
```

**Resize by Height (maintains aspect ratio):**
```bash
python background_replacer.py IMG_0124.CR3 --height 1080
```

**Resize by Scale Factor:**
```bash
python background_replacer.py IMG_0124.CR3 --scale 0.5   # 50% of original size
python background_replacer.py IMG_0124.CR3 --scale 0.25  # 25% for thumbnails
python background_replacer.py IMG_0124.CR3 --scale 2.0   # 200% upscale
```

**Fit Within Dimensions (maintains aspect ratio):**
```bash
python background_replacer.py IMG_0124.CR3 --width 1920 --height 1080
```
Image will fit within 1920x1080 while maintaining aspect ratio

**Exact Dimensions (may distort):**
```bash
python background_replacer.py IMG_0124.CR3 --width 800 --height 600 --no-aspect
```

**Combine Resize with Format:**
```bash
# Create web-optimized version
python background_replacer.py IMG_0124.CR3 --width 1200 --format WEBP --quality 85

# Create thumbnail
python background_replacer.py IMG_0124.CR3 --scale 0.2 --format JPG --quality 80

# Batch create multiple sizes
python background_replacer.py *.CR3 --width 1920 --format AVIF --quality 80 --output-dir ./full
python background_replacer.py *.CR3 --width 800 --format WEBP --quality 85 --output-dir ./medium
python background_replacer.py *.CR3 --width 400 --format WEBP --quality 80 --output-dir ./small
```

### Color Filters and Grading

Apply artistic color filters and adjustments for different moods and styles:

**Warm Filter (Golden Hour, Sunset):**
```bash
python background_replacer.py IMG_0124.CR3 --filter warm --color white
```
- Increases red and yellow tones
- Decreases blue tones
- Perfect for warm, inviting photos

**Cool/Cold Filter (Winter, Arctic):**
```bash
python background_replacer.py IMG_0124.CR3 --filter cool --color white
```
- Increases blue tones
- Decreases red tones
- Creates cold, crisp atmosphere

**Sepia Tone (Classic Vintage):**
```bash
python background_replacer.py IMG_0124.CR3 --filter sepia --color white
```
- Classic brown-toned vintage look
- Timeless, nostalgic feel

**Vintage Filter (Film Photography):**
```bash
python background_replacer.py IMG_0124.CR3 --filter vintage --color "#F5F5DC"
```
- Faded colors with warm undertones
- Resembles old film photographs

**Vibrant Filter (Bold Colors):**
```bash
python background_replacer.py IMG_0124.CR3 --filter vibrant --color white
```
- Increases color intensity
- Makes colors pop
- Great for product photography

**Muted Filter (Desaturated, Pastel):**
```bash
python background_replacer.py IMG_0124.CR3 --filter muted --color white
```
- Soft, desaturated colors
- Elegant, modern aesthetic

**Saturation Control:**
```bash
# Grayscale/Black & White
python background_replacer.py IMG_0124.CR3 --saturation 0.0 --color white

# Subtle desaturation
python background_replacer.py IMG_0124.CR3 --saturation 0.7 --color white

# Original colors
python background_replacer.py IMG_0124.CR3 --saturation 1.0

# Enhanced saturation
python background_replacer.py IMG_0124.CR3 --saturation 1.5 --color white

# Maximum saturation (vivid)
python background_replacer.py IMG_0124.CR3 --saturation 2.0 --color white
```

**Combine Filters with Other Effects:**
```bash
# Warm vintage portrait
python background_replacer.py portrait.CR3 \
  --model birefnet-portrait \
  --filter warm \
  --saturation 0.9 \
  --brightness 1.05 \
  --contrast 1.1 \
  --color "#FFF8DC"

# Cool modern product photo
python background_replacer.py product.jpg \
  --filter cool \
  --saturation 1.2 \
  --sharpness 1.3 \
  --color white \
  --format WEBP

# Sepia vintage with vignette effect
python background_replacer.py old_photo.jpg \
  --filter sepia \
  --contrast 0.9 \
  --feather 15 \
  --color "#F5DEB3"
```

**Filter Comparison (Batch Processing):**
```bash
# Create same image with different filters
python background_replacer.py portrait.CR3 --filter warm -o portrait_warm.png
python background_replacer.py portrait.CR3 --filter cool -o portrait_cool.png
python background_replacer.py portrait.CR3 --filter sepia -o portrait_sepia.png
python background_replacer.py portrait.CR3 --filter vintage -o portrait_vintage.png
python background_replacer.py portrait.CR3 --filter vibrant -o portrait_vibrant.png
python background_replacer.py portrait.CR3 --filter muted -o portrait_muted.png
```

### Web Optimization Features

Optimize images specifically for web deployment with faster loading and smaller file sizes:

**Progressive JPEG (Faster Perceived Loading):**
```bash
python background_replacer.py product.CR3 --format JPG --progressive
```
- Loads images in multiple passes (low to high quality)
- Improves perceived performance on slow connections
- Only works with JPEG format
- Recommended for web hero images and large photos

**Strip Metadata (Privacy & Size Reduction):**
```bash
python background_replacer.py photo.CR3 --strip-metadata
```
- Removes all EXIF data (camera settings, GPS, timestamps)
- Reduces file size by removing unnecessary data
- Improves privacy by removing location and device info
- Works with all formats

**Web-Optimized Preset (Best for Web):**
```bash
python background_replacer.py product.CR3 --format JPG --web-optimized --quality 85
```
- Enables progressive JPEG encoding
- Strips all metadata
- Applies optimize flag for maximum compression
- Single flag for complete web optimization

**Responsive Image Generation (Multiple Sizes):**
```bash
# Generate responsive image set at standard breakpoints
python background_replacer.py product.CR3 --responsive --format WEBP
```
- Creates images at 6 standard breakpoints: 640, 768, 1024, 1280, 1920, 2560px
- Outputs: `product_640w.webp`, `product_768w.webp`, etc.
- Perfect for HTML `<picture>` element with `srcset`
- Skips breakpoints larger than original image

**Custom Breakpoints:**
```bash
python background_replacer.py photo.CR3 --responsive --breakpoints "480,768,1200,1920"
```

**Complete Web Optimization Workflow:**
```bash
# Generate responsive WebP images with full optimization
python background_replacer.py product.CR3 \
  --responsive \
  --format WEBP \
  --web-optimized \
  --quality 85 \
  --filter vibrant \
  --output-dir ./web-images

# Generate responsive AVIF for modern browsers (smaller files)
python background_replacer.py product.CR3 \
  --responsive \
  --format AVIF \
  --web-optimized \
  --quality 80 \
  --breakpoints "640,1024,1920" \
  --output-dir ./avif-images
```

**HTML Usage Example:**
```html
<!-- Use responsive images in HTML -->
<picture>
  <source srcset="product_640w.webp 640w,
                  product_768w.webp 768w,
                  product_1024w.webp 1024w,
                  product_1920w.webp 1920w"
          sizes="(max-width: 640px) 100vw,
                 (max-width: 1024px) 80vw,
                 1200px"
          type="image/webp">
  <img src="product_1024w.webp" alt="Product">
</picture>
```

**Performance Comparison:**
```bash
# Standard PNG (baseline)
python background_replacer.py product.CR3 --format PNG
# Result: ~2.5MB, no progressive loading

# Progressive JPEG (faster loading)
python background_replacer.py product.CR3 --format JPG --progressive --quality 90
# Result: ~400KB, incremental display, 84% smaller

# Web-optimized WebP (best quality/size balance)
python background_replacer.py product.CR3 --format WEBP --web-optimized --quality 85
# Result: ~180KB, excellent quality, 93% smaller

# Web-optimized AVIF (maximum compression)
python background_replacer.py product.CR3 --format AVIF --web-optimized --quality 80
# Result: ~120KB, great quality, 95% smaller
```

### Advanced: AI Model Selection

Use different AI models for specific content types:

**Portrait Photography:**
```bash
python background_replacer.py portrait.CR3 --model birefnet-portrait
```

**Human Segmentation:**
```bash
python background_replacer.py photo.jpg --model u2net_human_seg
```

**Anime/Artwork:**
```bash
python background_replacer.py anime.png --model isnet-anime
```

**Maximum Quality:**
```bash
python background_replacer.py product.jpg --model bria-rmbg
```

**Fast Processing:**
```bash
python background_replacer.py *.jpg --model silueta --output-dir ./fast
```

### Advanced: Alpha Matting

Enable alpha matting for smoother edge refinement:
```bash
python background_replacer.py IMG_0124.CR3 --alpha-matting
```

Combine with portrait model for best results:
```bash
python background_replacer.py portrait.jpg --model birefnet-portrait --alpha-matting
```

### Advanced: Image Enhancements

**Adjust Brightness:**
```bash
python background_replacer.py IMG_0124.CR3 --brightness 1.2  # 20% brighter
python background_replacer.py IMG_0124.CR3 --brightness 0.8  # 20% darker
```

**Adjust Contrast:**
```bash
python background_replacer.py IMG_0124.CR3 --contrast 1.3    # More contrast
python background_replacer.py IMG_0124.CR3 --contrast 0.7    # Less contrast
```

**Adjust Sharpness:**
```bash
python background_replacer.py IMG_0124.CR3 --sharpness 1.5   # Sharper
python background_replacer.py IMG_0124.CR3 --sharpness 0.5   # Softer
```

**Combine Multiple Enhancements:**
```bash
python background_replacer.py IMG_0124.CR3 --brightness 1.1 --contrast 1.2 --sharpness 1.3
```

### Advanced: Edge Feathering

Soften edges with Gaussian blur for smooth transitions:
```bash
python background_replacer.py IMG_0124.CR3 --feather 3  # 3 pixel feather
python background_replacer.py IMG_0124.CR3 --feather 10 # 10 pixel feather (very soft)
```

Perfect for composite images:
```bash
python background_replacer.py subject.jpg --bg-image scene.jpg --feather 5
```

### Advanced: Mask Output

Export only the segmentation mask:
```bash
python background_replacer.py IMG_0124.CR3 --mask-only
```

Use with different models to compare results:
```bash
python background_replacer.py photo.jpg --model u2net --mask-only -o mask_u2net.png
python background_replacer.py photo.jpg --model birefnet-general --mask-only -o mask_birefnet.png
```

### Professional Workflow Example

Complete professional processing with all features:
```bash
python background_replacer.py portrait.CR3 \
  --model birefnet-portrait \
  --alpha-matting \
  --brightness 1.1 \
  --contrast 1.15 \
  --sharpness 1.2 \
  --feather 2 \
  --color white \
  --format PNG \
  -o final_portrait.png
```

Batch process with consistent settings:
```bash
python background_replacer.py *.CR3 \
  --model u2net_human_seg \
  --alpha-matting \
  --brightness 1.1 \
  --feather 3 \
  --color "#F5F5F5" \
  --output-dir ./processed
```

## Command-Line Options

```
usage: background_replacer.py [-h] [-o OUTPUT] [-d OUTPUT_DIR]
                              [-f {PNG,JPG,JPEG,WEBP,AVIF}] [--suffix SUFFIX]
                              [-q QUALITY] [-c COLOR] [-b BG_IMAGE] [-m MODEL]
                              [-a] [--mask-only] [--brightness BRIGHTNESS]
                              [--contrast CONTRAST] [--sharpness SHARPNESS]
                              [--feather FEATHER] [--width WIDTH] [--height HEIGHT]
                              [--scale SCALE] [--no-aspect]
                              input [input ...]

Advanced background removal and replacement with multiple AI models

positional arguments:
  input                         Input image file(s)

Input/Output options:
  -o OUTPUT, --output OUTPUT    Output file path (for single file)
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
                                Output directory (for multiple files)
  -f {PNG,JPG,JPEG,WEBP,AVIF}, --format {PNG,JPG,JPEG,WEBP,AVIF}
                                Output format (default: PNG)
  --suffix SUFFIX               Suffix for output files (default: _no_bg)
  -q QUALITY, --quality QUALITY Output quality for lossy formats JPG/WEBP/AVIF (1-100, default: 90)

Background options:
  -c COLOR, --color COLOR       Background color (hex like #FFFFFF, RGB like 255,255,255,
                                or name like white)
  -b BG_IMAGE, --bg-image BG_IMAGE
                                Background image file

Model and processing options:
  -m MODEL, --model MODEL       AI model for background removal (default: u2net)
                                Available: u2net, u2netp, u2net_human_seg, u2net_cloth_seg,
                                silueta, isnet-general-use, isnet-anime, birefnet-general,
                                birefnet-general-lite, birefnet-portrait, birefnet-massive,
                                sam, bria-rmbg
  -a, --alpha-matting           Enable alpha matting for better edge refinement
  --mask-only                   Output only the segmentation mask

Image enhancement options:
  --brightness BRIGHTNESS       Brightness adjustment (0.0=black, 1.0=original, 2.0=double)
  --contrast CONTRAST           Contrast adjustment (0.0=gray, 1.0=original, 2.0=double)
  --sharpness SHARPNESS         Sharpness adjustment (0.0=blurred, 1.0=original, 2.0=sharper)
  --feather FEATHER             Edge feathering in pixels (0=no feathering)

Color filter options:
  --filter {warm,cool,cold,sepia,vintage,vibrant,muted}
                                Apply color filter preset
  --saturation SATURATION       Saturation adjustment (0.0=grayscale, 1.0=original, 2.0=double)

Resize options:
  --width WIDTH                 Resize to specific width in pixels (maintains aspect ratio)
  --height HEIGHT               Resize to specific height in pixels (maintains aspect ratio)
  --scale SCALE                 Resize by scale factor (e.g., 0.5 for 50%, 2.0 for 200%)
  --no-aspect                   Do not maintain aspect ratio when both width and height specified

Web optimization options:
  --progressive                 Enable progressive JPEG encoding for faster web loading
  --strip-metadata              Remove all EXIF/metadata from output for privacy and smaller file size
  --web-optimized               Apply web optimization preset (progressive + metadata stripping)
  --responsive                  Generate responsive image set at multiple breakpoints
  --breakpoints BREAKPOINTS     Custom responsive breakpoints (comma-separated widths, e.g., "640,1024,1920")
```

## Examples

### Example 1: Basic Usage (White Background)
```bash
source venv/bin/activate
python background_replacer.py IMG_0124.CR3 --color white
```

### Example 2: Portrait with Best Quality Model
```bash
source venv/bin/activate
python background_replacer.py portrait.CR3 --model birefnet-portrait --alpha-matting --color white
```

### Example 3: Enhanced Product Photography
```bash
source venv/bin/activate
python background_replacer.py product.jpg \
  --model u2net \
  --alpha-matting \
  --brightness 1.1 \
  --contrast 1.15 \
  --sharpness 1.3 \
  --color white
```

### Example 4: Batch Processing with Consistent Settings
```bash
source venv/bin/activate
python background_replacer.py *.CR3 \
  --model u2net_human_seg \
  --alpha-matting \
  --feather 3 \
  --color "#F5F5F5" \
  --output-dir ./processed
```

### Example 5: Anime Character with Specialized Model
```bash
source venv/bin/activate
python background_replacer.py anime_art.png --model isnet-anime --feather 2 --color transparent
```

### Example 6: Export Segmentation Mask
```bash
source venv/bin/activate
python background_replacer.py IMG_0124.CR3 --model birefnet-general --mask-only -o mask.png
```

### Example 7: Professional Composite with Custom Background
```bash
source venv/bin/activate
python background_replacer.py subject.CR3 \
  --model birefnet-portrait \
  --alpha-matting \
  --feather 5 \
  --brightness 1.05 \
  --bg-image studio_background.jpg \
  -o final_composite.png
```

### Example 8: Web-Optimized Export (WebP)
```bash
source venv/bin/activate
python background_replacer.py product.CR3 \
  --model u2net \
  --alpha-matting \
  --width 1200 \
  --format WEBP \
  --quality 85 \
  --color white
```

### Example 9: Next-Gen AVIF for Best Compression
```bash
source venv/bin/activate
python background_replacer.py portrait.jpg \
  --model birefnet-portrait \
  --alpha-matting \
  --width 1920 \
  --format AVIF \
  --quality 80 \
  -o optimized_portrait.avif
```

### Example 10: Create Multiple Sizes for Responsive Web
```bash
source venv/bin/activate
# Full size
python background_replacer.py product.CR3 --width 1920 --format WEBP --quality 90 -o product_full.webp

# Medium size
python background_replacer.py product.CR3 --width 1200 --format WEBP --quality 85 -o product_medium.webp

# Small/thumbnail
python background_replacer.py product.CR3 --width 600 --format WEBP --quality 80 -o product_small.webp

# Tiny thumbnail
python background_replacer.py product.CR3 --scale 0.2 --format JPG --quality 75 -o product_thumb.jpg
```

### Example 11: Batch Export in Multiple Formats
```bash
source venv/bin/activate
# Export as PNG (lossless, for editing)
python background_replacer.py *.CR3 --format PNG --output-dir ./png

# Export as WebP (web, with transparency)
python background_replacer.py *.CR3 --format WEBP --quality 85 --output-dir ./webp

# Export as AVIF (smallest, modern browsers)
python background_replacer.py *.CR3 --format AVIF --quality 80 --output-dir ./avif

# Export as JPG (compatibility, no transparency)
python background_replacer.py *.CR3 --format JPG --quality 90 --color white --output-dir ./jpg
```

## Current Directory Files

```
IMG_0124.CR3 (25M)
IMG_0137.CR3 (25M)
IMG_0150.CR3 (12M)
IMG_0159.CR3 (12M)
IMG_0167.CR3 (26M)
IMG_0175.CR3 (26M)
```

## Workflow

1. **Image Reading**
   - Script detects file format
   - RAW files are processed using rawpy
   - Standard formats use Pillow

2. **Background Removal**
   - Image is sent to rembg AI model
   - U2-Net neural network identifies subject
   - Alpha channel mask is generated

3. **Background Replacement**
   - New background is created (color or image)
   - Background is resized to match foreground
   - Foreground is composited using alpha blending

4. **Output**
   - Image is converted to target format
   - File is saved with specified naming convention

## Troubleshooting

### Virtual Environment Not Activated
**Error**: `ModuleNotFoundError: No module named 'rawpy'`

**Solution**: Activate the virtual environment:
```bash
source venv/bin/activate
```

### Missing onnxruntime Backend
**Error**: `No onnxruntime backend found`

**Solution**: Install rembg with CPU support:
```bash
source venv/bin/activate
pip install "rembg[cpu]"
```

### First Run Takes Longer
The first time you run the script, it will download the AI model (~176MB). This is normal and only happens once. Subsequent runs will be much faster.

### Out of Memory
For very large images, you may need more RAM. Consider:
- Processing images one at a time instead of batch processing
- Reducing image resolution before processing
- Using a machine with more memory

## Performance Notes

- **First run**: 30-60 seconds (includes model download)
- **Subsequent runs**: 10-20 seconds per image (depending on size)
- **Batch processing**: More efficient than processing individually
- **RAW files**: Slightly slower than JPG/PNG due to RAW conversion

## Technical Stack

- **Python 3.12**: Programming language
- **rawpy 0.25.1**: RAW file processing (wraps LibRaw)
- **Pillow 12.1.0**: Image manipulation
- **rembg 2.0.72**: AI background removal framework
- **onnxruntime**: Neural network inference engine
- **U2-Net**: Deep learning model for salient object detection
- **NumPy**: Array operations for image data
- **scikit-image**: Image processing utilities

## License

This is a personal tool for image processing. The underlying libraries have their own licenses:
- Pillow: HPND License
- rawpy: MIT License
- rembg: MIT License

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify virtual environment is activated
3. Ensure all dependencies are installed correctly
4. Check that input files exist and are readable

## Future Enhancements

Potential features for future versions:
- GPU acceleration support
- Multiple AI model options
- Edge refinement controls
- Preview mode before processing
- GUI interface
- Cloud processing option

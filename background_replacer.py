#!/usr/bin/env python3
"""
Background Replacement Script - Advanced Edition
Removes backgrounds from images using multiple AI models and replaces them
with a solid color or another image. Includes advanced image processing features.
Supports CR3 (Canon RAW), JPG, PNG, and other common formats.

Author: Radko Yordanov
"""

import os
import sys
import argparse
from pathlib import Path
import rawpy
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove, new_session


def read_cr3_image(file_path):
    """Read CR3 (Canon RAW) file and convert to RGB image."""
    print(f"Reading CR3 file: {file_path}")
    with rawpy.imread(file_path) as raw:
        rgb = raw.postprocess()
    return Image.fromarray(rgb)


def read_image(file_path):
    """Read image file (supports CR3, JPG, PNG, etc.)."""
    file_path = Path(file_path)

    if file_path.suffix.lower() in ['.cr3', '.cr2', '.nef', '.arw', '.dng']:
        return read_cr3_image(str(file_path))
    else:
        return Image.open(file_path)


def remove_background(image, model='u2net', alpha_matting=False, mask_only=False):
    """Remove background from image using AI model.

    Args:
        image: PIL Image object
        model: Model name (u2net, u2netp, u2net_human_seg, isnet-general-use,
               birefnet-general, birefnet-portrait, etc.)
        alpha_matting: Enable alpha matting for better edge refinement
        mask_only: Return only the mask without background removal

    Returns:
        PIL Image with transparent background or mask
    """
    print(f"Removing background using model: {model}")
    if alpha_matting:
        print("  - Alpha matting enabled for edge refinement")

    # Convert PIL Image to bytes
    import io
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create session with specified model
    try:
        session = new_session(model)
        print(f"  - Model loaded successfully")
    except Exception as e:
        print(f"  - Warning: Could not load model '{model}': {e}")
        print(f"  - Falling back to default model 'u2net'")
        session = new_session('u2net')

    # Remove background with options
    output = remove(
        img_byte_arr,
        session=session,
        alpha_matting=alpha_matting,
        only_mask=mask_only
    )

    # Convert back to PIL Image
    return Image.open(io.BytesIO(output))


def resize_image(image, width=None, height=None, scale=None, maintain_aspect=True):
    """Resize image with various options.

    Args:
        image: PIL Image object
        width: Target width in pixels (None to auto-calculate)
        height: Target height in pixels (None to auto-calculate)
        scale: Scale factor (e.g., 0.5 for 50%, 2.0 for 200%)
        maintain_aspect: Maintain aspect ratio when width or height specified

    Returns:
        Resized PIL Image
    """
    original_size = image.size

    if scale:
        # Scale based on factor
        new_width = int(original_size[0] * scale)
        new_height = int(original_size[1] * scale)
        print(f"  - Resizing by scale {scale}: {original_size[0]}x{original_size[1]} -> {new_width}x{new_height}")
    elif width and height:
        # Both dimensions specified
        if maintain_aspect:
            # Fit within dimensions, maintaining aspect ratio
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
            print(f"  - Resizing to fit {width}x{height} (aspect maintained): {original_size[0]}x{original_size[1]} -> {image.size[0]}x{image.size[1]}")
            return image
        else:
            # Exact dimensions (may distort)
            new_width = width
            new_height = height
            print(f"  - Resizing to exact {width}x{height} (aspect NOT maintained)")
    elif width:
        # Width specified, calculate height to maintain aspect
        aspect_ratio = original_size[1] / original_size[0]
        new_width = width
        new_height = int(width * aspect_ratio)
        print(f"  - Resizing to width {width}px (aspect maintained): {original_size[0]}x{original_size[1]} -> {new_width}x{new_height}")
    elif height:
        # Height specified, calculate width to maintain aspect
        aspect_ratio = original_size[0] / original_size[1]
        new_width = int(height * aspect_ratio)
        new_height = height
        print(f"  - Resizing to height {height}px (aspect maintained): {original_size[0]}x{original_size[1]} -> {new_width}x{new_height}")
    else:
        # No resize needed
        return image

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def apply_color_filter(image, filter_type=None, saturation=1.0):
    """Apply color filters and adjustments.

    Args:
        image: PIL Image object
        filter_type: Filter preset (warm, cool, cold, sepia, vintage, vibrant, muted)
        saturation: Saturation factor (0.0=grayscale, 1.0=original, >1.0=more saturated)

    Returns:
        Filtered PIL Image
    """
    if not filter_type and saturation == 1.0:
        return image

    filtered = image.copy()

    # Apply preset color filters
    if filter_type:
        print(f"  - Applying {filter_type} filter")

        # Convert to RGB for color operations (preserve alpha if exists)
        has_alpha = filtered.mode == 'RGBA'
        if has_alpha:
            alpha = filtered.split()[3]
            filtered = filtered.convert('RGB')

        # Get image data as numpy array for color manipulation
        img_array = np.array(filtered, dtype=np.float32)

        if filter_type == 'warm':
            # Increase red and yellow tones, decrease blue
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.15, 0, 255)  # Red +15%
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.08, 0, 255)  # Green +8%
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.85, 0, 255)  # Blue -15%

        elif filter_type in ['cool', 'cold']:
            # Increase blue tones, decrease red
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.85, 0, 255)  # Red -15%
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 0.95, 0, 255)  # Green -5%
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.15, 0, 255)  # Blue +15%

        elif filter_type == 'sepia':
            # Classic sepia tone
            r = img_array[:, :, 0]
            g = img_array[:, :, 1]
            b = img_array[:, :, 2]

            img_array[:, :, 0] = np.clip(r * 0.393 + g * 0.769 + b * 0.189, 0, 255)
            img_array[:, :, 1] = np.clip(r * 0.349 + g * 0.686 + b * 0.168, 0, 255)
            img_array[:, :, 2] = np.clip(r * 0.272 + g * 0.534 + b * 0.131, 0, 255)

        elif filter_type == 'vintage':
            # Vintage film look: slight sepia + reduced contrast + vignette effect
            r = img_array[:, :, 0]
            g = img_array[:, :, 1]
            b = img_array[:, :, 2]

            # Sepia-like tone
            img_array[:, :, 0] = np.clip(r * 0.9 + 30, 0, 255)
            img_array[:, :, 1] = np.clip(g * 0.85 + 20, 0, 255)
            img_array[:, :, 2] = np.clip(b * 0.7 + 10, 0, 255)

        elif filter_type == 'vibrant':
            # Increase all colors slightly for vibrant look
            img_array = np.clip(img_array * 1.12, 0, 255)

        elif filter_type == 'muted':
            # Decrease saturation and add slight gray
            mean_val = np.mean(img_array, axis=2, keepdims=True)
            img_array = img_array * 0.7 + mean_val * 0.3

        # Convert back to PIL Image
        filtered = Image.fromarray(img_array.astype(np.uint8), mode='RGB')

        # Restore alpha channel if it existed
        if has_alpha:
            filtered = filtered.convert('RGBA')
            filtered.putalpha(alpha)

    # Apply saturation adjustment
    if saturation != 1.0:
        print(f"  - Adjusting saturation: {saturation}")

        # Ensure RGB mode for color operations
        has_alpha = filtered.mode == 'RGBA'
        if has_alpha:
            alpha = filtered.split()[3]
            rgb = filtered.convert('RGB')
        else:
            rgb = filtered if filtered.mode == 'RGB' else filtered.convert('RGB')

        enhancer = ImageEnhance.Color(rgb)
        rgb = enhancer.enhance(saturation)

        if has_alpha:
            filtered = rgb.convert('RGBA')
            filtered.putalpha(alpha)
        else:
            filtered = rgb

    return filtered


def enhance_image(image, brightness=1.0, contrast=1.0, sharpness=1.0, feather=0):
    """Apply image enhancements.

    Args:
        image: PIL Image object
        brightness: Brightness factor (0.0=black, 1.0=original, >1.0=brighter)
        contrast: Contrast factor (0.0=gray, 1.0=original, >1.0=more contrast)
        sharpness: Sharpness factor (0.0=blurred, 1.0=original, >1.0=sharper)
        feather: Edge feathering amount in pixels (0=no feathering)

    Returns:
        Enhanced PIL Image
    """
    enhanced = image.copy()

    # Apply enhancements if not default values
    if brightness != 1.0:
        print(f"  - Adjusting brightness: {brightness}")
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(brightness)

    if contrast != 1.0:
        print(f"  - Adjusting contrast: {contrast}")
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(contrast)

    if sharpness != 1.0:
        print(f"  - Adjusting sharpness: {sharpness}")
        enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = enhancer.enhance(sharpness)

    # Apply edge feathering (blur the alpha channel)
    if feather > 0 and enhanced.mode == 'RGBA':
        print(f"  - Feathering edges: {feather}px")
        # Extract alpha channel
        r, g, b, a = enhanced.split()
        # Blur the alpha channel
        a = a.filter(ImageFilter.GaussianBlur(radius=feather))
        # Recombine
        enhanced = Image.merge('RGBA', (r, g, b, a))

    return enhanced


def replace_background(foreground_image, background_color=None, background_image=None):
    """Replace background with solid color or another image."""

    # Ensure foreground has alpha channel
    if foreground_image.mode != 'RGBA':
        foreground_image = foreground_image.convert('RGBA')

    # Create background
    if background_image:
        print(f"Using background image: {background_image}")
        bg = Image.open(background_image).convert('RGBA')
        # Resize background to match foreground
        bg = bg.resize(foreground_image.size, Image.Resampling.LANCZOS)
    elif background_color:
        print(f"Using background color: {background_color}")
        bg = Image.new('RGBA', foreground_image.size, background_color)
    else:
        # Default white background
        bg = Image.new('RGBA', foreground_image.size, (255, 255, 255, 255))

    # Composite foreground over background
    result = Image.alpha_composite(bg, foreground_image)

    return result


def process_image(input_path, output_path, background_color=None, background_image=None,
                  output_format='PNG', model='u2net', alpha_matting=False,
                  mask_only=False, brightness=1.0, contrast=1.0, sharpness=1.0,
                  feather=0, resize_width=None, resize_height=None, resize_scale=None,
                  maintain_aspect=True, quality=90, color_filter=None, saturation=1.0,
                  progressive=False, strip_metadata=False):
    """Process a single image: remove and replace background with enhancements.

    Args:
        input_path: Path to input image
        output_path: Path to output image
        background_color: Background color tuple (R,G,B,A)
        background_image: Path to background image
        output_format: Output format (PNG, JPG, JPEG, WEBP, AVIF)
        model: AI model name for background removal
        alpha_matting: Enable alpha matting for edge refinement
        mask_only: Output only the segmentation mask
        brightness: Brightness enhancement factor
        contrast: Contrast enhancement factor
        sharpness: Sharpness enhancement factor
        feather: Edge feathering amount in pixels
        resize_width: Target width in pixels
        resize_height: Target height in pixels
        resize_scale: Scale factor (0.5 = 50%, 2.0 = 200%)
        maintain_aspect: Maintain aspect ratio when resizing
        quality: Output quality for lossy formats (1-100)
        color_filter: Color filter preset (warm, cool, cold, sepia, vintage, vibrant, muted)
        saturation: Saturation adjustment factor

    Returns:
        Path to output file
    """
    print(f"\n{'='*60}")
    print(f"Processing: {input_path}")
    print(f"{'='*60}")

    # Read image
    image = read_image(input_path)

    # Remove background
    no_bg_image = remove_background(image, model=model, alpha_matting=alpha_matting,
                                    mask_only=mask_only)

    # If mask only, save and return
    if mask_only:
        print(f"Saving mask to: {output_path}")
        no_bg_image.save(output_path, format=output_format)
        return output_path

    # Apply color filters
    if color_filter or saturation != 1.0:
        print("Applying color filters...")
        no_bg_image = apply_color_filter(no_bg_image, color_filter, saturation)

    # Apply enhancements
    if brightness != 1.0 or contrast != 1.0 or sharpness != 1.0 or feather > 0:
        print("Applying enhancements...")
        no_bg_image = enhance_image(no_bg_image, brightness, contrast, sharpness, feather)

    # Replace background
    final_image = replace_background(no_bg_image, background_color, background_image)

    # Apply resizing if specified
    if resize_width or resize_height or resize_scale:
        print("Resizing image...")
        final_image = resize_image(final_image, resize_width, resize_height,
                                   resize_scale, maintain_aspect)

    # Prepare format-specific save options
    save_kwargs = {}
    output_format_upper = output_format.upper()

    # Normalize format name for Pillow (requires 'JPEG' not 'JPG')
    save_format = 'JPEG' if output_format_upper in ['JPG', 'JPEG'] else output_format_upper

    # Convert image based on format requirements
    if output_format_upper in ['JPG', 'JPEG']:
        final_image = final_image.convert('RGB')
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
        if progressive:
            save_kwargs['progressive'] = True
            print("  - Progressive JPEG enabled")
    elif output_format_upper == 'WEBP':
        # WebP supports both RGB and RGBA
        save_kwargs['quality'] = quality
        save_kwargs['method'] = 6  # Better compression
    elif output_format_upper == 'AVIF':
        # AVIF supports both RGB and RGBA
        save_kwargs['quality'] = quality
        save_kwargs['speed'] = 6  # Balance between speed and compression
    elif output_format_upper == 'PNG':
        save_kwargs['optimize'] = True

    # Strip metadata if requested
    if strip_metadata:
        save_kwargs['exif'] = b''
        print("  - Metadata stripped for privacy/optimization")

    # Save result
    print(f"Saving as {output_format_upper} (quality: {quality})...")
    final_image.save(output_path, format=save_format, **save_kwargs)
    print(f"Saved to: {output_path}")

    return output_path


def generate_responsive_images(input_path, output_dir, background_color=None, background_image=None,
                               output_format='WEBP', model='u2net', alpha_matting=False,
                               brightness=1.0, contrast=1.0, sharpness=1.0, feather=0,
                               color_filter=None, saturation=1.0, quality=90,
                               breakpoints=None, progressive=False, strip_metadata=False):
    """Generate responsive image set at multiple breakpoints.

    Args:
        input_path: Path to input image
        output_dir: Output directory for responsive images
        breakpoints: List of widths for responsive images
        ... (other parameters same as process_image)

    Returns:
        List of generated file paths
    """
    if breakpoints is None:
        # Standard responsive breakpoints for web (mobile to 4K)
        breakpoints = [640, 768, 1024, 1280, 1920, 2560]

    print(f"\n{'='*60}")
    print(f"Generating responsive images: {input_path}")
    print(f"Breakpoints: {breakpoints}")
    print(f"{'='*60}")

    # Read and process image once
    image = read_image(input_path)
    no_bg_image = remove_background(image, model=model, alpha_matting=alpha_matting, mask_only=False)

    # Apply color filters
    if color_filter or saturation != 1.0:
        print("Applying color filters...")
        no_bg_image = apply_color_filter(no_bg_image, color_filter, saturation)

    # Apply enhancements
    if brightness != 1.0 or contrast != 1.0 or sharpness != 1.0 or feather > 0:
        print("Applying enhancements...")
        no_bg_image = enhance_image(no_bg_image, brightness, contrast, sharpness, feather)

    # Replace background
    final_image = replace_background(no_bg_image, background_color, background_image)

    # Generate images at each breakpoint
    generated_files = []
    input_name = Path(input_path).stem
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    for width in breakpoints:
        # Skip if original is smaller than breakpoint
        if final_image.size[0] < width:
            print(f"  - Skipping {width}px (original is {final_image.size[0]}px)")
            continue

        # Resize for this breakpoint
        resized = resize_image(final_image.copy(), width=width)

        # Generate filename with width suffix
        output_name = f"{input_name}_{width}w.{output_format.lower()}"
        output_path = output_dir_path / output_name

        # Prepare save options
        save_kwargs = {'optimize': True}
        output_format_upper = output_format.upper()

        # Normalize format name for Pillow (requires 'JPEG' not 'JPG')
        save_format = 'JPEG' if output_format_upper in ['JPG', 'JPEG'] else output_format_upper

        # Format-specific options
        if output_format_upper in ['JPG', 'JPEG']:
            resized_save = resized.convert('RGB')
            save_kwargs['quality'] = quality
            if progressive:
                save_kwargs['progressive'] = True
                print(f"  - {width}px: Progressive JPEG enabled")
        elif output_format_upper == 'WEBP':
            resized_save = resized
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 6
        elif output_format_upper == 'AVIF':
            resized_save = resized
            save_kwargs['quality'] = quality
            save_kwargs['speed'] = 6
        elif output_format_upper == 'PNG':
            resized_save = resized
        else:
            resized_save = resized

        # Strip metadata if requested
        if strip_metadata:
            save_kwargs['exif'] = b''

        # Save
        resized_save.save(output_path, format=save_format, **save_kwargs)
        print(f"  - Generated: {output_name} ({resized.size[0]}x{resized.size[1]})")
        generated_files.append(str(output_path))

    return generated_files


def parse_color(color_string):
    """Parse color string to RGBA tuple."""
    if color_string.startswith('#'):
        # Hex color
        color_string = color_string.lstrip('#')
        if len(color_string) == 6:
            return tuple(int(color_string[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        elif len(color_string) == 8:
            return tuple(int(color_string[i:i+2], 16) for i in (0, 2, 4, 6))
    else:
        # Named colors or comma-separated RGB/RGBA
        if ',' in color_string:
            values = [int(v.strip()) for v in color_string.split(',')]
            if len(values) == 3:
                return tuple(values) + (255,)
            elif len(values) == 4:
                return tuple(values)

    # Common named colors
    colors = {
        'white': (255, 255, 255, 255),
        'black': (0, 0, 0, 255),
        'red': (255, 0, 0, 255),
        'green': (0, 255, 0, 255),
        'blue': (0, 0, 255, 255),
        'yellow': (255, 255, 0, 255),
        'cyan': (0, 255, 255, 255),
        'magenta': (255, 0, 255, 255),
    }

    return colors.get(color_string.lower(), (255, 255, 255, 255))


def main():
    parser = argparse.ArgumentParser(
        description='Advanced background removal and replacement with multiple AI models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with white background
  python background_replacer.py IMG_0124.CR3

  # Use different AI model (portrait optimized)
  python background_replacer.py IMG_0124.CR3 --model birefnet-portrait

  # Enable alpha matting for refined edges
  python background_replacer.py IMG_0124.CR3 --alpha-matting

  # Apply image enhancements
  python background_replacer.py IMG_0124.CR3 --brightness 1.2 --contrast 1.1 --sharpness 1.3

  # Feather edges for smooth transition
  python background_replacer.py IMG_0124.CR3 --feather 5

  # Output only the segmentation mask
  python background_replacer.py IMG_0124.CR3 --mask-only

  # Batch processing with custom model
  python background_replacer.py *.CR3 --model u2net_human_seg --output-dir ./processed

  # Export as WebP with 85% quality
  python background_replacer.py IMG_0124.CR3 --format WEBP --quality 85

  # Export as AVIF (modern format with best compression)
  python background_replacer.py IMG_0124.CR3 --format AVIF --quality 80

  # Resize to specific width (maintains aspect ratio)
  python background_replacer.py IMG_0124.CR3 --width 1920

  # Resize by 50%
  python background_replacer.py IMG_0124.CR3 --scale 0.5

  # Resize to exact dimensions (no aspect ratio)
  python background_replacer.py IMG_0124.CR3 --width 800 --height 600 --no-aspect

  # Apply warm filter for golden hour look
  python background_replacer.py IMG_0124.CR3 --filter warm

  # Apply cool filter for winter/cold feel
  python background_replacer.py IMG_0124.CR3 --filter cool

  # Apply sepia tone for vintage look
  python background_replacer.py IMG_0124.CR3 --filter sepia

  # Increase saturation for vivid colors
  python background_replacer.py IMG_0124.CR3 --saturation 1.5

  # Desaturate for muted/monochrome look
  python background_replacer.py IMG_0124.CR3 --saturation 0.5

Available Models:
  General: u2net (default), u2netp, silueta, isnet-general-use
  Human/Portrait: u2net_human_seg, birefnet-portrait
  Specialized: u2net_cloth_seg, isnet-anime
  Advanced: birefnet-general, birefnet-general-lite, birefnet-massive
  Professional: sam, bria-rmbg

Available Formats:
  PNG: Lossless, transparency support (best for graphics)
  JPG/JPEG: Lossy compression, no transparency (photos)
  WEBP: Modern format, transparency support, excellent compression
  AVIF: Next-gen format, best compression, transparency support
        """
    )

    # Input/Output arguments
    parser.add_argument('input', nargs='+', help='Input image file(s)')
    parser.add_argument('-o', '--output', help='Output file path (for single file)')
    parser.add_argument('-d', '--output-dir', help='Output directory (for multiple files)')
    parser.add_argument('-f', '--format', default='PNG', choices=['PNG', 'JPG', 'JPEG', 'WEBP', 'AVIF'],
                        help='Output format (default: PNG)')
    parser.add_argument('--suffix', default='_no_bg', help='Suffix for output files (default: _no_bg)')
    parser.add_argument('-q', '--quality', type=int, default=90,
                        help='Output quality for lossy formats JPG/WEBP/AVIF (1-100, default: 90)')

    # Background options
    parser.add_argument('-c', '--color', help='Background color (hex like #FFFFFF or RGB like 255,255,255 or name like white)')
    parser.add_argument('-b', '--bg-image', help='Background image file')

    # Model and processing options
    parser.add_argument('-m', '--model', default='u2net',
                        help='AI model for background removal (default: u2net)')
    parser.add_argument('-a', '--alpha-matting', action='store_true',
                        help='Enable alpha matting for better edge refinement')
    parser.add_argument('--mask-only', action='store_true',
                        help='Output only the segmentation mask')

    # Image enhancement options
    parser.add_argument('--brightness', type=float, default=1.0,
                        help='Brightness adjustment (0.0=black, 1.0=original, 2.0=double, default: 1.0)')
    parser.add_argument('--contrast', type=float, default=1.0,
                        help='Contrast adjustment (0.0=gray, 1.0=original, 2.0=double, default: 1.0)')
    parser.add_argument('--sharpness', type=float, default=1.0,
                        help='Sharpness adjustment (0.0=blurred, 1.0=original, 2.0=sharper, default: 1.0)')
    parser.add_argument('--feather', type=int, default=0,
                        help='Edge feathering in pixels (default: 0, no feathering)')

    # Color filter options
    parser.add_argument('--filter', choices=['warm', 'cool', 'cold', 'sepia', 'vintage', 'vibrant', 'muted'],
                        help='Apply color filter preset')
    parser.add_argument('--saturation', type=float, default=1.0,
                        help='Saturation adjustment (0.0=grayscale, 1.0=original, 2.0=double saturated, default: 1.0)')

    # Resize options
    parser.add_argument('--width', type=int, default=None,
                        help='Resize to specific width in pixels (maintains aspect ratio)')
    parser.add_argument('--height', type=int, default=None,
                        help='Resize to specific height in pixels (maintains aspect ratio)')
    parser.add_argument('--scale', type=float, default=None,
                        help='Resize by scale factor (e.g., 0.5 for 50%%, 2.0 for 200%%)')
    parser.add_argument('--no-aspect', action='store_true',
                        help='Do not maintain aspect ratio when both width and height specified')

    # Web optimization options
    parser.add_argument('--progressive', action='store_true',
                        help='Enable progressive JPEG encoding for faster web loading')
    parser.add_argument('--strip-metadata', action='store_true',
                        help='Remove all EXIF/metadata from output for privacy and smaller file size')
    parser.add_argument('--web-optimized', action='store_true',
                        help='Apply web optimization preset (progressive JPEG, strip metadata, optimized compression)')
    parser.add_argument('--responsive', action='store_true',
                        help='Generate responsive image set at multiple breakpoints')
    parser.add_argument('--breakpoints', type=str,
                        help='Custom responsive breakpoints as comma-separated widths (e.g., "640,1024,1920")')

    args = parser.parse_args()

    # Parse background color
    bg_color = None
    if args.color:
        bg_color = parse_color(args.color)
        print(f"Background color: {bg_color}")

    # Apply web-optimized preset
    if args.web_optimized:
        args.progressive = True
        args.strip_metadata = True
        print("Web optimization preset enabled (progressive + metadata stripping)")

    # Parse responsive breakpoints
    breakpoints = None
    if args.breakpoints:
        try:
            breakpoints = [int(w.strip()) for w in args.breakpoints.split(',')]
            print(f"Custom breakpoints: {breakpoints}")
        except ValueError:
            print("Error: Invalid breakpoints format. Use comma-separated integers (e.g., '640,1024,1920')")
            sys.exit(1)

    # Process files
    input_files = []
    for pattern in args.input:
        from glob import glob
        matched = glob(pattern)
        if matched:
            input_files.extend(matched)
        elif os.path.exists(pattern):
            input_files.append(pattern)

    if not input_files:
        print("Error: No input files found!")
        sys.exit(1)

    print(f"Found {len(input_files)} file(s) to process")

    # Process each file
    for input_file in input_files:
        try:
            # Handle responsive image generation
            if args.responsive:
                # Determine output directory for responsive images
                if args.output_dir:
                    output_dir = Path(args.output_dir)
                else:
                    output_dir = Path(input_file).parent / "responsive"

                output_dir.mkdir(parents=True, exist_ok=True)

                # Generate responsive images
                generated_files = generate_responsive_images(
                    input_file,
                    str(output_dir),
                    background_color=bg_color,
                    background_image=args.bg_image,
                    output_format=args.format,
                    model=args.model,
                    alpha_matting=args.alpha_matting,
                    brightness=args.brightness,
                    contrast=args.contrast,
                    sharpness=args.sharpness,
                    feather=args.feather,
                    color_filter=args.filter,
                    saturation=args.saturation,
                    quality=args.quality,
                    breakpoints=breakpoints,
                    progressive=args.progressive,
                    strip_metadata=args.strip_metadata
                )
                print(f"Generated {len(generated_files)} responsive images in {output_dir}")
            else:
                # Regular single image processing
                # Determine output path
                if len(input_files) == 1 and args.output:
                    output_path = args.output
                else:
                    input_path = Path(input_file)
                    output_name = f"{input_path.stem}{args.suffix}.{args.format.lower()}"

                    if args.output_dir:
                        output_dir = Path(args.output_dir)
                        output_dir.mkdir(parents=True, exist_ok=True)
                        output_path = output_dir / output_name
                    else:
                        output_path = input_path.parent / output_name

                # Process image
                process_image(
                    input_file,
                    str(output_path),
                    background_color=bg_color,
                    background_image=args.bg_image,
                    output_format=args.format,
                    model=args.model,
                    alpha_matting=args.alpha_matting,
                    mask_only=args.mask_only,
                    brightness=args.brightness,
                    contrast=args.contrast,
                    sharpness=args.sharpness,
                    feather=args.feather,
                    resize_width=args.width,
                    resize_height=args.height,
                    resize_scale=args.scale,
                    maintain_aspect=not args.no_aspect,
                    quality=args.quality,
                    color_filter=args.filter,
                    saturation=args.saturation,
                    progressive=args.progressive,
                    strip_metadata=args.strip_metadata
                )

        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n{'='*60}")
    print("Processing complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()

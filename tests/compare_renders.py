#!/usr/bin/env python3
"""
Image comparison tool for HP-35 GUI pixel-perfect rendering.

Uses multiple metrics to compare rendered output with reference image:
- SSIM (Structural Similarity Index) - best for human perception
- MSE (Mean Squared Error) - pixel-level difference
- Color histogram comparison - overall color accuracy
"""

import sys
from PIL import Image, ImageChops, ImageFilter
import numpy as np


def load_and_resize(img_path, target_size=None):
    """Load image and optionally resize to target dimensions."""
    img = Image.open(img_path).convert('RGB')
    if target_size:
        img = img.resize(target_size, Image.Resampling.LANCZOS)
    return img


def calculate_mse(img1, img2):
    """Calculate Mean Squared Error between two images."""
    arr1 = np.array(img1, dtype=np.float64)
    arr2 = np.array(img2, dtype=np.float64)
    mse = np.mean((arr1 - arr2) ** 2)
    return mse


def calculate_ssim_simple(img1, img2):
    """
    Simplified SSIM calculation.
    Returns value between 0 (completely different) and 1 (identical).
    """
    arr1 = np.array(img1, dtype=np.float64)
    arr2 = np.array(img2, dtype=np.float64)

    # Calculate means
    mu1 = np.mean(arr1)
    mu2 = np.mean(arr2)

    # Calculate variances and covariance
    sigma1_sq = np.var(arr1)
    sigma2_sq = np.var(arr2)
    sigma12 = np.mean((arr1 - mu1) * (arr2 - mu2))

    # SSIM constants
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # SSIM formula
    numerator = (2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1**2 + mu2**2 + C1) * (sigma1_sq + sigma2_sq + C2)

    ssim = numerator / denominator
    return max(0, min(1, ssim))


def calculate_color_histogram_distance(img1, img2):
    """
    Calculate color histogram distance (lower is more similar).
    Returns value roughly between 0 (identical) and 1000+ (very different).
    """
    hist1 = np.array(img1.histogram())
    hist2 = np.array(img2.histogram())

    # Normalize histograms
    hist1 = hist1.astype(float) / hist1.sum()
    hist2 = hist2.astype(float) / hist2.sum()

    # Calculate chi-squared distance
    distance = np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + 1e-10))
    return distance


def create_diff_image(img1, img2, amplify=3):
    """Create a difference image showing where images differ."""
    diff = ImageChops.difference(img1, img2)

    # Amplify differences for visibility
    arr = np.array(diff, dtype=np.float64)
    arr = np.clip(arr * amplify, 0, 255).astype(np.uint8)

    return Image.fromarray(arr)


def compare_images(reference_path, test_path, output_diff=None):
    """
    Compare two images and return similarity metrics.

    Returns:
        dict with metrics: ssim (0-1, higher=better), mse (lower=better),
                          hist_dist (lower=better), combined_score (0-100, higher=better)
    """
    # Load images
    ref_img = Image.open(reference_path).convert('RGB')
    test_img = Image.open(test_path).convert('RGB')

    # Get dimensions
    ref_size = ref_img.size
    test_size = test_img.size

    print(f"Reference: {ref_size[0]}×{ref_size[1]}")
    print(f"Test:      {test_size[0]}×{test_size[1]}")

    # Resize test image to match reference if needed
    if ref_size != test_size:
        print(f"Resizing test image to match reference...")
        test_img = test_img.resize(ref_size, Image.Resampling.LANCZOS)

    # Calculate metrics
    mse = calculate_mse(ref_img, test_img)
    ssim = calculate_ssim_simple(ref_img, test_img)
    hist_dist = calculate_color_histogram_distance(ref_img, test_img)

    # Combined score (0-100, higher is better)
    # Weight SSIM heavily as it's most perceptually accurate
    combined_score = (
        ssim * 70 +                          # 70% weight on SSIM
        (1 - min(mse / 10000, 1)) * 20 +    # 20% weight on inverse MSE
        (1 - min(hist_dist / 10, 1)) * 10   # 10% weight on inverse hist distance
    )

    # Create diff image if requested
    if output_diff:
        diff_img = create_diff_image(ref_img, test_img, amplify=5)
        diff_img.save(output_diff)
        print(f"\nDiff image saved: {output_diff}")

    return {
        'ssim': ssim,
        'mse': mse,
        'hist_dist': hist_dist,
        'combined_score': combined_score
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_renders.py <reference.jpg> <test.png> [diff_output.png]")
        sys.exit(1)

    reference = sys.argv[1]
    test = sys.argv[2]
    diff_output = sys.argv[3] if len(sys.argv) > 3 else None

    print("=" * 60)
    print("HP-35 Render Comparison")
    print("=" * 60)

    metrics = compare_images(reference, test, diff_output)

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"SSIM (Structural Similarity):  {metrics['ssim']:.4f}  (1.0 = perfect)")
    print(f"MSE (Mean Squared Error):      {metrics['mse']:.2f}     (0 = perfect)")
    print(f"Histogram Distance:            {metrics['hist_dist']:.2f}     (0 = perfect)")
    print(f"\n{'='*60}")
    print(f"COMBINED SCORE: {metrics['combined_score']:.2f}/100")
    print(f"{'='*60}")

    # Provide interpretation
    if metrics['combined_score'] >= 95:
        print("\n✓ EXCELLENT - Nearly pixel-perfect!")
    elif metrics['combined_score'] >= 85:
        print("\n✓ GOOD - Very close, minor differences")
    elif metrics['combined_score'] >= 70:
        print("\n~ FAIR - Noticeable differences, but recognizable")
    else:
        print("\n✗ POOR - Significant differences remain")

    return 0


if __name__ == '__main__':
    sys.exit(main())

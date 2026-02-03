# Passport-Print-Gen

A professional-grade Python utility to generate print-ready A4 sheets of passport-sized photos (). This tool is optimized for high-resolution photography workflows (Nikon D850/D5) where color accuracy and shadow detail are critical.

## Key Features

* **Professional Tiling**: Generates a standard 5x6 grid (30 photos) on an A4 canvas.
* **Shadow Lift Technology**: Uses a Gamma-style Look-Up Table (LUT) to reveal detail in dark hair and clothing without blowing out skin highlights.
* **Color Profile Preservation**: Full support for **Adobe RGB (1998)** via ICC profile embedding to ensure lab-quality print results.
* **Scissor-Friendly Design**: Includes a generous 60px gutter (gap) between photos for easy manual cutting.
* **High-Res Optimization**: Efficiently handles 45MP+ images using Lanczos resampling and NumPy-accelerated processing.

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/passport-print-gen.git
cd passport-print-gen

```


2. **Create and activate a virtual environment**:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

```


3. **Install dependencies**:
```bash
pip install Pillow numpy

```



## Usage

1. Place your source photo (ideally in 4:5 aspect ratio) in the project folder.
2. Ensure you have the `AdobeRGB1998.icc` profile available if you wish to embed it (usually found in `C:/Windows/System32/spool/drivers/color/` on Windows).
3. Run the script:

```python
from passport_gen import generate_passport_sheet

# Parameters:
# input_path: Your source image
# output_path: Where to save the A4 sheet
# adobe_icc_path: Path to your Adobe RGB profile
# shadow_lift: 1.0 (none) to 1.5 (heavy lift)
generate_passport_sheet("input.jpg", "print_ready.jpg", shadow_lift=1.4)

```

## Technical Specifications

| Parameter | Value |
| --- | --- |
| **Print Resolution** | 300 DPI |
| **Sheet Size** | A4 (210 x 297 mm) |
| **Photo Size** | 35 x 45 mm |
| **Grid** | 5 Columns x 6 Rows |
| **Color Space** | Adobe RGB (1998) Supported |
| **Sampling** | 4:4:4 (Subsampling 0) |

## Git Maintenance

To keep the repository clean, the `.gitignore` is configured to exclude:

* Virtual environments (`venv/`)
* Source/Output images (`*.jpg`, `*.jpeg`)
* Python cache files


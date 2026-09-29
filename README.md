# DARTIS-2019 Land Mask Generation

Generate pixel-level land masks for the DARTIS-2019 Sentinel-1 SAR image patches.

This project uses the geographical coordinates provided in `DARTIS_2019.tab` together with a global land-polygon shapefile to determine which pixels in each SAR image correspond to land.

The generated land masks can then be used as a preprocessing step for oil-spill segmentation, especially for preventing land pixels from interfering with SAR-based oil-slick detection and segmentation.

---

# 1. Overview

The land-mask generation pipeline is:

```text
DARTIS-2019 SAR Image
          |
          v
DARTIS_2019.tab
          |
          |-- Image corner coordinates
          |
          v
Ground Control Points (GCPs)
          |
          v
Global Land Polygon Shapefile
          |
          v
Geographic -> Image Coordinate Transformation
          |
          v
Rasterization
          |
          v
Pixel-level Land Mask

For every input image, a corresponding binary land mask is generated.

Example:

Input:
S1_20191104_033417_033557_VV_8.jpg

Output:
S1_20191104_033417_033557_VV_8_mask.jpg
2. Based on the DARTIS-2019 Repository

This implementation is based on the land-mask generation approach provided in the official DARTIS-2019 repository.

Official DARTIS-2019 repository:

https://github.com/yi-jie-yang/dataset_DARTIS_2019

The official repository contains:

dataset_toolbox.py
img_land_mask.py
structure_dataset.py
other utilities for working with the DARTIS-2019 dataset.

The DARTIS repository describes the structured dataset as:

oil/
    coast/
    water/

no_oil/
    coast/
        c0/
        c1/
        ...
    water/
        c0/
        c1/
        ...

The repository also explains that img_land_mask.py generates land masks corresponding to the image patches.


---

# 3. Dataset

This project expects the DARTIS-2019 image patches and metadata.

The DARTIS dataset contains two major groups:

```text
oil
no_oil

with coastal and water subsets.

For land-mask generation, the important subsets are:

oil/coast
no_oil/coast

because these are the patches where land may be present.

4. Download DARTIS-2019

Download the DARTIS-2019 dataset from the official source:

https://github.com/yi-jie-yang/dataset_DARTIS_2019

The dataset itself is associated with the DARTIS-2019 publication/data release.

The repository also references the PANGAEA dataset:

https://doi.pangaea.de/10.1594/PANGAEA.980773

5. Dataset Directory Structure

The dataset should follow the structured DARTIS format.

Recommended structure:

dataset_structured/
│
├── no_oil/
│   │
│   ├── coast/
│   │   ├── c0/
│   │   │   ├── image1.jpg
│   │   │   ├── image2.jpg
│   │   │   └── ...
│   │   │
│   │   ├── c1/
│   │   │   ├── image1.jpg
│   │   │   └── ...
│   │   │
│   │   ├── c2/
│   │   ├── c3/
│   │   └── c4/
│   │
│   └── water/
│       ├── c0/
│       ├── c1/
│       └── ...
│
└── oil/
    │
    ├── coast/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    │
    └── water/
        ├── image1.jpg
        └── ...
Important

Do not randomly move images between these folders.

The folder structure is meaningful.

For example:

no_oil/coast/c0/

means:

no oil
+
coastal patch
+
coast category 0

while:

oil/coast/

contains oil-containing coastal patches.

The official DARTIS repository describes this structured organization and explains that the folders help distinguish image patches that can otherwise have duplicate patch names.


---

# 6. DARTIS Metadata File

You also need:

```text
DARTIS_2019.tab

Place it in the project root.

The metadata file contains information about the image patches, including geographical information required for land-mask generation.

Important fields include the four image-corner coordinates:

patch_ul_lon
patch_ul_lat

patch_ur_lon
patch_ur_lat

patch_br_lon
patch_br_lat

patch_bl_lon
patch_bl_lat

These coordinates represent:

UL = Upper Left
UR = Upper Right
BR = Bottom Right
BL = Bottom Left

They allow the program to establish the relationship between the image pixels and their geographic coordinates.

7. Land Polygon Shapefile
Where do I get the shapefile?

The official DARTIS repository lists several possible land-mask sources:

OpenStreetMap
GSHHG
Todd Karin Global Land Mask

For this implementation, we recommend the OpenStreetMap land polygons because they are directly available as a global polygon shapefile and fit the workflow used by img_land_mask.py.

Official OpenStreetMap land-polygon download page:

https://osmdata.openstreetmap.de/data/land-polygons.html

The DARTIS repository itself links to this source as one of its recommended land-mask sources.

8. Which OpenStreetMap File Should I Download?

On the OpenStreetMap land-polygons page, several versions are available.

Download:

Format: Shapefile
Projection: WGS84
Large polygons not split

In other words:

WGS84 + Large polygons not split

Do NOT use the Mercator version for this implementation.

The OpenStreetMap download page currently provides both WGS84 and Mercator versions and both split and unsplit polygon variants. The WGS84 / large-polygons-not-split version is the appropriate choice for this code because the DARTIS metadata provides geographic longitude/latitude coordinates.


---

# 9. Land Shapefile Directory

After downloading the OpenStreetMap land polygon ZIP file, extract it.

Keep all shapefile components together.

For example:

```text
land_polygons/
│
├── land_polygons.shp
├── land_polygons.shx
├── land_polygons.dbf
├── land_polygons.prj
└── ...

The exact filename may vary depending on the downloaded release.

The important point is that the .shp, .shx, .dbf, .prj, etc. remain in the same directory.

A shapefile is not a single file. The associated files are required by GeoPandas/GDAL to correctly read the dataset.

10. Complete Project Structure

After downloading everything, your project should look approximately like this:

DARTIS-land-mask/
│
├── dataset_structured/
│   │
│   ├── no_oil/
│   │   ├── coast/
│   │   │   ├── c0/
│   │   │   ├── c1/
│   │   │   ├── c2/
│   │   │   ├── c3/
│   │   │   └── c4/
│   │   │
│   │   └── water/
│   │       ├── c0/
│   │       ├── c1/
│   │       └── ...
│   │
│   └── oil/
│       ├── coast/
│       └── water/
│
├── land_polygons/
│   ├── land_polygons.shp
│   ├── land_polygons.shx
│   ├── land_polygons.dbf
│   ├── land_polygons.prj
│   └── ...
│
├── DARTIS_2019.tab
│
├── dataset_toolbox.py
├── img_land_mask.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── patches_masked/
    └── generated automatically
11. Python Requirements

Recommended Python version:

Python 3.9+

The project requires:

numpy
pandas
Pillow
geopandas
rasterio

Install all dependencies using:

pip install -r requirements.txt

The requirements.txt file should contain:

numpy
pandas
Pillow
geopandas
rasterio
12. Recommended Virtual Environment

It is recommended to create a separate virtual environment.

Windows

Create the environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Linux / macOS

Create the environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
13. Important Note About GeoPandas and Rasterio

geopandas and rasterio depend on geospatial libraries such as:

GDAL
PROJ
GEOS
Shapely

If installation using pip causes problems, use Conda/Miniconda.

Example:

conda create -n dartis-land python=3.10
conda activate dartis-land

conda install -c conda-forge \
    numpy pandas pillow geopandas rasterio

Then run the program inside the environment.

14. Configure the Script

Open:

img_land_mask.py

Set the dataset directory:

dir_dataset = "dataset_structured"

Because the dataset is already in the structured format, set:

structured_tf = True

Set the metadata file:

data_tab = "DARTIS_2019.tab"

Set the land shapefile:

landpolygons_file = "land_polygons/land_polygons.shp"

If your downloaded shapefile has a different name, use the actual .shp filename.

For example:

landpolygons_file = "land_polygons/land-polygons-complete-4326/land_polygons.shp"

depending on the extracted directory structure.

15. Select the Dataset Subsets

For land-mask generation, use:

select_subsets = ["nc", "oc"]

These correspond to:

nc = no_oil / coast
oc = oil / coast

This selects the coastal patches.

Water-only patches generally do not need a land mask.

16. Output Directory

Set:

dir_output = "patches_masked"

The program will create this directory if it does not exist.

17. Generate Only Land Masks

If you only want the land masks:

create_land_mask_tf = True
create_masked_patch_tf = False

This is recommended if the goal is to use the masks later in another segmentation pipeline.

The program will generate:

*_mask.jpg

without creating additional masked SAR images.

18. Recommended Configuration

Your configuration should look like:

####################
### User's Input ###
####################

dir_dataset = "dataset_structured"

structured_tf = True

data_tab = "DARTIS_2019.tab"

landpolygons_file = "land_polygons/land_polygons.shp"

select_subsets = ["nc", "oc"]

dir_output = "patches_masked"

create_land_mask_tf = True

create_masked_patch_tf = False

verbose = True
19. Run the Program

Open a terminal in the project root.

Your terminal should be inside:

DARTIS-land-mask/

Then run:

python img_land_mask.py

The program will:

1. Load DARTIS_2019.tab
        |
        v
2. Select nc and oc subsets
        |
        v
3. Locate the corresponding image files
        |
        v
4. Read image dimensions
        |
        v
5. Read geographic corner coordinates
        |
        v
6. Create Ground Control Points
        |
        v
7. Load relevant land polygons
        |
        v
8. Transform land polygons to image coordinates
        |
        v
9. Rasterize the polygons
        |
        v
10. Save the land mask
20. Expected Output

The output will be stored in:

patches_masked/

For example:

patches_masked/
│
├── S1_20191103_034307_034447_VV_19_mask.jpg
├── S1_20191104_033417_033557_VV_65_mask.jpg
├── S1_20191104_033417_033557_VV_67_mask.jpg
├── S1_20191106_155619_155644_VV_0_mask.jpg
└── ...
21. Image-to-Mask Mapping

The generated mask uses the original image filename.

The code effectively performs:

original_filename + "_mask.jpg"

For example:

Original:

S1_20191104_033417_033557_VV_65.jpg

becomes:

Mask:

S1_20191104_033417_033557_VV_65_mask.jpg

Therefore:

IMAGE                              MASK

image.jpg                     -> image_mask.jpg

The mask can be automatically paired with its original image using the filename.

22. Mask Values

The generated raster is a Boolean land mask.

Conceptually:

1 / True  = LAND
0 / False = NON-LAND

The mask has the same dimensions as the corresponding image.

For example:

SAR image:

1024 x 1024


Land mask:

1024 x 1024
23. How the Land Mask Is Created

The script obtains the image corner coordinates from:

DARTIS_2019.tab

The four corners are:

Upper Left
Upper Right
Bottom Right
Bottom Left

These coordinates are converted into Ground Control Points.

Conceptually:

Geographic coordinates
        |
        v
GCP transformation
        |
        v
Image pixel coordinates
        |
        v
Land polygons
        |
        v
Rasterization
        |
        v
Binary land mask

The relevant operation is:

rasterio.features.rasterize(...)

which converts the geographic land polygons into pixels matching the dimensions of the SAR image.

24. Verify the Generated Masks

Before using the masks for oil segmentation, visually inspect several examples.

For each image:

Original SAR image
        +
Generated land mask

The land area in the mask should correspond to the coastline in the original SAR image.

Example:

SAR IMAGE                    LAND MASK

┌─────────────────┐          ┌─────────────────┐
│                 │          │                 │
│      SEA        │          │       0         │
│                 │          │                 │
│─────────────────│          │─────────────────│
│      LAND       │          │       1         │
└─────────────────┘          └─────────────────┘

Do not proceed to oil segmentation until the masks are correctly aligned.

25. Land Mask vs Oil Mask

The land mask is NOT the oil-spill ground truth.

They have different purposes.

Land mask
1 = land
0 = non-land
Oil mask
1 = oil
0 = non-oil

The land mask is an auxiliary mask used to prevent land pixels from interfering with oil detection/segmentation.

26. Intended Oil Segmentation Pipeline

The land mask can subsequently be used in an oil segmentation pipeline such as:

Sentinel-1 SAR Image
          |
          v
      Land Mask
          |
          v
    Exclude Land
          |
          v
     Median Filter
          |
          v
   CFAR Bright Pixel
       Detection
          |
          v
    σ / μ Analysis
          |
          v
  Discontinuity / Edge
       Detection
          |
          v
      Seed Points
          |
          v
   Region Growing
          |
          v
      Oil Mask

The land mask is particularly useful for preventing coastal land pixels from being interpreted as oil-slick boundaries.

27. Troubleshooting
Problem: File doesn't exist

If you see:

File <filename.jpg> doesn't exist

check:

The image exists.
The filename matches the jpg_file value in DARTIS_2019.tab.
dir_dataset points to the correct dataset directory.
structured_tf is set correctly.

For your structured dataset:

structured_tf = True
Problem: Shapefile cannot be opened

Make sure all shapefile components are together:

.shp
.shx
.dbf
.prj

For example:

land_polygons/
├── land_polygons.shp
├── land_polygons.shx
├── land_polygons.dbf
└── land_polygons.prj

Do not keep only the .shp file.

Problem: rasterio installation fails

Try Conda:

conda install -c conda-forge rasterio geopandas
Problem: Generated mask is empty

Check:

The land polygon shapefile is correct.
The shapefile uses WGS84.
The image coordinates in DARTIS_2019.tab are valid.
The correct image metadata is being used.
The image and metadata filename mapping is correct.
Problem: Mask is not aligned with coastline

Check the CRS of the land polygon:

import geopandas as gpd

land = gpd.read_file("land_polygons/land_polygons.shp")

print(land.crs)

For the recommended OpenStreetMap dataset, it should be WGS84 / EPSG:4326.

28. Verify the Shapefile Before Running

You can quickly check the downloaded shapefile using:

import geopandas as gpd

path = "land_polygons/land_polygons.shp"

land = gpd.read_file(path)

print("CRS:", land.crs)
print("Number of polygons:", len(land))
print(land.head())

Expected CRS:

EPSG:4326

or an equivalent WGS84 CRS representation.

29. Git Repository

Do not commit the large DARTIS dataset or the global land polygons to GitHub.

Recommended repository:

DARTIS-land-mask/
│
├── img_land_mask.py
├── dataset_toolbox.py
├── requirements.txt
├── README.md
└── .gitignore

The user should download the datasets separately.

The .gitignore should exclude:

dataset_structured/
land_polygons/
DARTIS_2019.tab
patches_masked/
30. Quick Start

For experienced users:

Step 1

Clone the repository:

git clone <YOUR_REPOSITORY_URL>
cd DARTIS-land-mask
Step 2

Create a virtual environment:

python -m venv .venv
Step 3

Activate it.

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate
Step 4

Install dependencies:

pip install -r requirements.txt
Step 5

Download DARTIS-2019.

Place the structured dataset at:

dataset_structured/
Step 6

Place:

DARTIS_2019.tab

in the project root.

Step 7

Download the OpenStreetMap land polygons:

https://osmdata.openstreetmap.de/data/land-polygons.html

Select:

Shapefile
WGS84
Large polygons not split

Extract it into:

land_polygons/
Step 8

Configure:

dir_dataset = "dataset_structured"
structured_tf = True
data_tab = "DARTIS_2019.tab"
landpolygons_file = "land_polygons/land_polygons.shp"
select_subsets = ["nc", "oc"]
dir_output = "patches_masked"
create_land_mask_tf = True
create_masked_patch_tf = False
Step 9

Run:

python img_land_mask.py
Step 10

Check:

patches_masked/

for:

*_mask.jpg
31. References
DARTIS-2019

Official GitHub repository:

https://github.com/yi-jie-yang/dataset_DARTIS_2019

DARTIS-2019 dataset:

https://doi.pangaea.de/10.1594/PANGAEA.980773

OpenStreetMap Land Polygons

https://osmdata.openstreetmap.de/data/land-polygons.html

GSHHG

Wessel, P. and Smith, W. H. F. (1996).

A Global, Self-consistent, Hierarchical, High-resolution Shoreline Database.

Journal of Geophysical Research.

https://doi.org/10.1029/96JB00104

Todd Karin Global Land Mask

https://doi.org/10.5281/zenodo.4066722

32. License and Data Attribution

The DARTIS-2019 dataset and its associated materials are subject to their respective data/source terms.

The OpenStreetMap land polygon data is derived from OpenStreetMap and is available under the Open Database License (ODbL).

Users should review and comply with the licenses and attribution requirements of the respective datasets before redistribution or publication.

33. Summary

This project generates land masks for DARTIS-2019 coastal Sentinel-1 SAR images.

Required inputs:

1. DARTIS-2019 images
2. DARTIS_2019.tab
3. WGS84 land polygon shapefile

Required Python packages:

numpy
pandas
Pillow
geopandas
rasterio

Main script:

img_land_mask.py

Output:

*_mask.jpg

The generated masks can then be used as an auxiliary input for oil-spill segmentation and subsequent U-Net-based segmentation workflows.


### One detail I'd keep in the README

The official DARTIS repository actually says that **land masking was not necessary for the authors' own study**, and that `img_land_mask.py` is provided for users who want to apply land masks to the published dataset. It also warns that applying the script can rename files, which affects the repository's performance-evaluation programs. :contentReference[oaicite:1]{index=1}

That note is worth retaining because it makes your README scientifically accurate rather than presenting land masking as something the original DARTIS authors required.

For the land polygons, the current OSM page confirms that the **WGS84 / large polygons not split / Shapefile** option is available, and explains that the polygons represent continents and islands derived from OSM coastline data. :contentReference[oaicite:2]{index=2}
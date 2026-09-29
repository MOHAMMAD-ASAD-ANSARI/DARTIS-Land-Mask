from pathlib import Path
import numpy as np
from PIL import Image
from global_land_mask import globe
import dataset_toolbox

####################
### User's Input ###
####################
# dir_dataset = "dataset"
# structured_tf = False          # True if you ran structure_dataset.py
# data_tab = "DARTIS_2019.tab"
# select_subsets = ["nc", "oc"]
# dir_output = "patches_masked"
# create_land_mask_tf = True     # save mask images
# create_masked_patch_tf = True  # save patches with land set to 0
# verbose = True

dir_dataset = "dataset_structured"
structured_tf = True
data_tab = "DARTIS_2019.tab"
landpolygons_file = "land_polygons/land_polygons.shp"
select_subsets = ["nc", "oc"]
dir_output = "patches_masked"
create_land_mask_tf = True
create_masked_patch_tf = False
verbose = True


#############
### Func. ###
#############
def pixel_lonlat(row, height, width):
    """Bilinear interpolation of the 4 corner coords to every pixel centre."""
    v, u = np.meshgrid((np.arange(height) + 0.5) / height,
                       (np.arange(width) + 0.5) / width, indexing="ij")

    def interp(ul, ur, bl, br):
        top = (1 - u) * ul + u * ur
        bot = (1 - u) * bl + u * br
        return (1 - v) * top + v * bot

    lon = interp(row.patch_ul_lon, row.patch_ur_lon, row.patch_bl_lon, row.patch_br_lon)
    lat = interp(row.patch_ul_lat, row.patch_ur_lat, row.patch_bl_lat, row.patch_br_lat)
    lon = ((lon + 180) % 360) - 180   # safety: wrap to -180..180
    return lon, lat


def land_masking(row, dir_output):
    if verbose: print(row.tag)

    image_arr = np.array(Image.open(row.path_jpg))
    height, width = image_arr.shape[:2]

    lon, lat = pixel_lonlat(row, height, width)
    landmask = globe.is_land(lat, lon)          # True = land

    stem = Path(row.path_jpg).stem

    if create_land_mask_tf:
        out = dir_output / f"{stem}_mask.png"   # PNG: lossless, avoids bool->JPG error
        Image.fromarray((landmask * 255).astype(np.uint8)).save(out)
        if verbose: print(f"    --> {out}")

    if create_masked_patch_tf:
        out = dir_output / f"{stem}_maskout.jpg"
        masked = image_arr.copy()
        masked[landmask] = 0
        Image.fromarray(masked).save(out)
        if verbose: print(f"    --> {out}")

############
### Main ###
############
if __name__ == "__main__":
    dir_dataset = Path(dir_dataset)
    dir_output = Path(dir_output)
    dir_output.mkdir(parents=True, exist_ok=True)

    dataset_info = dataset_toolbox.DataTab(data_tab)
    df_dataset = dataset_info.extract_partial_dataset(select_subsets=select_subsets)

    # if structured_tf:
    #     df_dataset = dataset_info.refresh2folder_structure(
    #         dir_dataset_new=dir_dataset,
    #         col_path_jpg_new="path_jpg", col_path_xml_new="path_xml")

    if structured_tf:
        df_dataset, _ = dataset_info.refresh2folder_structure(
            dir_dataset_new=dir_dataset,
            col_path_jpg_new="path_jpg",
            col_path_xml_new="path_xml"
        )

    else:
        df_dataset = dataset_info.load_jpg_path(dir_dataset=dir_dataset)

    df_dataset.apply(lambda row: land_masking(row, dir_output), axis=1)
    print("Done.")
# import os
import subprocess

# import gdal


# TODO: Clean-up
def create_raster_tile(file):
    """
    Work flow convert the geotiff file that is in 16-bit to 8-bit for mapbox
    """
    scaled_command_using_glad = "gdal_translate -ot Byte -b 1 ODDRIN_EQ20210814HTI_Est20210815.tif raster.tif -scale 0 22954.003 1 255 -a_nodata 0 -colorinterp_1 blue"  # noqa: E501

    scaled_file = subprocess.Popen(scaled_command_using_glad, stdout=subprocess.PIPE, shell=True)
    print(scaled_file)
    username = "togglecorp"
    # upload this file
    upload_command = f"mapbox upload {username}.data raster.tif"
    # this returns the upload_id
    # use this id for the tileset
    upload = subprocess.Popen(upload_command, stdout=subprocess.PIPE, shell=True)
    print(upload)

    # the upload_id is thus used to create_tileset
    # create_tileset = f"mapbox datasets create-tileset ckw4px83t06yi21pndbxpnpg5 {username}"
    # tileset = os.system(create_tileset)

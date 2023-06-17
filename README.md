## Sample raster file(s) using vector file(s) by PyQGIS 

A package that uses PyQGIS to sample (m) raster files using (n) shape file and produce m\*n output shape files.

Using QGIS version 3.2 and later.

All the environment variables can be found at file named `python-qgis-ltr.bat` at Windows (QGIS bin folder).

The file's name may differ according to your GIS installation.

```
python script.py 
       --qgis_path "C:/Program Files/QGIS 3.28.6/app/qgis-ltr" ^
       --vector_files "D:/path_to_shape_files/*.shp" ^
       --raster_file "D:/path_to_raster_file/*.tif" ^
	   --output_files "D:/path_to_output_optional/output" ^
	   --log_files "D:/path_to_logs_optional/logs"
```
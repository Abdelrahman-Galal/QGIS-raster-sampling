import os
import logging
from qgis.core import QgsVectorFileWriter

def write_vector_to(vector_file, output_file, format, encoding, logger=None):
    """To save vector layer"""
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = format
    options.fileEncoding = encoding
    if logger is None:
        logger = logging.getLogger()

    out_dir = os.path.dirname(output_file)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        logger.info(f'Output folder does not exist,Created Now!')
       
    return QgsVectorFileWriter.writeAsVectorFormatV3(
        vector_file, output_file,
        vector_file.transformContext(),
        options)
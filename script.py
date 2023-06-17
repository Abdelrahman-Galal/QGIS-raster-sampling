import argparse
from pathlib import Path
from datetime import datetime 
from qgis.core import *
from create_logger import create_logger
from write_vector_to import write_vector_to


def main(qgis_path,vector_files_path,raster_files_path,output_dir_path,log_dir_path):
    # set parameters
    start_date = 2000
    project_crs = 'EPSG:3035'
    output_dir = output_dir_path
    log_dir = log_dir_path
    vector_layers = []

    # set main logger
    log_file = log_dir + "/"+ f'main-{datetime.now():%Y-%m-%d-%H-%M}.log'
    main_logger = create_logger('root', log_file)

    # initiate QGIS
    QgsApplication.setPrefixPath(qgis_path, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # import processing
    from processing.core.Processing import Processing
    import processing
    Processing.initialize()

    vector_files_path = Path(vector_files_path)
    raster_files_path = Path(raster_files_path)

    vector_files = vector_files_path.parent
    raster_files = raster_files_path.parent

    vector_pattern = vector_files_path.name
    raster_pattern = raster_files_path.name
    

    vector_files = list(vector_files.glob(vector_pattern))
    raster_files = list(raster_files.glob(raster_pattern))
    

    main_logger.info(f'There is {len(vector_files)} vector files(s)')
    main_logger.info(f'There is {len(raster_files)} rasterfiles(s)')

    # load vector (address) layer
    for file in sorted(vector_files):
        vlayer = QgsVectorLayer(str(file), file.name)
        if vlayer.isValid():
            vector_layers.append(vlayer)
            log_msg = f'"Vector layer {vlayer.name()} - {vlayer.crs()} loaded."'
            main_logger.info(log_msg)
        else:
            log_msg = f'"Vector layer {file.name} failed to load!"'
            main_logger.error(log_msg)
        # load raster (environmental factors) layer(s)
        for file in sorted(raster_files):
            layer = QgsRasterLayer(str(file), file.name)
            log_file = log_dir + "/" +layer.name().split('.')[0] + '.log'
            raster_log = create_logger("raster_log", log_file)
            log_msg = f'"starting working with {layer.name()} - {layer.crs()}"'
            raster_log.info(log_msg)
            if layer.isValid():
                output_file = output_dir + "/" +layer.name().split('.')[0] + '.csv'
                feedback = QgsProcessingFeedback()
                # run vector/raster sampling tool
                params = {'INPUT': vlayer,
                          'RASTERCOPY': layer,
                          'COLUMN_PREFIX': 'ENV_F_',
                          'OUTPUT': 'TEMPORARY_OUTPUT'}
                result = processing.run("native:rastersampling",
                                        params,
                                        feedback=feedback)
                raster_log.info(feedback.textLog())
                # feedback object to collect logs
                feedback = QgsProcessingFeedback()
                # run field calculator tool
                params = {'INPUT': result['OUTPUT'],
                          'FIELD_NAME': 'DATE',
                          'FIELD_TYPE': 2,
                          'FIELD_LENGTH:0': 4,
                          'FIELD_PRECISION': 0,
                          'FORMULA': str(start_date),
                          'OUTPUT': 'TEMPORARY_OUTPUT'}
                result = processing.run('qgis:fieldcalculator',
                                        params,
                                        feedback=feedback)
                raster_log.info(feedback.textLog())
                # write final file as a csv file
                to_csv = write_vector_to(
                    result["OUTPUT"], output_file, "CSV", 'utf-8')
                if not to_csv[0]:
                    start_date = start_date + 1
                    log_msg = f'"Done writing {layer.name()}"'
                    raster_log.info(log_msg)
                    main_logger.info(log_msg)
                else:
                    log_msg = f'"Error writing {layer.name()} - {to_csv[1]}"'
                    raster_log.error(log_msg)
                    main_logger.info(log_msg)
            else:
                log_msg = f'"Layer failed to load raster {layer.name()}!"'
                raster_log.error(log_msg)
                main_logger.info(log_msg)

    qgs.exitQgis()
    main_logger.info("Exiting!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qgis_path',type=str,required=True,help="location of QGIS Installation path")
    parser.add_argument('--vector_files',type=str,required=True,help="location of *.shp files")
    parser.add_argument('--raster_files',type=str,required=True,help="location of *.tif files")
    parser.add_argument('--output_files',type=str,required=False,default="./output",help="location of output files")
    parser.add_argument('--log_files',type=str,required=False,default="./logs",help="location of log files")
    args = parser.parse_args()
    main(args.qgis_path,args.vector_files,args.raster_files,args.output_files,args.log_files)

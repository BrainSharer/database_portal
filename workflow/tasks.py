import os, sys, time
from datetime import datetime
import re
from multiprocessing.pool import Pool
from subprocess import Popen
from decimal import Decimal
import traceback
from celery.exceptions import Ignore
from celery_progress.backend import ProgressRecorder
from brain.models import ScanRun, Section, Slide, SlideCziToTif
from celery.app import shared_task
from celery.utils.log import get_task_logger
from celery import states, current_task
from django.conf import settings
from time import sleep

import random

if settings.DEBUG:
    from abakit.utilities.file_location import FileLocationManager
    from abakit.utilities.shell_tools import workernoshell
    from abakit.utilities.czi_tools import get_czi_metadata, get_fullres_series_indices

    SCALING_FACTOR = 0.03125
    PROGRESS_STATE = 'PROGRESS'
    logger = get_task_logger(__name__)


    @shared_task(bind=True)
    def setup(self, animal):
        progress_recorder = ProgressRecorder(self)
        fileLocationManager = FileLocationManager(animal)
        INPUT = fileLocationManager.czi
        files = []
        description = "Looking for CZI files."
        
        try:
            files = os.listdir(INPUT)
        except FileNotFoundError as fe:
            error = f'Error: {fe}'
            logger.error(error)
            raise Ignore()
        
        for i in range(len(files)):
            progress_recorder.set_progress(i, len(files), description=description)
            sleep(1)
        return len(files)


    """
    Start of import of methods to set up celery queue
    """

    @shared_task(bind=True)
    def make_meta(self, animal):
        """
        Scans the czi dir to extract the meta information for each tif file
        Args:
            animal: the animal as primary key
            remove: boolean to determine if we should remove the scan run ID

        Returns: nothing
        """
        progress_recorder = ProgressRecorder(self)
        fileLocationManager = FileLocationManager(animal)
        scan_run = ScanRun.objects.filter(prep_id=animal)[0]
        slides = Slide.objects.filter(scan_run=scan_run).all()

        lslides = len(slides)
        if lslides > 0:
            logger.info(f"Found {lslides} some slides, so existing function.")
            return lslides


        try:
            czi_files = sorted(os.listdir(fileLocationManager.czi))
        except OSError as e:
            print(e)

        section_number = 1
        file_count = len(czi_files)
        for i, czi_file in enumerate(czi_files):
            extension = os.path.splitext(czi_file)[1]
            if extension.endswith('czi'):
                slide = Slide()
                slide.scan_run_id = scan_run.id
                slide.slide_physical_id = int(re.findall(r'\d+', czi_file)[1])
                slide.rescan_number = "1"
                slide.slide_status = 'Good'
                slide.processed = False
                slide.file_size = os.path.getsize(os.path.join(fileLocationManager.czi, czi_file))
                slide.file_name = czi_file
                slide.created = datetime.fromtimestamp(os.path.getmtime(os.path.join(fileLocationManager.czi, czi_file)))

                # Get metadata from the czi file
                czi_file_path = os.path.join(fileLocationManager.czi, czi_file)
                metadata_dict = get_czi_metadata(czi_file_path)
                series = get_fullres_series_indices(metadata_dict)
                slide.scenes = len(series)
                slide.save()
                progress_recorder.set_progress(i, len(czi_files), description='Yanking meta information from CZI')

                for j, series_index in enumerate(series):
                    scene_number = j + 1
                    channels = range(metadata_dict[series_index]['channels'])
                    channel_counter = 0
                    width = metadata_dict[series_index]['width']
                    height = metadata_dict[series_index]['height']
                    for channel in channels:
                        tif = SlideCziToTif()
                        tif.slide_id = slide.id
                        tif.scene_number = scene_number
                        tif.file_size = 0
                        tif.active = 1
                        tif.width = width
                        tif.height = height
                        tif.scene_index = series_index
                        channel_counter += 1
                        newtif = '{}_S{}_C{}.tif'.format(czi_file, scene_number, channel_counter)
                        newtif = newtif.replace('.czi', '').replace('__','_')
                        tif.file_name = newtif
                        tif.channel = channel_counter
                        tif.processing_duration = 0
                        tif.created = time.strftime('%Y-%m-%d %H:%M:%S')
                        tif.save()
                    section_number += 1
        return section_number

    """
    from create_tifs.py
    """

    @shared_task(bind=True)
    def make_tifs(self, animal, channel, njobs):
        """
        This method will:
            1. Fetch the sections from the database
            2. Yank the tif out of the czi file according to the index and channel with the bioformats tool.
            3. Then updates the database with updated meta information
        Args:
            animal: the prep id of the animal
            channel: the channel of the stack to process
            njobs: number of jobs for parallel computing

        Returns:
            number of tifs created
        """
        progress_recorder = ProgressRecorder(self)
        fileLocationManager = FileLocationManager(animal)
        INPUT = fileLocationManager.czi
        OUTPUT = fileLocationManager.tif
        os.makedirs(OUTPUT, exist_ok=True)
        sections = Section.objects.filter(prep_id=animal).filter(channel=channel)\
            .values('czi_file', 'file_name', 'scene_index',  'channel').distinct()

        commands = []
        for i, section in enumerate(sections):
            input_path = os.path.join(INPUT, section['czi_file'])
            output_path = os.path.join(OUTPUT, section['file_name'])
            progress_recorder.set_progress(i, len(sections), description='Creating tifs')

            if not os.path.exists(input_path):
                continue

            if os.path.exists(output_path):
                continue

            channel_index = str(int(section['channel']) - 1)
            cmd = ['/usr/local/share/bftools/bfconvert', '-bigtiff', '-separate', '-series', str(section['scene_index']),
                    '-channel', channel_index,  '-nooverwrite', input_path, output_path]

            
            #cmd = [section.scene_index, section.channel_index, input_path, output_path]
            #commands.extend([bfconvert.subtask(
            #    (section.scene_index, section.channel_index, input_path, output_path))
            #        for i in range(nproc)])

        #result = group(commands).apply_async()
            
            commands.append(cmd)

        with Pool(njobs) as p:
            p.map(workernoshell, commands)

        return len(sections)



    @shared_task
    def bfconvert(scene_index, channel_index, input_path, output_path):
        cmd = ['/usr/local/share/bftools/bfconvert', '-bigtiff', '-separate', '-series', str(scene_index),
                '-channel', str(channel_index),  '-nooverwrite', input_path, output_path]
        proc = Popen(cmd, shell=False, stderr=None, stdout=None)
        proc.wait()
        #run(cmd)



    @shared_task(bind=True)
    def make_scenes(self, animal, njobs):
        """
        This will create some PNG files from the tif files.
        The PNG files are downsampled to 3.125% of the original size.
        Args:
            animal: the animal to work on
            njobs: how many procs to spawn.
        Returns:
            the number of PNG files created.
        """
        progress_recorder = ProgressRecorder(self)
        fileLocationManager = FileLocationManager(animal)
        INPUT = fileLocationManager.tif
        OUTPUT = os.path.join(fileLocationManager.thumbnail_web, 'scene')
        os.makedirs(OUTPUT, exist_ok=True)

        commands = []
        tifs = os.listdir(INPUT)
        for i, tif in enumerate(tifs):
            tif_path = os.path.join(INPUT, tif)
            progress_recorder.set_progress(i, len(tifs), description='Creating PNG web files')
            if not tif.endswith('_C1.tif'):
                continue

            png = tif.replace('tif', 'png')
            png_path = os.path.join(OUTPUT, png)
            if os.path.exists(png_path):
                continue

            # convert tif to png
            cmd = ['convert', tif_path, '-resize', '3.125%', '-normalize', png_path]
            commands.append(cmd)

        with Pool(njobs) as p:
            p.map(workernoshell, commands)

        return len(tifs)

else:
    def setup():
        pass 
    def make_meta():
        pass
    def make_tifs():
        pass 
    def make_scenes():
        pass
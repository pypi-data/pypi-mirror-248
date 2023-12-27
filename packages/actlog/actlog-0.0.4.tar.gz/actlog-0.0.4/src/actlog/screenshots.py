import glob
import datetime
import subprocess
import os
import time
import json
import re

from . import image_timestring
from .file_importer import import_module_from_file
from . import external_dependencies


def screenshot_problems():
    if os.environ.get('WAYLAND_DISPLAY'):
        return "Cannot take screenshots under wayland. Sorry."
    if not external_dependencies.find('scrot') and \
          not external_dependencies.find('import'):
        return "Couldn't find either scrot or import - cannot take screenshots"
    return None


class Screenshotter:
    def __init__(self, screenshots_dir, generator_path):
        self.screenshots_dir = screenshots_dir
        if os.path.exists(generator_path):
            self.metadata_generator = import_module_from_file(
                'screenshot_metadata_generator', generator_path)
        else:
            self.metadata_generator = None
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

        if external_dependencies.find('scrot'):
            self.make_screenshot = ['scrot', '-z']
        elif external_dependencies.find('import'):
            self.make_screenshot = ['import', '-silent', '-window', 'root']
        else:
            raise RuntimeError('expected to find scrot or import')

        self.found_convert = external_dependencies.find('convert')
        self.found_pngquant = external_dependencies.find('pngquant')

    def _validate_metadata_keys(self, metadata):
        """Only allow filename-friendly chars in metadata keys.

        We use the keys to create file names in def _meta_file_name below, so if
        you relax this, make sure the other code is safe.
        """
        for key in metadata.keys():
            if re.search(r'[^a-zA-Z0-9_\-]', key):
                raise RuntimeError(f'Bad metadata key: "{key}"')

    def screenshot_now(self):
        now = time.time()
        base_filename = os.path.join(
            self.screenshots_dir, image_timestring.time_to_string(now)
        )
        png_file = base_filename + '.png'

        # scrot creates png_file - 1.2MB for a 4K screenshot
        make_screenshot = self.make_screenshot.copy()
        make_screenshot.append(png_file)
        subprocess.run(make_screenshot)

        # This reduces it to approx 598KB
        if self.found_convert:
            subprocess.run(["convert", "-depth", "4", png_file, png_file])
        # This reduces it to approx 340KB
        if self.found_pngquant:
            subprocess.run(["pngquant", "-f", "--ext", ".png", png_file])
        created_files = [png_file]
        if self.metadata_generator:
            try:
                metadata = self.metadata_generator.metadata()
                if len(metadata.keys()) > 0:
                    self._validate_metadata_keys(metadata)
                    m_file = base_filename + '.metadata'
                    with open(m_file, 'w') as f:
                        f.write(json.dumps(
                            metadata,
                            sort_keys=True,
                            indent=4
                        ) + "\n")
                    created_files.append(m_file)
            except Exception as e:
                print("Got exection generating metadata: ", e)
        return created_files


def _get_metadata(mfname):
    with open(mfname, 'r') as f:
        metadata = json.load(f)
        return metadata


def _create_meta_image(path, label):
    command = [
        "convert",
        "-background", "lightblue",
        "-fill", "blue",
        "-pointsize", "96",
        "-gravity", "center",
        "-size", "1024x768",
        f"label:Metadata:\\n\\n{label}",
        path
    ]
    # print(" ".join(command))
    subprocess.run(command, check=True)


class Consumer:
    def __init__(self, screenshots_dir):
        self.screenshots_dir = screenshots_dir
        self.meta_dir = os.path.join(screenshots_dir, 'meta')
        if not os.path.exists(self.meta_dir):
            os.makedirs(self.meta_dir)

    def _meta_file_name(self, metadata):
        label = "+".join(sorted(metadata.keys()))
        fname = os.path.join("meta", label)
        path = os.path.join(self.screenshots_dir, fname) + '.png'
        if not os.path.exists(path):
            _create_meta_image(path, label)
        return fname

    def _get_screenshot_info(self, fname, file_paths):
        basename = os.path.basename(fname)
        name = os.path.splitext(basename)[0]
        timestamp = int(image_timestring.string_to_time(name))

        info = {
            "unsafe": name,
            "timestamp": timestamp,
            "safe": name,
        }
        if file_paths:
            info['path'] = fname

        # Metadata?
        metadata_fname = f"{os.path.splitext(fname)[0]}.metadata"
        if os.path.exists(metadata_fname):
            info['metadata'] = _get_metadata(metadata_fname)
            if file_paths:
                info['metadata']['path'] = metadata_fname
            info['safe'] = self._meta_file_name(info['metadata'])

        return info

    def _list_all_screenshots(self, file_paths):
        """_list_all_screenshots lists all screenshots.

        TODO: There probably should be some paging involved in case there are
        multiple 1000s of screenshots.
        """
        files = glob.glob(f"{self.screenshots_dir}/*.png")
        files.sort()
        shots = []
        for f in files:
            shots.append(self._get_screenshot_info(f, file_paths))
        return shots

    def list_screenshots(self, t_from, t_to):
        all = self._list_all_screenshots(False)

        def use_shot(s):
            if t_from and s['timestamp'] < t_from:
                return False
            if t_to and s['timestamp'] >= t_to:
                return False
            return True

        return list(filter(use_shot, all))

    def screenshot_days(self, t_from, t_to, start_of_day):
        def get_date(t):
            return datetime.date.fromtimestamp(t - start_of_day * 3600)
        shots = self.list_screenshots(t_from, t_to)
        days = []
        current_day = None
        for s in shots:
            s_date = get_date(s['timestamp'])
            if current_day == None or current_day['date'] != s_date:
                current_day = {
                    "date": s_date,
                    "screenshots": []
                }
                days.append(current_day)
            current_day['screenshots'].append(s)
        return days

    def expire(self, before):
        shots = self._list_all_screenshots(file_paths=True)
        files = []
        for shot in shots:
            if shot['timestamp'] > before:
                continue
            # print(shot)
            files.append(shot['path'])
            if 'metadata' in shot:
                files.append(shot['metadata']['path'])
        for f in files:
            # print(f)
            os.remove(f)

import json
from dataclasses import dataclass, replace
from datetime import date, datetime, time
from pathlib import Path
from typing import Dict, Optional, List

from loguru import logger
from mhdwriter.args import WriteArgs, WriteType
from mhdwriter.writer import write_mhd_raw



@dataclass
class ImportFilter:
    app: str
    roi: Optional[str]
    exposure: List[int]
    output_dir: Optional[str] = None
    include_rgb: bool = True
    downsample_factor: int = 0
    write_type: WriteType = WriteType.RAW


def run_import(cft_path: Path, import_filter: ImportFilter) -> None:
    if cft_path.suffix == ".json" and cft_path.name.startswith("study_detail"):
        convert_local_dataset(cft_path, import_filter)
    else:
        logger.error("Invalid CFT path. Please provide a url,.cft, or study_detail.json file")


def convert_local_dataset(cft_path: Path, import_filter: ImportFilter) -> None:
    logger.info(f"Converting local cft dataset from '{cft_path}' to mhd/raw")
    json_data = parse_json_file(cft_path)

    if json_data is None or "study_details" not in json_data:
        logger.error("Invalid study_detail.json file")
        return

    roi_dir = cft_path.parent.joinpath("rois")

    if not roi_dir.exists():
        logger.error("Missing rois directory")
        return

    study_details = json_data["study_details"]
    base_out_path = cft_path.parent.joinpath("mhds")
    base_out_path.mkdir(exist_ok=True, parents=True)

    study_date_str = study_details.get("study_date", "20000101")
    study_time_str = study_details.get("study_time", "000000")
    study_date_time = parse_date_time(study_date_str, study_time_str)

    if study_date_time is None:
        raise ValueError("Unable to parse date time from study_details file.")

    base_args = WriteArgs(
        fov=study_details["fov"],
        protocol=study_details["protocol"],
        study_description=study_details["study"],
        series_description=study_details["study"],
        downsample_factor=import_filter.downsample_factor,
        date_time=study_date_time,
        write_type=import_filter.write_type,
    )

    for roi_path in roi_dir.iterdir():
        if not roi_path.is_dir():
            continue
        roi_name = roi_path.name
        if import_filter.roi is not None and roi_name != import_filter.roi:
            continue
        for roi_app_path in roi_path.iterdir():
            if roi_app_path.name == "rgb":
                logger.info("Generating RGB mhd/raw for " + str(roi_app_path))
                if import_filter.downsample_factor > 0:
                    series_desc = f"{study_details['study']}_{roi_name}_RGB_d{import_filter.downsample_factor}"
                else:
                    series_desc = f"{study_details['study']}_{roi_name}_RGB"
                write_mhd_raw(
                    roi_app_path,
                    replace(base_args, is_rgb=True, series_description=series_desc),
                    base_out_path
                )
            elif roi_app_path.is_dir() and roi_app_path.name.startswith("ex"):
                for exp in import_filter.exposure:
                    if import_filter.downsample_factor > 0:
                        series_desc = f"{study_details['study']}_{roi_name}_{roi_app_path.name}_{exp}_d{import_filter.downsample_factor}"
                    else:
                        series_desc = f"{study_details['study']}_{roi_name}_{roi_app_path.name}_{exp}"
                    exp_dir = roi_app_path.joinpath(f"{exp}")
                    if not exp_dir.is_dir():
                        logger.error(f"Missing exposure directory {exp_dir}")
                        continue
                    write_mhd_raw(
                        exp_dir,
                        replace(base_args, is_rgb=False, series_description=series_desc),
                        base_out_path
                    )


def parse_json_file(file_path: Path) -> Optional[Dict]:
    try:
        with file_path.open('r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"An error occurred while reading the file: {e}")
        return None


def parse_date_time(study_date_str: str, study_time_str: str) -> Optional[datetime]:
    try:
        study_date = date(
            int(study_date_str[:4]),
            int(study_date_str[4:6]),
            int(study_date_str[6:]),
        )
    except ValueError as e:
        print("Unable to read date str " + study_date_str)
        return
    try:
        study_time = time(
            int(study_time_str[0:2]),
            int(study_time_str[2:4]),
            int(study_time_str[4:6]),
        )
    except ValueError as e:
        print("Unable to read time str " + study_time_str)
        return
    return datetime.combine(study_date, study_time)

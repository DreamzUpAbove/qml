import re
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

PATTERN_FLAGS = re.MULTILINE
PATTERN_TUTORIAL_NAME = re.compile(r"<span\sclass=\"pre\">(.*\.py)</span>", flags=PATTERN_FLAGS)
PATTERN_TUTORIAL_TIME = re.compile(r"<td><p>(\d{2}:\d{2}.\d{3})</p></td>", flags=PATTERN_FLAGS)


def convert_execution_time_to_ms(execution_time: str) -> int:
    """
    This function takes the execution time output from the sphinx_execution_times.html file and
    converts the time from:
      MM:SS.SSS -> <int: in milliseconds>
    """
    execution_time_parts = re.split(r"[:.]", execution_time)

    execution_time_min = int(execution_time_parts[0])
    execution_time_sec = int(execution_time_parts[1])
    execution_time_dsc = int(execution_time_parts[2])  # `dsc` short for decisecond (1 tenth of a second)

    return (execution_time_min * 60000) \
        + (execution_time_sec * 1000) \
        + (execution_time_dsc * 100)


def parse_sg_execution_times(sphinx_gallery_dir: "Path") -> Dict[str, int]:
    # Hard coding the filename here as it is not something the user controls.
    # The sg_execution_times exists inside the directory sphinx puts all the built "galleries"
    sg_execution_file_location = sphinx_gallery_dir / "sg_execution_times.html"

    with sg_execution_file_location.open("r") as fh:
        sg_execution_file_content = fh.read()

    tutorial_name_matches = PATTERN_TUTORIAL_NAME.findall(sg_execution_file_content)
    tutorial_time_matches = PATTERN_TUTORIAL_TIME.findall(sg_execution_file_content)

    assert len(tutorial_name_matches) == len(tutorial_time_matches), f"Unable to properly parse " \
                                                                     f"{str(sg_execution_file_location)}." \
                                                                     f"Got {len(tutorial_name_matches)} tutorial " \
                                                                     f"names, but {len(tutorial_time_matches)} " \
                                                                     f"execution time matches"

    return {
        tutorial_name: convert_execution_time_to_ms(tutorial_time)
        for tutorial_name, tutorial_time in zip(tutorial_name_matches, tutorial_time_matches)
    }

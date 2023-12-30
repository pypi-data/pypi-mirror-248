import sys

import cv2
import argparse
from enum import Enum

from mflowm import __doc__ as DESCRIPTION
from mflowm.helpers import file_path
from mflowm import MotionFlowMulti, CompositeMode, VideoReader


class ScaleMethods(Enum):
    AREA = cv2.INTER_AREA
    BITS = cv2.INTER_BITS
    BITS2 = cv2.INTER_BITS2
    CUBIC = cv2.INTER_CUBIC
    LANCZOS4 = cv2.INTER_LANCZOS4
    LINEAR = cv2.INTER_LINEAR
    LINEAR_EXACT = cv2.INTER_LINEAR_EXACT
    MAX = cv2.INTER_MAX
    NEAREST = cv2.INTER_NEAREST
    NEAREST_EXACT = cv2.INTER_NEAREST_EXACT
    TAB_SIZE = cv2.INTER_TAB_SIZE
    TAB_SIZE2 = cv2.INTER_TAB_SIZE2


def convert_video(
        filename,
        mode: CompositeMode,
        trails: bool = False,
        fade_speed: float | None = 2,
        fade_out: bool = True,
        windows_balance: bool = False,
        pre_scale: float = 1,
        output_scale: float = 1,
        display_scale: float = 1,
        scale_method: int = cv2.INTER_NEAREST,
        filename_suffix: str = "_flow"
):
    # Create the VideoReader
    video_reader = VideoReader(filename, scale=pre_scale, scale_method=scale_method)

    # Create the MotionFlowMulti object
    mfm = MotionFlowMulti(
        video_reader,
        mode=mode,
        trails=trails,
        fade_speed=fade_speed,
        windows_balance=windows_balance,
    )

    mfm.convert_to_file(
        output_scale=output_scale,
        display_scale=display_scale,
        output_scale_method=scale_method,
        display_scale_method=scale_method,
        filename_suffix=filename_suffix,
        fade_to_black=fade_out
    )


# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description=f"{DESCRIPTION}\n\n"
                    f"Valid parameters are shown in {{braces}}\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-i", "--input", dest="video_file",
        type=file_path, required=True,
        help="the video file to process"
    )

    parser.add_argument(
        "-m", "--mode", dest="mode",
        type=str, required=True,
        help="the composite mode to use {{{values}}}".format(
            values=", ".join([x.name for x in CompositeMode])
        )
    )

    parser.add_argument(
        "-t", "--trails", dest="draw_trails",
        type=bool, required=False, default=False,
        help=f"if we should draw trails or not [{False}]"
    )

    parser.add_argument(
        "-f", "--fade", dest="fade_speed",
        type=float, required=False, default=2,
        help=f"the fade speed to use for the trails (0 to disable) [{2}]"
    )

    parser.add_argument(
        "-fo", "--fade-out", dest="do_fade_out",
        type=bool, required=False, default=True,
        help=f"if we should fade to black at the end [{True}]"
    )

    parser.add_argument(
        "-b", "--balance-windows", dest="do_balancing",
        type=bool, required=False, default=False,
        help=f"if the flow windows should be averaged in brightness (makes the motion darker) [{False}]"
    )

    parser.add_argument(
        "-p", "--pre-scale", dest="prescale",
        type=float, required=False, default=1,
        help=f"the factor to pre-scale the video by (less than 1 makes it lower resolution) [{1}]"
    )

    parser.add_argument(
        "-o", "--output-scale", dest="output_scale",
        type=float, required=False, default=1,
        help=f"the factor to scale the output by [{1}]"
    )

    parser.add_argument(
        "-d", "--display-scale", dest="display_scale",
        type=float, required=False, default=1,
        help=f"the factor to scale the display by [{1}]"
    )

    parser.add_argument(
        "-sm", "--scale-method", dest="method",
        type=str, required=False, default=ScaleMethods.NEAREST.name,
        help="the composite mode to use {{{values}}} [{default}]".format(
            values=", ".join([x.name for x in ScaleMethods]),
            default=ScaleMethods.NEAREST.name
        )
    )

    parser.add_argument(
        "-s", "--suffix", dest="output_suffix",
        type=str, required=False, default="_flow",
        help="the suffix to use for the output filename [_flow]"
    )

    parsed_args = parser.parse_args(args)

    # Interpret string arguments
    if parsed_args.mode in [x.name for x in CompositeMode]:
        parsed_args.mode = CompositeMode[parsed_args.mode]
    else:
        valid_modes = ", ".join([x.name for x in CompositeMode])
        parser.error(f"\"{parsed_args.mode}\" is not a valid mode ({valid_modes})")

    if parsed_args.method in [x.name for x in ScaleMethods]:
        parsed_args.method = ScaleMethods[parsed_args.method]
    else:
        valid_methods = ", ".join([x.name for x in ScaleMethods])
        parser.error(f"\"{parsed_args.method}\" is not a valid scale method ({valid_methods})")

    # Correct values
    if parsed_args.fade_speed <= 0:
        parsed_args.fade_speed = None

    return parsed_args


def main(args):
    parsed_args = parse_args(args)

    convert_video(
        filename=parsed_args.video_file,
        mode=parsed_args.mode,
        trails=parsed_args.draw_trails,
        fade_speed=parsed_args.fade_speed,
        fade_out=parsed_args.do_fade_out,
        windows_balance=parsed_args.do_balancing,
        pre_scale=parsed_args.prescale,
        output_scale=parsed_args.output_scale,
        display_scale=parsed_args.display_scale,
        scale_method=parsed_args.method.value,
        filename_suffix=parsed_args.output_suffix
    )


def run():
    main(sys.argv[1:])

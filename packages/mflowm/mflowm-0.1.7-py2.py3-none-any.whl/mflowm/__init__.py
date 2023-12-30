"""MotionFlowMulti - A multi-resolution colorful motion detection video filter."""

__version__ = "0.1.7"

from mflowm.files import VideoReader
from mflowm.flow import MotionFlowMulti, CompositeMode
from mflowm.layer import LayerMode, layer_images
from mflowm.scripts import convert_video

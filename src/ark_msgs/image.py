import sys
import time
import numpy as np
from ark_msgs.registry import msgs

# image_pb2.py is generated from image.proto
from .image_pb2 import Image

@classmethod
def from_array(cls, array: np.ndarray, encoding: str = "rgb8") -> Image:
    """
    Initialize from a numpy array (e.g. from OpenCV).
    Assumes encoding matches array shape/type.
    """
    array = np.asarray(array)
    height, width = array.shape[:2]
    row_stride = array.strides[0]
    data = array.tobytes()
    
    # Simple mapping for common formats
    pixel_format = Image.PIXEL_FORMAT_UNKNOWN
    if encoding == "rgb8" or encoding == "rgb":
        pixel_format = Image.PIXEL_FORMAT_RGB
    elif encoding == "bgr8" or encoding == "bgr":
        pixel_format = Image.PIXEL_FORMAT_BGR
    elif encoding == "mono8" or encoding == "gray":
        pixel_format = Image.PIXEL_FORMAT_GRAY
    elif encoding == "rgba8" or encoding == "rgba":
        pixel_format = Image.PIXEL_FORMAT_RGBA
    elif encoding == "bgra8" or encoding == "bgra":
        pixel_format = Image.PIXEL_FORMAT_BGRA

    # utime in microseconds
    utime = int(time.time() * 1e6)

    return cls(
        utime=utime,
        height=height,
        width=width,
        pixel_format=pixel_format,
        row_stride=row_stride,
        size=len(data),
        data=data
    )

def as_array(self: Image, dtype=np.uint8) -> np.ndarray:
    """
    Convert to a numpy array.
    """
    shape = (self.height, self.width, -1)
    
    # Handle Mono/Gray special case for shape
    if (self.pixel_format == Image.PIXEL_FORMAT_GRAY or 
        self.pixel_format == Image.PIXEL_FORMAT_BE_GRAY16 or
        self.pixel_format == Image.PIXEL_FORMAT_LE_GRAY16):
         shape = (self.height, self.width)
    
    return np.frombuffer(self.data, dtype=dtype).reshape(shape)

# Optional PIL support
try:
    from PIL import Image as PILImage
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

@classmethod
def from_pil(cls, pil_image, encoding: str = "rgb") -> Image:
    """
    Initialize from a PIL Image.
    Converts PIL Image to numpy array and uses from_array.
    Requires pillow to be installed.
    """
    if not _HAS_PIL:
        raise ImportError("pillow is required for from_pil. Install with: pip install pillow")
    
    # Convert PIL image to numpy array
    array = np.array(pil_image)
    
    # Determine encoding from PIL mode
    if encoding == "auto":
        mode_to_encoding = {
            "RGB": "rgb",
            "RGBA": "rgba",
            "L": "gray",
            "BGR": "bgr",
        }
        encoding = mode_to_encoding.get(pil_image.mode, "rgb")
    
    return cls.from_array(array, encoding=encoding)

def as_pil(self: Image):
    """
    Convert to a PIL Image.
    Converts to numpy array first, then to PIL Image.
    Requires pillow to be installed.
    """
    if not _HAS_PIL:
        raise ImportError("pillow is required for as_pil. Install with: pip install pillow")
    
    # Convert to numpy array
    array = self.as_array()
    
    # Determine PIL mode from pixel format
    if self.pixel_format == Image.PIXEL_FORMAT_GRAY:
        mode = "L"
    elif self.pixel_format == Image.PIXEL_FORMAT_RGB:
        mode = "RGB"
    elif self.pixel_format == Image.PIXEL_FORMAT_RGBA:
        mode = "RGBA"
    elif self.pixel_format == Image.PIXEL_FORMAT_BGR:
        # PIL doesn't have BGR mode, convert to RGB
        array = array[:, :, ::-1]
        mode = "RGB"
    elif self.pixel_format == Image.PIXEL_FORMAT_BGRA:
        # Convert BGRA to RGBA
        array = array[:, :, [2, 1, 0, 3]]
        mode = "RGBA"
    else:
        # Default to RGB
        mode = "RGB"
    
    return PILImage.fromarray(array, mode=mode)

if not hasattr(Image, "from_array"):
    Image.from_array = from_array
if not hasattr(Image, "as_array"):
    Image.as_array = as_array
if not hasattr(Image, "from_pil"):
    Image.from_pil = from_pil
if not hasattr(Image, "as_pil"):
    Image.as_pil = as_pil

# Define constants matching proto/bot_core
Image.PIXEL_FORMAT_UNKNOWN          = 0
Image.PIXEL_FORMAT_UYVY             = 1498831189
Image.PIXEL_FORMAT_YUYV             = 1448695129
Image.PIXEL_FORMAT_IYU1             = 827677001
Image.PIXEL_FORMAT_IYU2             = 844454217
Image.PIXEL_FORMAT_YUV420           = 842093913
Image.PIXEL_FORMAT_YUV411P          = 1345401140
Image.PIXEL_FORMAT_I420             = 808596553
Image.PIXEL_FORMAT_NV12             = 842094158
Image.PIXEL_FORMAT_GRAY             = 1497715271
Image.PIXEL_FORMAT_RGB              = 859981650
Image.PIXEL_FORMAT_BGR              = 861030210
Image.PIXEL_FORMAT_RGBA             = 876758866
Image.PIXEL_FORMAT_BGRA             = 877807426
Image.PIXEL_FORMAT_BAYER_BGGR       = 825770306
Image.PIXEL_FORMAT_BAYER_GBRG       = 844650584
Image.PIXEL_FORMAT_BAYER_GRBG       = 861427800
Image.PIXEL_FORMAT_BAYER_RGGB       = 878205016
Image.PIXEL_FORMAT_BE_BAYER16_BGGR  = 826360386
Image.PIXEL_FORMAT_BE_BAYER16_GBRG  = 843137602
Image.PIXEL_FORMAT_BE_BAYER16_GRBG  = 859914818
Image.PIXEL_FORMAT_BE_BAYER16_RGGB  = 876692034
Image.PIXEL_FORMAT_LE_BAYER16_BGGR  = 826360396
Image.PIXEL_FORMAT_LE_BAYER16_GBRG  = 843137612
Image.PIXEL_FORMAT_LE_BAYER16_GRBG  = 859914828
Image.PIXEL_FORMAT_LE_BAYER16_RGGB  = 876692044
Image.PIXEL_FORMAT_MJPEG            = 1196444237
Image.PIXEL_FORMAT_BE_GRAY16        = 357
Image.PIXEL_FORMAT_LE_GRAY16        = 909199180
Image.PIXEL_FORMAT_BE_RGB16         = 358
Image.PIXEL_FORMAT_LE_RGB16         = 1279412050
Image.PIXEL_FORMAT_BE_SIGNED_GRAY16 = 359
Image.PIXEL_FORMAT_BE_SIGNED_RGB16  = 360
Image.PIXEL_FORMAT_FLOAT_GRAY32     = 842221382

msgs.register_item(Image)

__all__ = ["Image"]

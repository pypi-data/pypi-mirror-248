"""
AppConfig class providing central config

"""

import json
import logging
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import jsonref
from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt, PrivateAttr
from pydantic.fields import FieldInfo
from pydantic_extra_types.color import Color
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger(__name__)

CONFIG_FILENAME = "./config/config.json"


class EnumDebugLevel(str, Enum):
    """enum for debuglevel"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class GroupCommon(BaseModel):
    """Common config for photobooth."""

    model_config = ConfigDict(title="Common Config")

    countdown_capture_first: float = Field(
        default=2.0,
        ge=0,
        le=20,
        description="Countdown in seconds, started when user start a capture process",
    )

    countdown_capture_second_following: float = Field(
        default=1.0,
        ge=0,
        le=20,
        description="Countdown in seconds, used for second and following captures for collages",
    )
    countdown_camera_capture_offset: float = Field(
        default=0.25,
        ge=0,
        le=20,
        description="Trigger camera capture by offset earlier (in seconds). 0 trigger exactly when countdown is 0. Use to compensate for delay in camera processing for better UX.",
    )

    collage_automatic_capture_continue: bool = Field(
        default=True,
        description="Automatically continue with second and following images to capture for collage. No user interaction in between.",
    )

    DEBUG_LEVEL: EnumDebugLevel = Field(
        title="Debug Level",
        default=EnumDebugLevel.DEBUG,
        description="Log verbosity. File is writte to disc, and latest log is displayed also in UI.",
    )

    webserver_bind_ip: str = Field(
        default="0.0.0.0",
        description="IP/Hostname to bind the webserver to. 0.0.0.0 means bind to all IP adresses of host.",
    )
    webserver_port: int = Field(
        default=8000,
        description="Port to serve the photobooth website. Ensure the port is available. Ports below 1024 need root!",
    )


class GroupSharing(BaseModel):
    """Settings about shareing media"""

    model_config = ConfigDict(title="🫶 Share Config")

    shareservice_enabled: bool = Field(
        default=False,
        description="Enable share service. To enable URL needs to be configured and dl.php script setup properly.",
    )
    shareservice_url: str = Field(
        default="http://explain-shareservice.photobooth-app.org/dl.php",
        description="URL of php script that is used to serve files and share via QR code.",
    )
    shareservice_apikey: str = Field(
        default="changedefault!",
        description="Key to secure the download php script. Set the key in dl.php script to same value. Only if correct key is provided the shareservice works properly.",
    )
    shareservice_share_original: bool = Field(
        default=False,
        description="Upload original image as received from camera. If unchecked, the full processed version is uploaded with filter and texts applied.",
    )

    share_custom_qr_url: str = Field(
        default="http://localhost/media/processed/full/{filename}",
        description="URL displayed as QR code to image for download. Need you to sync the files on your own or allow the user to access via hotspot. {filename} is replaced by actual filename in QR code.",
    )


class EnumImageBackendsMain(str, Enum):
    """enum to choose image backend MAIN from"""

    VIRTUALCAMERA = "VirtualCamera"
    PICAMERA2 = "Picamera2"
    WEBCAMCV2 = "WebcamCv2"
    WEBCAMV4L = "WebcamV4l"
    GPHOTO2 = "Gphoto2"
    DIGICAMCONTROL = "Digicamcontrol"


class EnumImageBackendsLive(str, Enum):
    """enum to choose image backend LIVE from"""

    DISABLED = "Disabled"
    VIRTUALCAMERA = "VirtualCamera"
    PICAMERA2 = "Picamera2"
    WEBCAMCV2 = "WebcamCv2"
    WEBCAMV4L = "WebcamV4l"


class EnumPicamStreamQuality(str, Enum):
    """Enum type to describe the quality wanted from an encoder.
    This may be passed if a specific value (such as bitrate) has not been set.
    """

    VERY_LOW = "very low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very high"


class GroupBackends(BaseModel):
    """
    Choose backends for still images/high quality images captured on main backend.
    If the livepreview is enabled, the video is captured from live backend (if configured)
    or main backend.
    """

    model_config = ConfigDict(title="Camera Backend Config")

    MAIN_BACKEND: EnumImageBackendsMain = Field(
        title="Main Backend",
        default=EnumImageBackendsMain.VIRTUALCAMERA,
        description="Main backend to use for high quality still captures. Also used for livepreview if backend is capable of.",
    )
    LIVE_BACKEND: EnumImageBackendsLive = Field(
        title="Live Backend",
        default=EnumImageBackendsLive.DISABLED,
        description="Secondary backend used for live streaming only. Useful to stream from webcam if DSLR camera has no livestream capability.",
    )
    LIVEPREVIEW_ENABLED: bool = Field(
        default=True,
        description="Enable livestream (if possible)",
    )
    LIVEPREVIEW_FRAMERATE: int = Field(
        default=15,
        ge=5,
        le=30,
        description="Reduce the framerate to save cpu/gpu on device displaying the live preview",
        json_schema_extra={"ui_component": "QSlider"},
    )
    retry_capture: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Number of attempts to gather a picture from backend.",
    )

    gphoto2_iso_liveview: str = Field(
        default="",
        description="Sets the ISO for when the photobooth is in live preview modus. Very useful, when Camera does not support Exposure Simulation, and an external Flash is used. Only works when the camera is in manual. (Example Values: Auto, 100, 200, ...)",
    )

    gphoto2_iso_capture: str = Field(
        default="",
        description="Sets the ISO for when the photobooth captures a photo. Very useful, when Camera does not support Exposure Simulation, and an external Flash is used. Only works when the camera is in manual. (Example Values: Auto, 100, 200, ...)",
    )

    gphoto2_shutter_speed_liveview: str = Field(
        default="",
        description="Sets the shutter speed for the camera during the photobooth's live preview mode. Very useful, when Camera does not support Exposure Simulation, and an external Flash is used. This setting is effective only when the camera is in manual mode. (Example Values: 1, 1/5, 1/20, 1/30, 1/60, 1/1000, 1/4000, ...) Choose a very high default shutter speed in combination with Auto iso to emulate auto exposure. ",
    )

    gphoto2_shutter_speed_capture: str = Field(
        default="",
        description="Configures the shutter speed for the camera at the time of capturing a photo in the photobooth. Very useful, when Camera does not support Exposure Simulation, and an external Flash is used. Operational only in manual mode. (Example Values: 1/60, 1/320, 1/1000, 1/2000, 1/4000, ...)",
    )

    cv2_CAM_RESOLUTION_WIDTH: int = Field(
        default=10000,
        description="still photo camera resolution width to opencv2 backend",
    )
    cv2_CAM_RESOLUTION_HEIGHT: int = Field(
        default=10000,
        description="still photo camera resolution height to opencv2 backend",
    )
    cv2_device_index: int = Field(
        default=0,
        description="Device index of webcam opened in cv2 backend",
    )
    cv2_CAMERA_TRANSFORM_HFLIP: bool = Field(
        default=False,
        description="Apply horizontal flip to image source to opencv2 backend",
    )
    cv2_CAMERA_TRANSFORM_VFLIP: bool = Field(
        default=False,
        description="Apply vertical flip to image source to opencv2 backend",
    )

    v4l_CAM_RESOLUTION_WIDTH: int = Field(
        default=10000,
        description="still photo camera resolution width on supported backends",
    )
    v4l_CAM_RESOLUTION_HEIGHT: int = Field(
        default=10000,
        description="still photo camera resolution height on supported backends",
    )
    v4l_device_index: int = Field(
        default=0,
        description="Device index of webcam opened in v4l backend",
    )

    gphoto2_disable_viewfinder_before_capture: bool = Field(
        default=True,
        description="Disable viewfinder before capture might speed up following capture autofocus. Might not work with every camera.",
    )

    gphoto2_wait_event_after_capture_trigger: bool = Field(
        default=False,
        description="Usually wait_for_event not necessary before downloading the file from camera. Adjust if necessary.",
    )

    digicamcontrol_base_url: str = Field(
        default="http://127.0.0.1:5513",
        description="Base URL used to connect to the host running the digicamcontrol software. Usually photobooth-app and digicamcontrol are on the same computer and no adjustmend needed.",
    )

    picamera2_CAPTURE_CAM_RESOLUTION_WIDTH: int = Field(
        default=1280,
        description="camera resolution width to capture high resolution photo",
    )
    picamera2_CAPTURE_CAM_RESOLUTION_HEIGHT: int = Field(
        default=720,
        description="camera resolution height to capture high resolution photo",
    )
    picamera2_PREVIEW_CAM_RESOLUTION_WIDTH: int = Field(
        default=1280,
        ge=500,
        le=3500,  # hardware encoder in pi only supports max 4000 width/height
        description="camera resolution width to capture live video",
    )
    picamera2_PREVIEW_CAM_RESOLUTION_HEIGHT: int = Field(
        default=720,
        ge=500,
        le=2500,  # hardware encoder in pi only supports max 4000 width/height
        description="camera resolution height to capture live video",
    )
    picamera2_LIVEVIEW_RESOLUTION_WIDTH: int = Field(
        default=1280,
        ge=500,
        le=3500,  # hardware encoder in pi only supports max 4000 width/height
        description="actual resolution width for liveview stream",
    )
    picamera2_LIVEVIEW_RESOLUTION_HEIGHT: int = Field(
        default=720,
        ge=500,
        le=2500,  # hardware encoder in pi only supports max 4000 width/height
        description="actual resolution height for liveview stream",
    )
    picamera2_CAMERA_TRANSFORM_HFLIP: bool = Field(
        default=False,
        description="Apply horizontal flip to image source to picamera2 backend",
    )
    picamera2_CAMERA_TRANSFORM_VFLIP: bool = Field(
        default=False,
        description="Apply vertical flip to image source to picamera2 backend",
    )
    picamera2_AE_EXPOSURE_MODE: int = Field(
        default=1,
        ge=0,
        le=4,
        description="Usually 0=normal exposure, 1=short, 2=long, 3=custom. Not all necessarily supported by camera!",
    )
    picamera2_stream_quality: EnumPicamStreamQuality = Field(
        title="Picamera2 Stream Quality (for livepreview)",
        default=EnumPicamStreamQuality.MEDIUM,
        description="Lower quality results in less data to be transferred and may reduce load on display device.",
    )


class EnumPilgramFilter(str, Enum):
    """enum to choose image filter from, pilgram filter"""

    original = "original"

    _1977 = "_1977"
    aden = "aden"
    ashby = "ashby"
    amaro = "amaro"
    brannan = "brannan"
    brooklyn = "brooklyn"
    charmes = "charmes"
    clarendon = "clarendon"
    crema = "crema"
    dogpatch = "dogpatch"
    earlybird = "earlybird"
    gingham = "gingham"
    ginza = "ginza"
    hefe = "hefe"
    helena = "helena"
    hudson = "hudson"
    inkwell = "inkwell"
    juno = "juno"
    kelvin = "kelvin"
    lark = "lark"
    lofi = "lofi"
    ludwig = "ludwig"
    maven = "maven"
    mayfair = "mayfair"
    moon = "moon"
    nashville = "nashville"
    perpetua = "perpetua"
    poprocket = "poprocket"
    reyes = "reyes"
    rise = "rise"
    sierra = "sierra"
    skyline = "skyline"
    slumber = "slumber"
    stinson = "stinson"
    sutro = "sutro"
    toaster = "toaster"
    valencia = "valencia"
    walden = "walden"
    willow = "willow"
    xpro2 = "xpro2"


class TextsConfig(BaseModel):
    text: str = ""
    pos_x: NonNegativeInt = 50
    pos_y: NonNegativeInt = 50
    rotate: int = 0
    font_size: PositiveInt = 40
    font: str = "fonts/Roboto-Bold.ttf"
    color: Color = Color("red").as_named()


class CollageMergeDefinition(BaseModel):
    pos_x: NonNegativeInt = 50
    pos_y: NonNegativeInt = 50
    width: NonNegativeInt = 600
    height: NonNegativeInt = 600
    rotate: int = 0
    predefined_image: str = ""
    filter: EnumPilgramFilter = EnumPilgramFilter.original


class GroupMediaprocessing(BaseModel):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Process media after capture")

    HIRES_STILL_QUALITY: int = Field(
        default=90,
        ge=10,
        le=100,
        description="Still JPEG full resolution quality, applied to download images and images with filter",
        json_schema_extra={"ui_component": "QSlider"},
    )
    LIVEPREVIEW_QUALITY: int = Field(
        default=80,
        ge=10,
        le=100,
        description="Livepreview stream JPEG image quality on supported backends",
        json_schema_extra={"ui_component": "QSlider"},
    )
    THUMBNAIL_STILL_QUALITY: int = Field(
        default=60,
        ge=10,
        le=100,
        description="Still JPEG thumbnail quality, thumbs used in gallery list",
        json_schema_extra={"ui_component": "QSlider"},
    )
    PREVIEW_STILL_QUALITY: int = Field(
        default=75,
        ge=10,
        le=100,
        description="Still JPEG preview quality, preview still shown in gallery detail",
        json_schema_extra={"ui_component": "QSlider"},
    )

    FULL_STILL_WIDTH: int = Field(
        default=1500,
        ge=800,
        le=5000,
        description="Width of resized full image with filters applied. For performance choose as low as possible but still gives decent print quality. Example: 1500/6inch=250dpi",
    )
    PREVIEW_STILL_WIDTH: int = Field(
        default=1200,
        ge=200,
        le=2500,
        description="Width of resized preview image, height is automatically calculated to keep aspect ratio",
    )
    THUMBNAIL_STILL_WIDTH: int = Field(
        default=400,
        ge=100,
        le=1000,
        description="Width of resized thumbnail image, height is automatically calculated to keep aspect ratio",
    )

    removechromakey_enable: bool = Field(
        default=False,
        description="Apply chromakey greenscreen removal from captured images",
    )
    removechromakey_keycolor: int = Field(
        default=110,
        ge=0,
        le=360,
        description="Color (H) in HSV colorspace to remove on 360° scale.",
    )
    removechromakey_tolerance: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Tolerance for color (H) on chromakey color removal.",
    )


class GroupMediaprocessingPipelineSingleImage(BaseModel):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Postprocess single captures")

    pipeline_enable: bool = Field(
        default=True,
        description="Enable/Disable processing pipeline completely",
    )

    filter: EnumPilgramFilter = Field(
        title="Pic1 Filter",
        default=EnumPilgramFilter.original,
        description="Instagram-like filter to apply per default. 'original' applies no filter.",
    )
    fill_background_enable: bool = Field(
        default=False,
        description="Apply solid color background to captured image (useful only if image is extended or background removed)",
    )
    fill_background_color: Color = Field(
        default=Color("blue").as_named(),
        description="Solid color used to fill background.",
    )
    img_background_enable: bool = Field(
        default=False,
        description="Add image from file to background (useful only if image is extended or background removed)",
    )
    img_background_file: str = Field(
        default="backgrounds/pink-7761356_1920.jpg",
        description="Image file to use as background filling transparent area. File needs to be located in DATA_DIR/*",
    )
    img_frame_enable: bool = Field(
        default=True,
        description="Mount captured image to frame.",
    )
    img_frame_file: str = Field(
        default="frames/polaroid-6125402_1pic.png",
        description="Image file to which the captured image is mounted to. Frame determines the output image size! Photos are visible through transparant parts. Image needs to be transparent (PNG). File needs to be located in userdata/*",
    )
    texts_enable: bool = Field(
        default=True,
        description="General enable apply texts below.",
    )
    texts: list[TextsConfig] = Field(
        default=[
            TextsConfig(
                text="Some Text!",  # use {date} and {time} to add dynamic texts; cannot use in default because tests will fail that compare images
                pos_x=300,
                pos_y=900,
                rotate=-3,
                color=Color("black"),
            ),
        ],
        description="Text to overlay on images after capture. Pos_x/Pos_y measure in pixel starting 0/0 at top-left in image. Font to use in text stages. File needs to be located in DATA_DIR/*",
    )


class GroupMediaprocessingPipelineCollage(BaseModel):
    """Configure stages how to process collage after capture."""

    model_config = ConfigDict(title="Process collage after capture")

    ## phase 1 per capture application on collage also. settings taken from PipelineImage if needed

    capture_fill_background_enable: bool = Field(
        default=False,
        description="Apply solid color background to captured image (useful only if image is extended or background removed)",
    )
    capture_fill_background_color: Color = Field(
        default=Color("blue").as_named(),
        description="Solid color used to fill background.",
    )
    capture_img_background_enable: bool = Field(
        default=False,
        description="Add image from file to background (useful only if image is extended or background removed)",
    )
    capture_img_background_file: str = Field(
        default="backgrounds/pink-7761356_1920.jpg",
        description="Image file to use as background filling transparent area. File needs to be located in DATA_DIR/*",
    )

    ## phase 2 per collage settings.

    canvas_width: int = Field(
        default=1920,
        description="Width (X) in pixel of collage image. The higher the better the quality but also longer time to process. All processes keep aspect ratio.",
    )
    canvas_height: int = Field(
        default=1080,
        description="Height (Y) in pixel of collage image. The higher the better the quality but also longer time to process. All processes keep aspect ratio.",
    )
    canvas_merge_definition: list[CollageMergeDefinition] = Field(
        default=[
            CollageMergeDefinition(pos_x=215, pos_y=122, width=660, height=660, rotate=-2, filter=EnumPilgramFilter.earlybird),
            CollageMergeDefinition(
                pos_x=1072,
                pos_y=122,
                width=660,
                height=660,
                rotate=-3,
                filter=EnumPilgramFilter.mayfair,
                predefined_image="predefined_images/pexels-marcelo-miranda-7708722.jpg",
            ),
        ],
        description="How to arrange single images in the collage. Pos_x/Pos_y measure in pixel starting 0/0 at top-left in image. Width/Height in pixels. Aspect ratio is kept always. Predefined image files are used instead a camera capture. File needs to be located in DATA_DIR/*",
    )
    canvas_fill_background_enable: bool = Field(
        default=False,
        description="Apply solid color background to collage",
    )
    canvas_fill_background_color: Color = Field(
        default=Color("green").as_named(),
        description="Solid color used to fill background.",
    )
    canvas_img_background_enable: bool = Field(
        default=False,
        description="Add image from file to background.",
    )
    canvas_img_background_file: str = Field(
        default="backgrounds/pink-7761356_1920.jpg",
        description="Image file to use as background filling transparent area. File needs to be located in userdata/*",
    )
    canvas_img_front_enable: bool = Field(
        default=True,
        description="Overlay image on canvas image.",
    )
    canvas_img_front_file: str = Field(
        default="frames/polaroid-6125402_1920.png",
        description="Image file to paste on top over photos and backgrounds. Photos are visible only through transparant parts. Image needs to be transparent (PNG). File needs to be located in DATA_DIR/*",
    )
    canvas_texts_enable: bool = Field(
        default=True,
        description="General enable apply texts below.",
    )
    canvas_texts: list[TextsConfig] = Field(
        default=[
            TextsConfig(
                text="Nice Collage Text!",
                pos_x=300,
                pos_y=800,
                rotate=-3,
                color=Color("black"),
            ),
        ],
        description="Text to overlay on final collage. Pos_x/Pos_y measure in pixel starting 0/0 at top-left in image. Font to use in text stages. File needs to be located in DATA_DIR/*",
    )


class GroupMediaprocessingPipelinePrint(BaseModel):
    """Configure stages how to process mediaitem before printing on paper."""

    model_config = ConfigDict(title="Process mediaitem before printing on paper")


class GroupHardwareInputOutput(BaseModel):
    """
    Configure hardware GPIO, keyboard and more. Find integration information in the documentation.
    """

    model_config = ConfigDict(title="Hardware Input/Output Config")

    # keyboardservice config
    keyboard_input_enabled: bool = Field(
        default=False,
        description="Enable keyboard input globally",
    )
    keyboard_input_keycode_takepic: str = Field(
        default="i",
        description="Keycode triggers capture of one image",
    )
    keyboard_input_keycode_takecollage: str = Field(
        default="c",
        description="Keycode triggers capture of collage",
    )
    keyboard_input_keycode_print_recent_item: str = Field(
        default="p",
        description="Keycode triggers printing most recent image captured",
    )

    # WledService Config
    wled_enabled: bool = Field(
        default=False,
        description="Enable WLED integration for user feedback during countdown and capture by LEDs.",
    )
    wled_serial_port: str = Field(
        default="",
        description="Serial port the WLED device is connected to.",
    )

    # GpioService Config
    gpio_enabled: bool = Field(
        default=False,
        description="Enable Raspberry Pi GPIOzero integration.",
    )
    gpio_pin_shutdown: int = Field(
        default=17,
        description="GPIO pin to shutdown after holding it for 2 seconds.",
    )
    gpio_pin_reboot: int = Field(
        default=18,
        description="GPIO pin to reboot after holding it for 2 seconds.",
    )
    gpio_pin_take1pic: int = Field(
        default=27,
        description="GPIO pin to take one picture.",
    )
    gpio_pin_collage: int = Field(
        default=22,
        description="GPIO pin to take a collage.",
    )
    gpio_pin_print_recent_item: int = Field(
        default=23,
        description="GPIO pin to print last captured item.",
    )

    # PrintingService Config
    printing_enabled: bool = Field(
        default=False,
        description="Enable printing in general.",
    )
    printing_command: str = Field(
        default="mspaint /p {filename}",
        description="Command issued to print. Use {filename} as placeholder for the JPEG image to be printed.",
    )
    printing_blocked_time: int = Field(
        default=20,
        description="Block queue print until time is passed. Time in seconds.",
    )


class GroupUiSettings(BaseModel):
    """Personalize the booth's UI."""

    model_config = ConfigDict(title="Personalize the User Interface")

    show_takepic_on_frontpage: bool = Field(
        default=True,
        description="Show link to capture single picture on frontpage.",
    )
    show_collage_on_frontpage: bool = Field(
        default=True,
        description="Show link to capture collage on frontpage.",
    )
    show_gallery_on_frontpage: bool = Field(
        default=True,
        description="Show link to gallery on frontpage.",
    )
    show_admin_on_frontpage: bool = Field(
        default=True,
        description="Show link to admin center, usually only during setup.",
    )

    livestream_mirror_effect: bool = Field(
        default=True,
        description="Flip livestream horizontally to create a mirror effect feeling more natural to users.",
    )
    FRONTPAGE_TEXT: str = Field(
        default='<div class="fixed-center text-h2 text-weight-bold text-center text-white" style="text-shadow: 4px 4px 4px #666;">Hey!<br>Let\'s take some pictures! <br>📷💕</div>',
        description="Text/HTML displayed on frontpage.",
    )

    TAKEPIC_MSG_TIME: float = Field(
        default=0.5,
        description="Offset in seconds, the smile-icon shall be shown.",
    )
    AUTOCLOSE_NEW_ITEM_ARRIVED: int = Field(
        default=30,
        description="Timeout in seconds a new item popup closes automatically.",
    )

    GALLERY_EMPTY_MSG: str = Field(
        default='<div class="fixed-center text-h2 text-weight-bold text-center text-white" style="text-shadow: 4px 4px 4px #666;">Empty, Zero, Nada! 🤷‍♂️<br>Let\'s take some pictures! <br>📷💕</div>',
        description="Message displayed if gallery is empty.",
    )
    gallery_show_qrcode: bool = Field(
        default=True,
        description="Show QR code in gallery. If shareservice is enabled the URL is automatically generated, if not go to share config and provide URL.",
    )
    gallery_show_filter: bool = Field(
        default=True,
        description="Show instagramlike filter (pilgram2).",
    )
    gallery_filter_userselectable: list[EnumPilgramFilter] = Field(
        title="Pic1 Filter Userselectable",
        default=[e.value for e in EnumPilgramFilter],
        description="Filter the user may choose from in the gallery. 'original' applies no filter.",
    )
    gallery_show_download: bool = Field(
        default=True,
        description="Show download button in gallery.",
    )
    gallery_show_delete: bool = Field(
        default=True,
        description="Show delete button for items in gallery.",
    )
    gallery_show_print: bool = Field(
        default=True,
        description="Show print button for items in gallery.",
    )


class GroupFileTransfer(BaseModel):
    """Configuration for USB File Transfer Service."""

    model_config = ConfigDict(title="USB File Transfer Service Config")

    enabled: bool = Field(
        default=False,
        description="Enable the automatic file transfer to USB service. Files are copied when the USB drive is inserted.",
    )
    target_folder_name: str = Field(
        default="photobooth",
        description="Name of the top-level folder on the USB drive where files will be copied to.",
    )


class GroupMisc(BaseModel):
    """
    Quite advanced, usually not necessary to touch.
    """

    model_config = ConfigDict(title="Miscellaneous Config")


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding")
        field_value = None
        try:
            file_content_json = json.loads(Path(CONFIG_FILENAME).read_text(encoding))
            field_value = file_content_json.get(field_name)
        except FileNotFoundError:
            # ignore file not found, because it could have been deleted or not yet initialized
            # using defaults
            pass

        return field_value, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                d[field_key] = field_value

        return d


class AppConfig(BaseSettings):
    """
    AppConfig class glueing all together

    In the case where a value is specified for the same Settings field in multiple ways, the selected value is determined as follows (in descending order of priority):

    1 Arguments passed to the Settings class initialiser.
    2 Environment variables, e.g. my_prefix_special_function as described above.
    3 Variables loaded from a dotenv (.env) file.
    4 Variables loaded from the secrets directory.
    5 The default field values for the Settings model.
    """

    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)  # private attributes

    # groups -> setting items
    common: GroupCommon = GroupCommon()
    sharing: GroupSharing = GroupSharing()
    filetransfer: GroupFileTransfer = GroupFileTransfer()
    mediaprocessing: GroupMediaprocessing = GroupMediaprocessing()
    mediaprocessing_pipeline_singleimage: GroupMediaprocessingPipelineSingleImage = GroupMediaprocessingPipelineSingleImage()
    mediaprocessing_pipeline_collage: GroupMediaprocessingPipelineCollage = GroupMediaprocessingPipelineCollage()
    mediaprocessing_pipeline_printing: GroupMediaprocessingPipelinePrint = GroupMediaprocessingPipelinePrint()
    uisettings: GroupUiSettings = GroupUiSettings()
    backends: GroupBackends = GroupBackends()
    hardwareinputoutput: GroupHardwareInputOutput = GroupHardwareInputOutput()
    misc: GroupMisc = GroupMisc()

    # TODO[pydantic]: We couldn't refactor this class, please create the `model_config` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        # first in following list is least important; last .env file overwrites the other.
        env_file=[".env.installer", ".env.dev", ".env.test", ".env.prod"],
        env_nested_delimiter="__",
        case_sensitive=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """customize sources"""
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )

    def get_schema(self, schema_type: str = "default"):
        """Get schema to build UI. Schema is polished to the needs of UI"""
        if schema_type == "dereferenced":
            # https://github.com/pydantic/pydantic/issues/889#issuecomment-1064688675
            return jsonref.loads(json.dumps(self.model_json_schema()))

        return self.model_json_schema()

    def persist(self):
        """Persist config to file"""
        logger.debug("persist config to json file")

        with open(CONFIG_FILENAME, mode="w", encoding="utf-8") as write_file:
            write_file.write(self.model_dump_json(indent=2))

    def deleteconfig(self):
        """Reset to defaults"""
        logger.debug("config reset to default")

        try:
            os.remove(CONFIG_FILENAME)
            logger.debug(f"deleted {CONFIG_FILENAME} file.")
        except (FileNotFoundError, PermissionError):
            logger.info(f"delete {CONFIG_FILENAME} file failed.")

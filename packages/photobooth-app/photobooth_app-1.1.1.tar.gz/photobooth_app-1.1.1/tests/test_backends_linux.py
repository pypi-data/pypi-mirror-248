import io
import logging
import os
import platform

import pytest
from PIL import Image

from photobooth.services.config import appconfig

from .backends_utils import get_images


@pytest.fixture(autouse=True)
def run_around_tests():
    appconfig.reset_defaults()

    yield


logger = logging.getLogger(name=None)

"""
prepare config for testing
"""


## check skip if wrong platform
if not platform.system() == "Linux":
    pytest.skip(
        "tests are linux only platform, skipping test",
        allow_module_level=True,
    )


@pytest.fixture()
def backend_v4l():
    from photobooth.services.backends.webcamv4l import WebcamV4lBackend
    from photobooth.services.backends.webcamv4l import available_camera_indexes as v4l_avail

    # setup
    backend = WebcamV4lBackend()

    logger.info("probing for available cameras")
    _availableCameraIndexes = v4l_avail()
    if not _availableCameraIndexes:
        pytest.skip("no camera found, skipping test")

    cameraIndex = _availableCameraIndexes[0]

    logger.info(f"available camera indexes: {_availableCameraIndexes}")
    logger.info(f"using first camera index to test: {cameraIndex}")

    appconfig.backends.v4l_device_index = cameraIndex

    # deliver
    backend.start()
    yield backend
    backend.stop()


@pytest.fixture()
def backend_gphoto2():
    from photobooth.services.backends.gphoto2 import Gphoto2Backend
    from photobooth.services.backends.gphoto2 import available_camera_indexes as gp2_avail
    # ensure virtual camera is available (starting from gphoto2 2.5.0 always true)
    # assert has_vcam() # on selfhosted-runner currently a problem. TODO: setup new RPI runner

    # its checked whether camera is available, but actually never used the index, because it's assumed
    # only one DSLR is connected at a time.

    def use_vcam():
        import gphoto2 as gp

        logger.info(f"python-gphoto2: {gp.__version__}")

        # virtual camera delivers images from following path:
        os.environ["VCAMERADIR"] = os.path.join(os.path.dirname(__file__), "assets")
        # switch to virtual camera from normal drivers
        # IOLIBS is set on import of gphoto2:
        # https://github.com/jim-easterbrook/python-gphoto2/blob/510149d454c9fa1bd03a43f098eea3c52d2e0675/src/swig-gp2_5_31/__init__.py#L15C32-L15C32
        os.environ["IOLIBS"] = os.environ["IOLIBS"].replace("iolibs", "vusb")

        logger.info(os.environ["VCAMERADIR"])
        logger.info(os.environ["IOLIBS"])

    def has_vcam():
        import gphoto2 as gp

        if "IOLIBS" not in os.environ:
            logger.warning("missing IOLIBS in os.environ! installation is off.")
            return False

        vusb_dir = os.environ["IOLIBS"].replace("iolibs", "vusb")
        if not os.path.isdir(vusb_dir):
            logger.warning(f"missing {vusb_dir=}")
            return False
        gp_library_version = gp.gp_library_version(gp.GP_VERSION_SHORT)[0]
        gp_library_version = tuple(int(x) for x in gp_library_version.split("."))
        if gp_library_version > (2, 5, 30):
            return True

        logger.warning(f"{gp_library_version=} too old. usually libgphoto is delivered with pip package, so this should not happen!")

        return False

    # setup
    if not has_vcam():
        pytest.skip("system installation does not support virtual camera!")

    # use vcam
    use_vcam()

    _availableCameraIndexes = gp2_avail()
    if not _availableCameraIndexes:
        pytest.skip("no camera found, skipping test")

    backend = Gphoto2Backend()
    # deliver
    backend.start()
    yield backend
    backend.stop()


## tests


def test_get_images_webcamv4l(backend_v4l):
    # get lores and hires images from backend and assert
    get_images(backend_v4l)


def test_get_images_gphoto2(backend_gphoto2):
    # get lores and hires images from backend and assert

    with pytest.raises(TimeoutError):
        with Image.open(io.BytesIO(backend_gphoto2.wait_for_lores_image())) as img:
            img.verify()

    with Image.open(io.BytesIO(backend_gphoto2.wait_for_hq_image())) as img:
        img.verify()


def test_get_gphoto2_info():
    import gphoto2 as gp

    logger.info(f"python-gphoto2: {gp.__version__}")
    logger.info(f"libgphoto2: {gp.gp_library_version(gp.GP_VERSION_VERBOSE)}")
    logger.info(f"libgphoto2_port: {gp.gp_port_library_version(gp.GP_VERSION_VERBOSE)}")

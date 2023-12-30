r"""
Digicamcontrol backend implementation

Quirks:
    - using webfrontend only possible via IPv4! Sending requests first to localhost(IPV6) results in timeout,
      retry and a delay of 2 seconds on every request

How to use Livestream
    - URL: http://localhost:5513/liveview.jpg
    - URL to simple digicamcontrol remoteapp: localhost:5513
    - start liveview:
    - http://localhost:5513/?CMD=LiveViewWnd_Show
    - http://localhost:5513/?CMD=All_Minimize  (issue at least one time to hide live preview, window should not popup on further liveview-starts)
    - stop liveview:
    - http://localhost:5513/?CMD=LiveViewWnd_Hide
    - capture from liveview (bad quality):
    - http://localhost:5513/?CMD=LiveView_Capture

Capture photo

via webinterface:
    - capture regular photo:
    http://localhost:5513/?slc=set&param1=session.folder&param2=c:\pictures
    http://localhost:5513/?slc=set&param1=session.filenametemplate&param2=capture1
    http://localhost:5513/?slc=capture&param1=&param2=
    - get session data for debugging:
    - http://localhost:5513/session.json
    - download photos:
    - specific file: http://localhost:5513/image/DSC_0001.jpg
    - last pic taken: http://localhost:5513/?slc=get&param1=lastcaptured&param2= ("returns a character if capture in progress")

via remotecmd
    - capture regular photo:
    CameraControlRemoteCmd.exe /c capture c:\pictures\capture1.jpg

"""


import dataclasses
import logging
import tempfile
import time
import urllib.parse
from pathlib import Path
from threading import Condition, Event

import requests

from ...utils.exceptions import ShutdownInProcessError
from ...utils.stoppablethread import StoppableThread
from ..config import appconfig
from .abstractbackend import AbstractBackend

logger = logging.getLogger(__name__)


class DigicamcontrolBackend(AbstractBackend):
    """
    The backend implementation using gphoto2
    """

    @dataclasses.dataclass
    class DigicamcontrolDataBytes:
        """
        bundle data bytes and it's condition.
        1) save some instance attributes and
        2) bundle as it makes sense
        """

        # jpeg data as bytes
        data: bytes = None
        # signal to producer that requesting thread is ready to be notified
        request_ready: Event = None
        # condition when frame is avail
        condition: Condition = None

    def __init__(self):
        super().__init__()

        # self._camera = gp.Camera()
        # self._camera_context = gp.Context()
        self._camera_connected = False

        self._hires_data: __class__.DigicamcontrolDataBytes = __class__.DigicamcontrolDataBytes(
            data=None,
            request_ready=Event(),
            condition=Condition(),
        )
        self._lores_data: __class__.DigicamcontrolDataBytes = __class__.DigicamcontrolDataBytes(
            data=None,
            condition=Condition(),
        )

        # worker threads
        self._worker_thread: StoppableThread = None
        self._connect_thread = StoppableThread(name="digicamcontrol_connect_thread", target=self._connect_fun, daemon=True)

    def start(self):
        """To start the FrameServer, you will also need to start the Picamera2 object."""

        self._connect_thread.start()

        logger.debug(f"{self.__module__} started")

        super().start()

    def stop(self):
        super().stop()

        if self._connect_thread and self._connect_thread.is_alive():
            self._connect_thread.stop()

            logger.debug(f"{self.__module__} waiting to join _connect_thread")
            self._connect_thread.join()
            logger.debug(f"{self.__module__} joined _connect_thread")

        logger.debug(f"{self.__module__} stopped")

    def wait_for_hq_image(self):
        """
        for other threads to receive a hq JPEG image
        mode switches are handled internally automatically, no separate trigger necessary
        this function blocks until frame is received
        raise TimeoutError if no frame was received
        """
        with self._hires_data.condition:
            self._hires_data.request_ready.set()

            if not self._hires_data.condition.wait(timeout=4):
                raise TimeoutError("timeout receiving frames")

        self._hires_data.request_ready.clear()
        return self._hires_data.data

    #
    # INTERNAL FUNCTIONS
    #

    def _check_camera_preview_available(self):
        """Test on init whether preview is available for this camera."""
        try:
            self._wait_for_lores_image()
        except Exception as exc:
            logger.info(f"gather preview failed. consider to disable permanently! {exc}")
        else:
            logger.info("preview is available")

    def _wait_for_lores_image(self):
        """for other threads to receive a lores JPEG image"""
        with self._lores_data.condition:
            if not self._lores_data.condition.wait(timeout=0.2):
                if self._worker_thread and self._worker_thread.stopped():
                    raise ShutdownInProcessError("shutdown in progress")
                else:
                    raise TimeoutError("timeout receiving frames")

            return self._lores_data.data

    def _on_capture_mode(self):
        logger.debug("change to capture mode - nothing needs to be done actually")

    def _on_preview_mode(self):
        logger.debug("enable liveview and minimize windows")
        try:
            session = requests.Session()
            r = session.get(f"{appconfig.backends.digicamcontrol_base_url}/?CMD=LiveViewWnd_Show")
            assert r.status_code == 200
            if not r.ok:
                raise RuntimeError(f"error starting liveview {r.text}")

            r = session.get(f"{appconfig.backends.digicamcontrol_base_url}/?CMD=All_Minimize")
            assert r.status_code == 200
            if not r.ok:
                raise RuntimeError(f"error minimize liveview {r.text}")

        except Exception as exc:
            logger.exception(exc)
            logger.error("fail set preview mode! no power? no connection?")
        else:
            logger.debug(f"{self.__module__} set preview mode successful")

    #
    # INTERNAL IMAGE GENERATOR
    #
    def _connect_fun(self):
        while not self._connect_thread.stopped():  # repeat until stopped
            if self._camera_connected:
                # if connected, just do nothing and continue with next loop some time later
                time.sleep(1)
                continue

            # camera not yet connected or disconnected due to whatever reason.
            # try to reconnect

            # check for available devices
            if not self.available_camera_indexes():
                logger.critical("no camera detected. waiting until camera available")
                time.sleep(5)  # wait additional time to not flood logs in seconds
                continue

            # at this point a camera was detected, try to connect.

            # start camera

            try:
                session = requests.Session()
                r = session.get(appconfig.backends.digicamcontrol_base_url)
                assert r.status_code == 200
                if not r.ok:
                    raise RuntimeError(f"error connecting to digicam webservice {r.text}")
            except Exception as exc:
                logger.exception(exc)
                logger.critical("camera failed to initialize. no power? no connection?")
            else:
                self._camera_connected = True
                logger.debug(f"{self.__module__} camera connected")

            if appconfig.backends.LIVEPREVIEW_ENABLED:
                self._check_camera_preview_available()

            self._worker_thread = StoppableThread(name="digicamcontrol_worker_thread", target=self._worker_fun, daemon=True)
            self._worker_thread.start()

            # short sleep until backend started.
            time.sleep(0.5)

            # after connection set preview mode to enable liveview.
            self._on_preview_mode()

        # supervising connection thread was asked to stop - so we ask to stop worker fun also
        if self._worker_thread:
            self._worker_thread.stop()
            self._worker_thread.join()

    def _worker_fun(self):
        logger.debug("starting digicamcontrol worker function")

        session = requests.Session()
        preview_failcounter = 0

        while not self._worker_thread.stopped():  # repeat until stopped
            if self._hires_data.request_ready.is_set():
                # only capture one pic and return to lores streaming afterwards
                self._hires_data.request_ready.clear()

                logger.debug("triggered capture")

                self._on_capture_mode()

                try:
                    # capture request, afterwards read file to buffer
                    tmp_dir = tempfile.gettempdir()

                    logger.info(f"requesting digicamcontrol to store files to {tmp_dir=}")

                    r = session.get(
                        f"{appconfig.backends.digicamcontrol_base_url}/?slc=set&param1=session.folder&param2={urllib.parse.quote(tmp_dir, safe='')}"  # noqa: E501
                    )
                    assert r.status_code == 200
                    if not r.text == "OK":
                        raise RuntimeError(f"error setting directory {r.text}")

                    r = session.get(f"{appconfig.backends.digicamcontrol_base_url}/?slc=capture&param1=&param2=")
                    assert r.status_code == 200
                    if not r.text == "OK":
                        raise RuntimeError(f"error capture {r.text}")

                    r = session.get(f"{appconfig.backends.digicamcontrol_base_url}/?slc=get&param1=lastcaptured&param2=")
                    assert r.status_code == 200
                    if r.text in ("-", "?"):  # "-" means capture in progress, "?" means not yet an image captured
                        error_translation = {"-": "capture still in process", "?": "not yet an image captured"}
                        raise RuntimeError(f"error retrieving capture, {error_translation[r.text]}")

                    # at this point it's assumed that r.text holds the filename:
                    captured_filepath = Path(tmp_dir, r.text)

                    logger.info(f"trying to open captured file {captured_filepath}")
                    with open(captured_filepath, "rb") as fh:
                        img_bytes = fh.read()

                except Exception as exc:
                    logger.critical(f"error capture! check logs for errors. {exc}")

                    # try again in next loop
                    continue

                with self._hires_data.condition:
                    self._hires_data.data = img_bytes
                    self._hires_data.condition.notify_all()

                # switch back to preview mode
                self._on_preview_mode()

            else:
                if appconfig.backends.LIVEPREVIEW_ENABLED:
                    try:
                        r = session.get(f"{appconfig.backends.digicamcontrol_base_url}/liveview.jpg")
                        # r = session.get("http://127.0.0.1:5514/live") #different port also!
                        assert r.status_code == 200

                        if not r.ok:
                            raise RuntimeError(f"error receiving jpg from digicamcontrol {r.status_code} {r.text}")

                        if self._lores_data.data and (self._lores_data.data == r.content):
                            raise RuntimeError(
                                "received same frame again - digicamcontrol liveview might be closed or delivers "
                                "low framerate only. Consider to reduce resolution or Livepreview Framerate."
                            )

                    except Exception as exc:
                        preview_failcounter += 1

                        if preview_failcounter <= 10:
                            logger.warning(f"error capturing frame from DSLR: {exc}")
                            # abort this loop iteration and continue sleeping...
                            time.sleep(0.5)  # add another delay to avoid flooding logs

                            continue
                        else:
                            logger.critical(f"aborting capturing frame, camera disconnected? {exc}")
                            self._camera_connected = False
                            break
                    else:
                        preview_failcounter = 0

                    with self._lores_data.condition:
                        self._lores_data.data = r.content
                        self._lores_data.condition.notify_all()

                    # limit fps to a reasonable amount. otherwise getting liveview.jpg would lead to 100% cpu as it's getting images way too often.
                    time.sleep(0.1)

            # wait for trigger...
            time.sleep(0.05)

        logger.warning("_worker_fun exits")

    def available_camera_indexes(self):
        """
        find available cameras, return valid indexes.
        """

        available_identifiers = []
        session = requests.Session()

        try:
            r = session.get(f"{appconfig.backends.digicamcontrol_base_url}?slc=list&param1=cameras&param2=")
            assert r.status_code == 200

            if not r.ok:
                raise RuntimeError(f"error checking avail cameras {r.text}")

            for line in r.iter_lines():
                if line:
                    available_identifiers.append(line)

        except requests.exceptions.RequestException as exc:
            logger.error(f"error checking for cameras. Cant connect to digicamcontrol webserver! {exc}")
        except RuntimeError as exc:
            logger.error(f"error checking avail cameras {exc}")

        logger.info(f"camera list: {available_identifiers}")
        if not available_identifiers:
            logger.warning("no camera detected")

        return available_identifiers

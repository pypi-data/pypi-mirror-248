import io
import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from PIL import Image

from ..appconfig import EnumPilgramFilter
from ..containers import ApplicationContainer
from ..services.mediacollectionservice import MediacollectionService
from ..services.mediaprocessing.image_pipelinestages import pilgram_stage
from ..services.mediaprocessingservice import MediaprocessingService
from ..utils.exceptions import PipelineError

logger = logging.getLogger(__name__)
mediaprocessing_router = APIRouter(
    prefix="/mediaprocessing",
    tags=["mediaprocessing"],
)


@mediaprocessing_router.get("/preview/{mediaitem_id}/{filter}", response_class=Response)
@inject
def api_get_preview_image_filtered(
    mediaitem_id,
    filter=None,
    mediacollection_service: MediacollectionService = Depends(Provide[ApplicationContainer.services.mediacollection_service]),
):
    try:
        mediaitem = mediacollection_service.db_get_image_by_id(item_id=mediaitem_id)

        image = Image.open(mediaitem.path_thumbnail_unprocessed)
    except FileNotFoundError as exc:
        # either db_get_image_by_id or open both raise FileNotFoundErrors if file/db entry not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{mediaitem_id=} cannot be found. {exc}",
        ) from exc

    try:
        if not (filter is None or filter == "original"):
            image = pilgram_stage(image, filter)
    except PipelineError as exc:
        logger.error(f"apply pilgram_stage failed, reason: {exc}.")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{filter=} cannot be found. {exc}",
        ) from exc

    buffer_preview_pipeline_applied = io.BytesIO()
    image.save(
        buffer_preview_pipeline_applied,
        format="jpeg",
        quality=80,
        optimize=False,
    )
    return Response(content=buffer_preview_pipeline_applied.getvalue(), media_type="image/jpeg")


@mediaprocessing_router.get("/applyfilter/{mediaitem_id}/{filter}")
@inject
def api_get_applyfilter(
    mediaitem_id,
    filter: str = None,
    mediacollection_service: MediacollectionService = Depends(Provide[ApplicationContainer.services.mediacollection_service]),
    mediaprocessing_service: MediaprocessingService = Depends(Provide[ApplicationContainer.services.mediaprocessing_service]),
):
    try:
        if not mediaprocessing_service._config.mediaprocessing_pipeline_singleimage.pipeline_enable:
            raise RuntimeError("singleimage pipeline needs to be enabled!")

        mediaitem = mediacollection_service.db_get_image_by_id(item_id=mediaitem_id)

        # create updated config that is the image is processed according to
        config = mediaprocessing_service._config.mediaprocessing_pipeline_singleimage.model_copy()

        config.filter = EnumPilgramFilter(filter)

        mediaprocessing_service.process_singleimage(mediaitem, config)
    except Exception as exc:
        logger.exception(exc)
        logger.error(f"apply pipeline failed, reason: {exc}.")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"apply pipeline failed, reason: {exc}.",
        ) from exc

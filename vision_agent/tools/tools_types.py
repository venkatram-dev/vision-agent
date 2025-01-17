from uuid import UUID
from enum import Enum
from typing import List, Tuple, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer, SerializationInfo


class BboxInput(BaseModel):
    image_path: str
    labels: List[str]
    bboxes: List[Tuple[int, int, int, int]]


class BboxInputBase64(BaseModel):
    image: str
    filename: str
    labels: List[str]
    bboxes: List[Tuple[int, int, int, int]]


class PromptTask(str, Enum):
    """
    Valid task prompts options for the Florencev2 model.
    """

    CAPTION = "<CAPTION>"
    """"""
    CAPTION_TO_PHRASE_GROUNDING = "<CAPTION_TO_PHRASE_GROUNDING>"
    """"""
    OBJECT_DETECTION = "<OD>"
    """"""


class FineTuning(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    job_id: UUID = Field(alias="jobId")

    @field_serializer("job_id")
    def serialize_job_id(self, job_id: UUID, _info: SerializationInfo) -> str:
        return str(job_id)


class Florencev2FtRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    image: str
    task: PromptTask
    tool: str
    prompt: Optional[str] = ""
    fine_tuning: Optional[FineTuning] = Field(None, alias="fineTuning")


class JobStatus(str, Enum):
    """The status of a fine-tuning job.

    CREATED:
        The job has been created and is waiting to be scheduled to run.
    STARTING:
        The job has started running, but not entering the training phase.
    TRAINING:
        The job is training a model.
    EVALUATING:
        The job is evaluating the model and computing metrics.
    PUBLISHING:
        The job is exporting the artifact(s) to an external directory (s3 or local).
    SUCCEEDED:
        The job has finished, including training, evaluation and publishing the
        artifact(s).
    FAILED:
        The job has failed for some reason internally, it can be due to resources
        issues or the code itself.
    STOPPED:
        The job has been stopped by the use locally or in the cloud.
    """

    CREATED = "CREATED"
    STARTING = "STARTING"
    TRAINING = "TRAINING"
    EVALUATING = "EVALUATING"
    PUBLISHING = "PUBLISHING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"

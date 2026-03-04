from pydantic import BaseModel, EmailStr
from typing import List

class QuizSubmitPayload(BaseModel):
    selectedInForm: List [str]
    answersText: list[str] | None = None

class ReportRequestPayload(BaseModel):
    submission_id: int
    email: EmailStr
    consent: bool

class PortraitSection(BaseModel):
    apparence_physique: str
    energie_sommeil: str
    comportement: str
    qualites_defauts: str
    sante_generale: str


class AlimentationSection(BaseModel):
    metabolisme: str
    aliments_conseilles: str
    aliments_a_eviter: str


class ActiviteSection(BaseModel):
    activite_physique_conseillee: str
    regulation_emotionnelle: str
    tips_soutien_emotionnel: str


class AiReport(BaseModel):
    portrait: PortraitSection
    alimentation: AlimentationSection
    activite: ActiviteSection
    reprogrammation_positive: str


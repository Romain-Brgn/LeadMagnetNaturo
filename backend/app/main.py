"""
LeadMagnet Naturo API

FastAPI backend that generates a personalized Hippocratic temperament report.
The report is generated using OpenAI and sent by email as a PDF.

Author: Romain Bourgin
"""

from fastapi import FastAPI, HTTPException, Request
from app.schemas import QuizSubmitPayload, ReportRequestPayload, AiReport
from app.scoring import compute_temperaments
from app.repository import count_report_requests_last_minutes, create_report_request, create_submission
from app.repository import get_submission_by_id
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import date
from app.pdf_utils import generate_pdf_report
import os
import resend
import base64
from openai import OpenAI

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. Initialisation du limiteur
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


BASE_DIR = Path(__file__).resolve().parents[2]
FRONT_DIR = BASE_DIR / "frontend"

app.mount("/assets", StaticFiles(directory=FRONT_DIR), name="assets")

@app.get("/")
def serve_index():
    return FileResponse(FRONT_DIR / "index.html")

@app.post("/quiz/submit")
@limiter.limit("3/minute") 
async def quiz_submit(payload: QuizSubmitPayload, request: Request):
# on a besoin de request pour le limiter
    
    result = compute_temperaments(payload.selectedInForm)
    if result["isValid"] != True:
        raise HTTPException(status_code=400, detail={"message":result["error_message"],"code":result["error_code"]})


    submission_id = create_submission(
        answers=result["answers"],
        scores=result["scores"],
        percentages=result["percentages"],
        top1=",".join(result["top1"]),
        top2=",".join(result["top2"]),
        created_at=date.today(),
        answers_text=payload.answersText
    )

    result["submission_id"] = submission_id

    return result

@app.post("/report/send")
@limiter.limit("1/minute")
async def report_send(payload: ReportRequestPayload, request: Request):
    # Validations de base
    if not payload.consent:
        raise HTTPException(
            status_code=400,
            detail={"message": "Consentement obligatoire.", "code": "CONSENT_REQUIRED"},
        )

    # Vérification du Rate Limit DB
    # On limite à 3 par heure par email 
    count = count_report_requests_last_minutes(payload.email, minutes=60)
    if count >= 3: 
        raise HTTPException(
            status_code=429,
            detail={"message": "Limite de rapports atteinte pour cette heure.", "code": "RATE_LIMIT"},
        )

    submission = get_submission_by_id(payload.submission_id)
    if not submission:
        raise HTTPException(
            status_code=404,
            detail={"message": "Soumission introuvable.", "code": "SUBMISSION_NOT_FOUND"},
        )

    report = None  

    try:
       
            report_request_id = create_report_request(payload.submission_id, payload.email, payload.consent)
            if not report_request_id:
                raise HTTPException(
                    status_code=500,
                    detail={"message": "Erreur lors de la création de la demande de rapport.", "code": "REPORT_REQUEST_FAILED"},
                )
            
            count = count_report_requests_last_minutes(payload.email, minutes=60)
            if count >= 30:
                raise HTTPException(
                status_code=429,
                detail={"message": "Trop de demandes. Réessayez plus tard.", "code": "RATE_LIMIT"},
                )

            client = OpenAI()
            response = client.responses.parse(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "Tu es expert en naturopathie sur les 4 profils hippocratiques "
                            "(sanguin, bilieux, lymphatique, nerveux). "
                            "Tu dois répondre UNIQUEMENT avec un JSON valide conforme au modèle AiReport. "
                            "Aucun texte en dehors du JSON. "
                            "3 phrases minimum et 6 phrases maximum par champ. "
                            "Aucun diagnostic / avis médical / traitement / posologie. "
                            "Ton : humain, professionnel, bienveillant, encourageant."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Données quiz:\n"
                            f"- réponses: {submission['answers_text']}\n"
                            f"- pourcentages: {submission['percentages']}\n"
                            f"- top1: {submission['top1']}\n"
                            f"- top2: {submission['top2']}\n"
                            "Génère le rapport au format AiReport."
                        ),
                    },
                ],
                text_format=AiReport,
            )

            report = response.output_parsed

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))

    if report is None:
        raise HTTPException(status_code=500, detail="Report IA non généré")

    # 4. Sécurisation du PDF avec un nom unique (UUID)
    out_dir = Path(__file__).parent / "generated_reports"
    out_dir.mkdir(exist_ok=True)
    
    # On génère un nom de fichier impossible à deviner : rapport_abc123.pdf
    unique_filename = f"rapport_{uuid.uuid4().hex[:10]}.pdf"
    
    # Adaptation de ta fonction pdf (vérifie si tu peux lui passer le nom)
    pdf_path = generate_pdf_report(submission, payload.email, out_dir, report)

    # 5. Envoi Email
    resend.api_key = os.getenv("RESEND_API_KEY")
    resend.Emails.send({
        "from": "Mon Naturo <info@romain-brgn.work>",
        "to": payload.email,
        "subject": "🌿 Votre bilan de naturopathie",
        "html": "<strong>Voici votre rapport personnalisé en pièce jointe.</strong>",
        "attachments": [{
            "filename": pdf_path.name,
            "content": base64.b64encode(pdf_path.read_bytes()).decode(),
        }],
    })

    return {"ok": True, "message": "Rapport envoyé avec succès."}


# si je met un btn plus tard
@app.get("/report/download/{filename}")
def report_download(filename: str):
    base_dir = Path(__file__).parent / "generated_reports"
    file_path = base_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=filename,
    )  


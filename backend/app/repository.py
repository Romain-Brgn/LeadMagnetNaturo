from datetime import date, datetime, timedelta
import json
from sqlalchemy import text
from app.database import engine

def create_submission(answers: list[str],  scores: dict, percentages: dict,top1 : str, top2: str, created_at: date, answers_text:list[str] | None = None) -> int:
    answers_text = answers_text or []  
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO quiz_submissions_v2 (answers_json, answers_text_json, scores_json, percentages_json, top1, top2, created_at)
                VALUES (:answers_json, :answers_text_json, :scores_json, :percentages_json, :top1, :top2, :created_at)
            """),
            {
                
                "answers_json": json.dumps(answers),
                "answers_text_json": json.dumps(answers_text,ensure_ascii=False),
                "scores_json": json.dumps(scores),
                "percentages_json": json.dumps(percentages),
                "top1": top1,
                "top2": top2,
                "created_at": created_at,
                
            },
        )
        return result.lastrowid

def get_submission_by_id(submission_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM quiz_submissions_v2
                WHERE id = :id
            """),
            {"id": submission_id}
        ).fetchone()

        if not result:
            return None

        
        return {
            "id": result.id,
            "answers": json.loads(result.answers_json),
            "answers_text": json.loads(result.answers_text_json) if result.answers_text_json else [],
            "scores": json.loads(result.scores_json),
            "percentages": json.loads(result.percentages_json),
            "top1": result.top1.split(",") if result.top1 else [],
            "top2": result.top2.split(",") if result.top2 else [],
            "created_at": result.created_at,
        }

def create_report_request(submission_id: int, email: str, isConsent: bool):
    with engine.begin() as conn:
        result =conn.execute(
            text("""
                INSERT INTO report_requests (quiz_submission_id, email, consent, created_at)
                VALUES (:quiz_submission_id, :email, :consent, :created_at)
            """),
            {
                "quiz_submission_id": submission_id,
                "email": email,
                "consent": isConsent,
                "created_at": datetime.now(),
            },
        )
        return int(result.lastrowid)

def count_report_requests_last_minutes(email: str, minutes: int = 60) -> int:
    cutoff = datetime.now() - timedelta(minutes=minutes)
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                SELECT COUNT(*) 
                FROM report_requests
                WHERE email = :email AND created_at >= :cutoff
            """),
            {"email": email, "cutoff": cutoff},
        ).fetchone()
    return int(row[0] or 0)
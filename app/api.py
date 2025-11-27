import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks

from .schemas import CreateJobRequest, Job, JobStatus
from .store import JobStore
from .services.serp_client import SERPClient
from .services.analyzer import SERPAnalyzer
from .services.outline_generator import OutlineGenerator
from .services.article_generator import ArticleGenerator

router = APIRouter()
job_store = JobStore()

serp_client = SERPClient()
analyzer = SERPAnalyzer()
outline_generator = OutlineGenerator()
article_generator = ArticleGenerator()


def _run_pipeline(job_id: str) -> None:
    job = job_store.get(job_id)
    if not job:
        return

    try:
        job_store.update_status(job_id, JobStatus.running)

        # 1) Fetch SERP data
        serp_results = serp_client.fetch_top_results(topic=job.topic, limit=10)

        # 2) Analyze SERP
        analysis = analyzer.analyze(topic=job.topic, serp_results=serp_results)

        # 3) Generate outline
        outline = outline_generator.generate(topic=job.topic, analysis=analysis)

        # 4) Generate article
        article = article_generator.generate_article(
            outline=outline,
            analysis=analysis,
            target_word_count=job.target_word_count,
        )

        # 5) Save article + mark complete
        job_store.save_article(job_id, article)
        job_store.update_status(job_id, JobStatus.completed)

    except Exception as e:  # noqa
        job_store.update_status(job_id, JobStatus.failed, error_message=str(e))


@router.post("/jobs", response_model=Job)
def create_job(payload: CreateJobRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        topic=payload.topic,
        target_word_count=payload.target_word_count,
        language=payload.language,
        status=JobStatus.pending,
    )
    job_store.create(job)

    # Run asynchronously so the API returns quickly
    background_tasks.add_task(_run_pipeline, job_id)

    return job


@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class Language(str, Enum):
    en = "en"
    # extend later if needed


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class SERPResult(BaseModel):
    rank: int
    url: HttpUrl
    title: str
    snippet: str


class SERPAnalysis(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    themes: List[str]
    serp_results: List[SERPResult]


class OutlineSection(BaseModel):
    heading: str
    level: int = Field(..., ge=1, le=3)
    content_points: List[str]


class Outline(BaseModel):
    topic: str
    sections: List[OutlineSection]


class InternalLinkSuggestion(BaseModel):
    anchor_text: str
    target_slug: str  # or URL/path in your CMS


class ExternalReference(BaseModel):
    title: str
    url: HttpUrl
    suggested_position: str  # e.g. "in section: Collaboration Tools"


class FAQItem(BaseModel):
    question: str
    answer: str


class SEOScore(BaseModel):
    overall_score: float
    meets_word_count: bool
    has_primary_in_title: bool
    has_primary_in_intro: bool
    heading_structure_ok: bool


class KeywordAnalysis(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    keyword_density: float  # simplistic overall density


class SEOData(BaseModel):
    title_tag: str
    meta_description: str
    keyword_analysis: KeywordAnalysis
    structured_data: dict
    internal_links: List[InternalLinkSuggestion]
    external_references: List[ExternalReference]
    faq: List[FAQItem]
    quality_score: SEOScore


class Article(BaseModel):
    h1: str
    body_markdown: str
    word_count: int
    seo: SEOData


class CreateJobRequest(BaseModel):
    topic: str
    target_word_count: int = 1500
    language: Language = Language.en


class Job(BaseModel):
    id: str
    topic: str
    target_word_count: int
    language: Language
    status: JobStatus
    error_message: Optional[str] = None
    article: Optional[Article] = None

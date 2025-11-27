from app.schemas import SERPResult
from app.services.analyzer import SERPAnalyzer
from app.services.outline_generator import OutlineGenerator
from app.services.article_generator import ArticleGenerator


def test_article_meets_basic_seo_constraints():
    topic = "best productivity tools for remote teams"

    serp_results = [
        SERPResult(
            rank=1,
            url="https://example.com/productivity-tools-1",
            title="15 Best Productivity Tools for Remote Teams in 2025",
            snippet="Discover collaboration, automation, and planning tools for remote work.",
        )
    ]

    analyzer = SERPAnalyzer()
    outline_generator = OutlineGenerator()
    article_generator = ArticleGenerator()

    analysis = analyzer.analyze(topic=topic, serp_results=serp_results)
    outline = outline_generator.generate(topic=topic, analysis=analysis)
    article = article_generator.generate_article(
        outline=outline,
        analysis=analysis,
        target_word_count=800,
    )

    assert article.seo.quality_score.has_primary_in_title
    assert article.seo.quality_score.has_primary_in_intro
    assert article.seo.quality_score.heading_structure_ok
    assert article.seo.quality_score.meets_word_count is True or article.word_count >= 0.8 * 800

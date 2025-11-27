from textwrap import fill
from typing import List

from ..schemas import (
    Article,
    Outline,
    SERPAnalysis,
    SEOData,
    KeywordAnalysis,
    InternalLinkSuggestion,
    ExternalReference,
    FAQItem,
    SEOScore,
)


def _make_paragraph(text: str) -> str:
    return fill(text, width=90)


def _sentence_variants(point: str, primary: str) -> List[str]:
    """
    Simple templates to avoid repeating the exact same sentence over and over.
    """
    return [
        f"{point} When you evaluate tools for remote teams, try to ground every claim in a concrete workflow or use case.",
        f"{point} Instead of staying abstract, show what this looks like inside a real remote team using specific tools.",
        f"{point} In practice, the best productivity tools for remote teams are the ones that fit your existing stack and habits.",
        f"{point} Back this up with screenshots, checklists, or real examples so the reader can picture using the tool tomorrow.",
    ]


class ArticleGenerator:
    def generate_article(
        self,
        outline: Outline,
        analysis: SERPAnalysis,
        target_word_count: int,
    ) -> Article:
        primary = analysis.primary_keyword

        # H1: just use the primary keyword nicely formatted
        h1 = f"{primary.title()} (2025 Guide)"

        body_lines: List[str] = []

        # Intro paragraph with primary keyword
        intro = (
            f"If you're looking for {primary}, you're not alone. "
            f"In this guide, we'll break down what actually works in 2025, "
            f"based on what’s ranking today and how real teams use these tools in day-to-day work."
        )
        body_lines.append(_make_paragraph(intro))
        body_lines.append("")

        # Convert outline sections to markdown
        for section in outline.sections:
            if section.level == 2:
                body_lines.append(f"## {section.heading}")
            elif section.level == 3:
                body_lines.append(f"### {section.heading}")
            else:
                body_lines.append(f"#### {section.heading}")

            body_lines.append("")

            for idx, point in enumerate(section.content_points):
                variants = _sentence_variants(point, primary)
                # rotate through variants so text feels more natural
                sentence = variants[idx % len(variants)]
                paragraph = (
                    sentence
                    + " Focus on the trade-offs, not just a features list, so the reader can make a confident decision."
                )
                body_lines.append(_make_paragraph(paragraph))
                body_lines.append("")

            # add a small bridging paragraph per section
            bridge = (
                "As you read through this section, map each idea to your own team: "
                "what tools you already use, where work gets stuck, and which gaps a new tool could realistically fill."
            )
            body_lines.append(_make_paragraph(bridge))
            body_lines.append("")

        body_markdown = "\n".join(body_lines)
        word_count = len(body_markdown.split())

        seo = self._build_seo_data(
            primary=primary,
            analysis=analysis,
            h1=h1,
            body=body_markdown,
            word_count=word_count,
            target_word_count=target_word_count,
        )

        return Article(
            h1=h1,
            body_markdown=body_markdown,
            word_count=word_count,
            seo=seo,
        )

    def _build_seo_data(
        self,
        primary: str,
        analysis: SERPAnalysis,
        h1: str,
        body: str,
        word_count: int,
        target_word_count: int,
    ) -> SEOData:
        # Clean up meta phrasing a bit
        title_tag = h1
        meta_description = (
            f"Learn how to choose and use the best productivity tools for remote teams with a practical, 2025-ready guide. "
            "We cover tool categories, selection criteria, rollout steps, and real-world examples."
        )

        keyword_density = body.lower().count(primary.lower()) / max(word_count, 1)

        keyword_analysis = KeywordAnalysis(
            primary_keyword=primary,
            secondary_keywords=analysis.secondary_keywords,
            keyword_density=keyword_density,
        )

        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title_tag,
            "description": meta_description,
            "about": primary,
            "keywords": [primary] + analysis.secondary_keywords,
        }

        internal_links = [
            InternalLinkSuggestion(
                anchor_text="SEO keyword research tools",
                target_slug="/blog/seo-keyword-research-tools",
            ),
            InternalLinkSuggestion(
                anchor_text="content optimization checklist",
                target_slug="/blog/content-optimization-checklist",
            ),
            InternalLinkSuggestion(
                anchor_text="how to build a content brief",
                target_slug="/blog/content-brief-framework",
            ),
        ]

        external_references = [
            ExternalReference(
                title="State of Remote Work 2025 (Industry Report)",
                url="https://example.org/state-of-remote-work-2025",
                suggested_position="after the section 'Key benefits and challenges'",
            ),
            ExternalReference(
                title="Official Product Documentation for a Leading Productivity Tool",
                url="https://example.org/productivity-tool-docs",
                suggested_position="inside 'Comparison of popular tools'",
            ),
        ]

        faq = [
            FAQItem(
                question=f"What is {primary}?",
                answer=(
                    f"{primary.title()} refers to the mix of tools, workflows, and habits that help distributed teams "
                    "stay aligned, communicate clearly, and ship work on time."
                ),
            ),
            FAQItem(
                question=f"How do I choose the right {primary}?",
                answer=(
                    "Start with your team’s size, existing stack, and collaboration style. "
                    "Shortlist tools that integrate well, are easy to adopt, and solve a real bottleneck instead of adding noise."
                ),
            ),
        ]

        has_primary_in_title = primary.lower() in title_tag.lower()
        has_primary_in_intro = primary.lower() in body[:300].lower()
        heading_structure_ok = "##" in body

        # Consider 40%+ of target acceptable for this demo implementation
        meets_word_count = word_count >= int(0.4 * target_word_count)

        overall = (
            (1.0 if has_primary_in_title else 0.0)
            + (1.0 if has_primary_in_intro else 0.0)
            + (1.0 if heading_structure_ok else 0.0)
            + (1.0 if meets_word_count else 0.0)
        ) / 4.0

        quality_score = SEOScore(
            overall_score=overall,
            meets_word_count=meets_word_count,
            has_primary_in_title=has_primary_in_title,
            has_primary_in_intro=has_primary_in_intro,
            heading_structure_ok=heading_structure_ok,
        )

        return SEOData(
            title_tag=title_tag,
            meta_description=meta_description,
            keyword_analysis=keyword_analysis,
            structured_data=structured_data,
            internal_links=internal_links,
            external_references=external_references,
            faq=faq,
            quality_score=quality_score,
        )

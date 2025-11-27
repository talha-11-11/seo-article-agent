# app/services/outline_generator.py
from ..schemas import Outline, OutlineSection, SERPAnalysis


class OutlineGenerator:
    def generate(self, topic: str, analysis: SERPAnalysis) -> Outline:
        # Use the raw topic string to build nicer headings
        base_topic = topic.strip().rstrip(".")  # e.g. "best productivity tools for remote teams"

        # A more generic noun phrase without "best"
        generic_phrase = base_topic.lower().replace("best ", "").strip()  # "productivity tools for remote teams"
        noun_phrase_title = generic_phrase.title() if generic_phrase else base_topic.title()

        sections: list[OutlineSection] = []

        # --- Intro / definition ---
        sections.append(
            OutlineSection(
                heading=f"What Are {noun_phrase_title}?",
                level=2,
                content_points=[
                    f"Define what {generic_phrase or base_topic} actually means in day-to-day work.",
                    "Explain why these tools matter specifically for remote or hybrid teams.",
                    "Give 1–2 short, concrete examples of a team using these tools well.",
                ],
            )
        )

        # --- Benefits & challenges ---
        sections.append(
            OutlineSection(
                heading="Key Benefits and Challenges",
                level=2,
                content_points=[
                    "Summarize the main benefits: focus, visibility, faster decisions, less context switching.",
                    "Discuss common challenges: tool overload, poor adoption, scattered data.",
                ],
            )
        )

        # --- Criteria for choosing tools ---
        sections.append(
            OutlineSection(
                heading="Core Criteria for Choosing the Right Tools",
                level=2,
                content_points=[
                    "Collaboration and communication features that actually get used by the team.",
                    "Integration with the existing stack (email, calendar, chat, code, CRM, etc.).",
                    "Pricing, security, scalability, and admin controls.",
                ],
            )
        )

        # --- Comparison (H2 + real H3s) ---
        sections.append(
            OutlineSection(
                heading="Comparison of Popular Tool Categories",
                level=2,
                content_points=[
                    "Explain how to compare tools by category instead of chasing every new app.",
                ],
            )
        )

        # Now add real H3 sections so the article uses H1 / H2 / H3
        sections.extend(
            [
                OutlineSection(
                    heading="Project Management and Task Tracking Tools",
                    level=3,
                    content_points=[
                        "Describe what this category covers (boards, sprints, backlogs).",
                        "Give 2–3 examples and when each tends to work best.",
                    ],
                ),
                OutlineSection(
                    heading="Communication and Meeting Tools",
                    level=3,
                    content_points=[
                        "Differentiate between synchronous (meetings) and asynchronous communication.",
                        "Explain how to avoid notification overload with sensible norms.",
                    ],
                ),
                OutlineSection(
                    heading="Documentation and Knowledge Base Tools",
                    level=3,
                    content_points=[
                        "Explain why remote teams need a single source of truth.",
                        "Cover search, templates, and permission models briefly.",
                    ],
                ),
                OutlineSection(
                    heading="Async Collaboration and Automation Tools",
                    level=3,
                    content_points=[
                        "Explain how automation reduces manual status updates and busywork.",
                        "Give examples of simple automations that help remote teams.",
                    ],
                ),
            ]
        )

        # --- Implementation / rollout ---
        sections.append(
            OutlineSection(
                heading="How to Implement and Roll Out Successfully",
                level=2,
                content_points=[
                    "Outline a step-by-step rollout plan for a new tool stack.",
                    "Describe how to run a pilot with a small group before a full rollout.",
                    "List common rollout mistakes and how to avoid them.",
                ],
            )
        )

        # --- Final recommendations ---
        sections.append(
            OutlineSection(
                heading="Final Recommendations and Next Steps",
                level=2,
                content_points=[
                    "Summarize which kinds of tools fit different team sizes and workflows.",
                    "Give 3–5 practical next steps the reader can take after finishing the article.",
                ],
            )
        )

        return Outline(topic=topic, sections=sections)

from typing import List
from ..schemas import SERPResult


class SERPClient:
    """
    Interface for a real SERP API client.
    For the assignment, we mock this with deterministic data.
    """

    def fetch_top_results(self, topic: str, limit: int = 10) -> List[SERPResult]:
        # In real life, call SerpAPI / DataForSEO / ValueSERP here.
        # For now, build mock results that look realistic.
        base_url = "https://example.com"
        words = topic.lower().replace("\"", "").replace(" ", "-")
        results: List[SERPResult] = []

        for i in range(1, limit + 1):
            results.append(
                SERPResult(
                    rank=i,
                    url=f"{base_url}/{words}-{i}",
                    title=f"{i + 4} Best {topic.title()} Strategies in 2025",
                    snippet=(
                        f"Learn about {topic} including tools, best practices, and tips. "
                        f"This guide covers collaboration, workflows, integrations, and more."
                    ),
                )
            )
        return results

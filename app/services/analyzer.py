from collections import Counter
from typing import List
import re

from ..schemas import SERPResult, SERPAnalysis


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]{3,}", text.lower())


class SERPAnalyzer:
    def analyze(self, topic: str, serp_results: List[SERPResult]) -> SERPAnalysis:
        all_text = " ".join(r.title + " " + r.snippet for r in serp_results)
        tokens = _tokenize(all_text)
        counts = Counter(tokens)

        # crude heuristic for "secondary keywords"
        common_terms = [w for w, c in counts.most_common(50)
                        if w not in {"best", "tools", "guide", "remote", "team", "teams"}]

        primary_keyword = topic.lower()
        secondary_keywords = common_terms[:10]

        # themes from coarser grouping
        themes = []
        if "collaboration" in tokens:
            themes.append("Collaboration & communication")
        if "automation" in tokens:
            themes.append("Automation & workflows")
        themes.append("Pricing & ROI")
        themes.append("Implementation tips & onboarding")
        themes.append("Pros and cons of different solutions")

        return SERPAnalysis(
            primary_keyword=primary_keyword,
            secondary_keywords=secondary_keywords,
            themes=themes,
            serp_results=serp_results,
        )

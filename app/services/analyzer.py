import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """You are an editor for a technical content creator in the AI and data science space.

Read the article below carefully, then return JSON with exactly these five fields, in this order:

- "story_type": one of exactly these: "announcement", "technical", "explainer", "opinion", "roundup", "quote". An announcement is a new release, model, or product. Technical is a how-to, benchmark, or deep dive. Explainer is a background piece teaching how something works. Opinion is commentary or argument. Roundup is a list post. Quote is a short excerpt post with little original content.

- "specific_detail": one concrete detail from the article — a number, a capability, a limitation, a claim, a result. Something a person who only read the headline would not know. Quote or closely paraphrase it.

- "angle": one thing worth making from this article. It must explicitly use the specific_detail above. Start with a verb: "Test whether...", "Compare X against Y...", "Build a...", "Show what happens when...". It must be something one person could make in a day with a laptop.

Decide "nothing here" based on whether the article actually contains something buildable — not based on the story_type you assigned. Some opinion pieces and roundups still name a specific tool, number, or claim worth testing. If there is genuinely nothing, write "nothing here" rather than inventing something.

Good angles:
- "Load a dataset bigger than your RAM using Datasets streaming and show exactly where it breaks"
- "Run the same prompt through both models and compare what the token costs actually come out to"
Bad angles:
- "A comparative look at dataset management approaches"
- "An overview of GPU efficiency strategies"

The test: could someone start making it today, without more research?

- "key_insight": what this actually means or makes possible. If the article is promotional or says nothing new, say that plainly.

- "summary": 2 sentences on what the article says.

Write like a person talking to another person. No phrases like "revolutionize", "democratize", "game-changing", "transform the landscape", "cutting-edge". If an article is boring, it is fine to say it is boring.

TITLE: {title}
SOURCE: {source}

ARTICLE:
{content}
"""


def analyze_article(title: str, source: str, content: str) -> dict | None:
    try:
        response = client.responses.create(
            model="gpt-4o",
            input=PROMPT.format(
                title=title,
                source=source,
                content=content[:12000],
            ),
            text={"format": {"type": "json_object"}},
        )
        return json.loads(response.output_text)
    except Exception as e:
        print(f"  analysis failed: {type(e).__name__}: {e}")
        return None
    


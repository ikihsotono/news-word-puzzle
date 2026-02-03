import json
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from email.utils import parsedate_to_datetime
from urllib.request import urlopen
import xml.etree.ElementTree as ET

CONFIG_PATH = os.environ.get("NWP_CONFIG", "backend/config.json")
OUTPUT_PATH = os.environ.get("NWP_OUTPUT", "data/puzzles.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def should_run(now, config, last_generated_date):
    local = now.astimezone(ZoneInfo(config["timezone"]))
    if local.hour != config["daily_hour"]:
        return False
    if local.minute > config.get("daily_window_minutes", 20):
        return False
    if last_generated_date == local.date().isoformat():
        return False
    return True


def load_last_generated_date():
    if not os.path.exists(OUTPUT_PATH):
        return None
    try:
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("generated_for_date")
    except Exception:
        return None


def _strip(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _text(node):
    if node is None:
        return ""
    return (node.text or "").strip()


def _find_first(node, names):
    for name in names:
        found = node.find(name)
        if found is not None:
            return found
    return None


def parse_feed_xml(xml_text):
    root = ET.fromstring(xml_text)
    items = []
    tag = _strip(root.tag).lower()

    # RSS 2.0
    if tag == "rss":
        channel = root.find("channel")
        if channel is None:
            return items
        for item in channel.findall("item"):
            title = _text(_find_first(item, ["title"]))
            summary = _text(_find_first(item, ["description"]))
            link = _text(_find_first(item, ["link"]))
            pub = _text(_find_first(item, ["pubDate", "published"]))
            items.append({
                "title": title,
                "summary": summary,
                "url": link,
                "published": pub,
            })
        return items

    # Atom
    if tag == "feed":
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"
        for entry in root.findall(f"{ns}entry"):
            title = _text(_find_first(entry, [f"{ns}title", "title"]))
            summary = _text(_find_first(entry, [f"{ns}summary", f"{ns}content", "summary", "content"]))
            link = ""
            for link_node in entry.findall(f"{ns}link"):
                rel = link_node.attrib.get("rel", "alternate")
                href = link_node.attrib.get("href", "")
                if rel == "alternate" and href:
                    link = href
                    break
                if not link and href:
                    link = href
            pub = _text(_find_first(entry, [f"{ns}updated", f"{ns}published", "updated", "published"]))
            items.append({
                "title": title,
                "summary": summary,
                "url": link,
                "published": pub,
            })
        return items

    return items


def fetch_feed_items(feeds, max_items=30):
    items = []
    for feed in feeds:
        url = feed["url"]
        xml_text = ""
        if url.startswith("file://"):
            path = url.replace("file://", "")
            with open(path, "r", encoding="utf-8") as f:
                xml_text = f.read()
        elif os.path.exists(url):
            with open(url, "r", encoding="utf-8") as f:
                xml_text = f.read()
        else:
            with urlopen(url, timeout=10) as resp:
                xml_text = resp.read().decode("utf-8", errors="ignore")

        parsed_items = parse_feed_xml(xml_text)
        for entry in parsed_items[:max_items]:
            items.append({
                "source": feed["source"],
                "rank_hint": feed.get("rank_hint", ""),
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "url": entry.get("url", ""),
                "published": entry.get("published", ""),
            })
    return items


def score_item(item):
    title = (item.get("title") or "").lower()
    score = 0
    # Prefer breaking/top/market headlines
    keywords = ["breaking", "exclusive", "top", "market", "markets"]
    for kw in keywords:
        if kw in title:
            score += 2
    # Source hints
    rank_hint = (item.get("rank_hint") or "").lower()
    if "top" in rank_hint or "breaking" in rank_hint:
        score += 3
    if any(tag in rank_hint for tag in ["economy", "finance", "business", "investing"]):
        score += 1
    # Prefer newer items
    published = item.get("published", "")
    if published:
        try:
            dt = parsedate_to_datetime(published)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_hours = (datetime.now(tz=timezone.utc) - dt).total_seconds() / 3600
            if age_hours <= 6:
                score += 3
            elif age_hours <= 24:
                score += 2
            elif age_hours <= 72:
                score += 1
        except Exception:
            pass
    return score


def rank_items(items):
    # Sort by score desc, then by published (if present) as a tiebreaker.
    def sort_key(item):
        score = score_item(item)
        published = item.get("published", "")
        return (score, published)

    return sorted(items, key=sort_key, reverse=True)


def generate_puzzles(items, min_puzzles, max_puzzles):
    # TODO: Replace with LLM-based generator.
    # For now, produce placeholder puzzles from titles only.
    puzzles = []
    for item in rank_items(items):
        if len(puzzles) >= max_puzzles:
            break
        title = item["title"].strip()
        if not title:
            continue
        # Placeholder: mask the last word
        words = title.split()
        if len(words) < 3:
            continue
        answer = words[-1].strip(".,:;!?")
        if not answer:
            continue
        question = " ".join(words[:-1] + ["_____"])
        puzzles.append({
            "article": item,
            "questionText": question,
            "answer": answer,
            "hint": "noun",
            "difficulty": "medium",
        })
    if len(puzzles) < min_puzzles:
        # If we cannot generate enough, return what we have.
        return puzzles
    return puzzles[:max_puzzles]


def main():
    now = datetime.now(tz=ZoneInfo("UTC"))
    config = load_config()
    last_generated_date = load_last_generated_date()

    force = os.environ.get("NWP_FORCE", "") == "1"
    if not force and not should_run(now, config, last_generated_date):
        return

    items = fetch_feed_items(config["feeds"])
    puzzles = generate_puzzles(items, config["min_puzzles"], config["max_puzzles"])

    output = {
        "generated_at": now.isoformat(),
        "generated_for_date": now.astimezone(ZoneInfo(config["timezone"]))
            .date().isoformat(),
        "puzzles": puzzles,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

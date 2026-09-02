"""Topic-wise resources: videos, books, tutoring hints."""

from __future__ import annotations

RESOURCES = [
    {"topic_id": "m-quad", "title": "Khan Academy — Quadratic equations", "kind": "youtube", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratic-functions-equations", "rating": 4.8, "note": "Free. Start here if yesterday's quadratic drill was incomplete."},
    {"topic_id": "m-quad", "title": "NCERT Exemplar — Quadratics", "kind": "book", "url": None, "rating": 4.6, "note": "Word problems that match board style."},
    {"topic_id": "m-quad", "title": "Private tutor (already enrolled)", "kind": "tuition", "url": None, "rating": 4.5, "note": "Ask the maths tutor to redo nature-of-roots + speed-distance word problems this week."},
    {"topic_id": "m-trig", "title": "Khan Academy — Trigonometric ratios", "kind": "youtube", "url": "https://www.khanacademy.org/math/geometry/hs-geo-trig", "rating": 4.9, "note": "Identities first, then heights & distances."},
    {"topic_id": "m-trig", "title": "NCERT Class 10 Maths Ch 8 examples", "kind": "book", "url": None, "rating": 4.7, "note": "Do every example before exercise 8.2."},
    {"topic_id": "m-ap", "title": "Vedantu — Arithmetic progressions (high rated)", "kind": "youtube", "url": "https://www.youtube.com/results?search_query=class+10+arithmetic+progressions+ncert", "rating": 4.4, "note": "Good for sum-of-n-terms shortcuts."},
    {"topic_id": "m-linear", "title": "Khan Academy — Systems of equations", "kind": "youtube", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:systems-of-equations", "rating": 4.7, "note": "Graphical vs algebraic consistency."},
    {"topic_id": "s-life", "title": "Khan Academy — Life processes", "kind": "youtube", "url": "https://www.khanacademy.org/science/biology", "rating": 4.8, "note": "Nutrition + respiration diagrams are high-yield."},
    {"topic_id": "s-life", "title": "NCERT diagrams: human heart & nephron", "kind": "book", "url": None, "rating": 4.9, "note": "Redraw from memory. School missed this if you took leave."},
    {"topic_id": "s-elec", "title": "Physics Wallah — Electricity Class 10", "kind": "youtube", "url": "https://www.youtube.com/results?search_query=class+10+electricity+ncert", "rating": 4.6, "note": "Circuit numericals with series-parallel mix."},
    {"topic_id": "s-light", "title": "Khan Academy — Light reflection", "kind": "youtube", "url": "https://www.khanacademy.org/science/physics/geometric-optics", "rating": 4.7, "note": "Sign convention is where most marks leak."},
    {"topic_id": "s-carbon", "title": "NCERT Ch 4 Carbon compounds", "kind": "book", "url": None, "rating": 4.5, "note": "Homologous series table + soap vs detergent."},
    {"topic_id": "h-nation-in", "title": "Crash Course / NCERT read-aloud Nationalism in India", "kind": "youtube", "url": "https://www.youtube.com/results?search_query=nationalism+in+india+class+10", "rating": 4.5, "note": "Timeline: 1919–1930 is almost certain in boards."},
    {"topic_id": "p-power", "title": "NCERT Democratic Politics II — Power Sharing", "kind": "book", "url": None, "rating": 4.8, "note": "Belgium vs Sri Lanka comparison is a 3-mark staple."},
    {"topic_id": "e-dev", "title": "Khan Academy — GDP and development", "kind": "youtube", "url": "https://www.khanacademy.org/economics-finance-domain", "rating": 4.3, "note": "Pair with HDI table from NCERT."},
    {"topic_id": "e-sectors", "title": "NCERT Economics Ch 2", "kind": "book", "url": None, "rating": 4.6, "note": "Organised vs unorganised + NREGA link."},
    {"topic_id": "m-trigapp", "title": "Heights and distances — worked PYQs", "kind": "youtube", "url": "https://www.youtube.com/results?search_query=class+10+heights+and+distances+pyq", "rating": 4.5, "note": "Two-angle problems (30°/60°) appear almost every year."},
    {"topic_id": "s-acids", "title": "Acids bases salts — pH and salts", "kind": "youtube", "url": "https://www.youtube.com/results?search_query=class+10+acids+bases+salts", "rating": 4.4, "note": "Plaster of Paris and washing soda uses are easy marks."},
]


def resources_for_topic(topic_id: str) -> list[dict]:
    return [r for r in RESOURCES if r["topic_id"] == topic_id]

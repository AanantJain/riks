"""CBSE Class 10 curriculum: topics, marking weights, exam probability."""

from __future__ import annotations

SUBJECTS = [
    {
        "id": "maths",
        "name": "Mathematics",
        "code": "041",
        "theory_marks": 80,
        "internal_marks": 20,
        "color": "#2F5D50",
    },
    {
        "id": "science",
        "name": "Science",
        "code": "086",
        "theory_marks": 80,
        "internal_marks": 20,
        "color": "#3D6B8A",
    },
    {
        "id": "sst",
        "name": "Social Science",
        "code": "087",
        "theory_marks": 80,
        "internal_marks": 20,
        "color": "#8A4B2F",
    },
]

# marks_weight ≈ expected board marks. probability = how often a similar
# question appears in the last 10 years / sample papers (0–1).
TOPICS = [
    # Mathematics
    {"id": "m-real", "subject_id": "maths", "chapter": "Real Numbers", "name": "Euclid's algorithm & fundamental theorem", "marks_weight": 4, "probability": 0.85, "ncert_priority": "must", "unit": "Number Systems"},
    {"id": "m-poly", "subject_id": "maths", "chapter": "Polynomials", "name": "Zeros of a polynomial & division algorithm", "marks_weight": 4, "probability": 0.80, "ncert_priority": "must", "unit": "Algebra"},
    {"id": "m-linear", "subject_id": "maths", "chapter": "Pair of Linear Equations", "name": "Graphical & algebraic methods", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "Algebra"},
    {"id": "m-quad", "subject_id": "maths", "chapter": "Quadratic Equations", "name": "Nature of roots & applications", "marks_weight": 6, "probability": 0.95, "ncert_priority": "must", "unit": "Algebra"},
    {"id": "m-ap", "subject_id": "maths", "chapter": "Arithmetic Progressions", "name": "nth term and sum of n terms", "marks_weight": 6, "probability": 0.92, "ncert_priority": "must", "unit": "Algebra"},
    {"id": "m-tri", "subject_id": "maths", "chapter": "Triangles", "name": "Similarity criteria & Pythagoras", "marks_weight": 8, "probability": 0.88, "ncert_priority": "must", "unit": "Geometry"},
    {"id": "m-coord", "subject_id": "maths", "chapter": "Coordinate Geometry", "name": "Distance, section formula, area", "marks_weight": 6, "probability": 0.86, "ncert_priority": "must", "unit": "Coordinate Geometry"},
    {"id": "m-trig", "subject_id": "maths", "chapter": "Introduction to Trigonometry", "name": "Ratios, identities, complementary angles", "marks_weight": 8, "probability": 0.97, "ncert_priority": "must", "unit": "Trigonometry"},
    {"id": "m-trigapp", "subject_id": "maths", "chapter": "Applications of Trigonometry", "name": "Heights and distances", "marks_weight": 4, "probability": 0.90, "ncert_priority": "must", "unit": "Trigonometry"},
    {"id": "m-circle", "subject_id": "maths", "chapter": "Circles", "name": "Tangent properties", "marks_weight": 6, "probability": 0.84, "ncert_priority": "must", "unit": "Geometry"},
    {"id": "m-areas", "subject_id": "maths", "chapter": "Areas Related to Circles", "name": "Sector, segment, combinations", "marks_weight": 4, "probability": 0.72, "ncert_priority": "should", "unit": "Mensuration"},
    {"id": "m-vol", "subject_id": "maths", "chapter": "Surface Areas and Volumes", "name": "Combination of solids", "marks_weight": 6, "probability": 0.82, "ncert_priority": "must", "unit": "Mensuration"},
    {"id": "m-stats", "subject_id": "maths", "chapter": "Statistics", "name": "Mean, median, mode of grouped data", "marks_weight": 6, "probability": 0.88, "ncert_priority": "must", "unit": "Statistics & Probability"},
    {"id": "m-prob", "subject_id": "maths", "chapter": "Probability", "name": "Classical probability", "marks_weight": 4, "probability": 0.90, "ncert_priority": "must", "unit": "Statistics & Probability"},
    # Science
    {"id": "s-chemrxn", "subject_id": "science", "chapter": "Chemical Reactions and Equations", "name": "Types of reactions & balancing", "marks_weight": 6, "probability": 0.88, "ncert_priority": "must", "unit": "Chemical Substances"},
    {"id": "s-acids", "subject_id": "science", "chapter": "Acids, Bases and Salts", "name": "pH, salts, indicators", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "Chemical Substances"},
    {"id": "s-metals", "subject_id": "science", "chapter": "Metals and Non-metals", "name": "Reactivity, extraction, corrosion", "marks_weight": 6, "probability": 0.78, "ncert_priority": "must", "unit": "Chemical Substances"},
    {"id": "s-carbon", "subject_id": "science", "chapter": "Carbon and its Compounds", "name": "Bonding, homologous series, soaps", "marks_weight": 8, "probability": 0.92, "ncert_priority": "must", "unit": "Chemical Substances"},
    {"id": "s-life", "subject_id": "science", "chapter": "Life Processes", "name": "Nutrition, respiration, transport, excretion", "marks_weight": 10, "probability": 0.96, "ncert_priority": "must", "unit": "World of Living"},
    {"id": "s-control", "subject_id": "science", "chapter": "Control and Coordination", "name": "Nervous system & hormones", "marks_weight": 6, "probability": 0.80, "ncert_priority": "must", "unit": "World of Living"},
    {"id": "s-repro", "subject_id": "science", "chapter": "How do Organisms Reproduce", "name": "Asexual & sexual reproduction", "marks_weight": 6, "probability": 0.86, "ncert_priority": "must", "unit": "World of Living"},
    {"id": "s-heredity", "subject_id": "science", "chapter": "Heredity", "name": "Mendel, sex determination", "marks_weight": 4, "probability": 0.84, "ncert_priority": "must", "unit": "World of Living"},
    {"id": "s-light", "subject_id": "science", "chapter": "Light — Reflection and Refraction", "name": "Mirrors, lenses, power", "marks_weight": 8, "probability": 0.94, "ncert_priority": "must", "unit": "Natural Phenomena"},
    {"id": "s-eye", "subject_id": "science", "chapter": "The Human Eye and Colourful World", "name": "Defects, dispersion, scattering", "marks_weight": 4, "probability": 0.82, "ncert_priority": "should", "unit": "Natural Phenomena"},
    {"id": "s-elec", "subject_id": "science", "chapter": "Electricity", "name": "Ohm's law, circuits, heating effect", "marks_weight": 8, "probability": 0.95, "ncert_priority": "must", "unit": "Effects of Current"},
    {"id": "s-mag", "subject_id": "science", "chapter": "Magnetic Effects of Electric Current", "name": "Field, motor, electromagnetic induction", "marks_weight": 6, "probability": 0.80, "ncert_priority": "must", "unit": "Effects of Current"},
    {"id": "s-env", "subject_id": "science", "chapter": "Our Environment", "name": "Food chains, ozone, waste", "marks_weight": 2, "probability": 0.70, "ncert_priority": "optional", "unit": "Natural Resources"},
    # Social Science
    {"id": "h-nation-eu", "subject_id": "sst", "chapter": "The Rise of Nationalism in Europe", "name": "French Revolution to nation-states", "marks_weight": 5, "probability": 0.75, "ncert_priority": "should", "unit": "History"},
    {"id": "h-nation-in", "subject_id": "sst", "chapter": "Nationalism in India", "name": "Non-cooperation to Civil Disobedience", "marks_weight": 8, "probability": 0.96, "ncert_priority": "must", "unit": "History"},
    {"id": "h-global", "subject_id": "sst", "chapter": "The Making of a Global World", "name": "Trade, colonisation, Bretton Woods", "marks_weight": 4, "probability": 0.68, "ncert_priority": "should", "unit": "History"},
    {"id": "h-print", "subject_id": "sst", "chapter": "Print Culture and the Modern World", "name": "Print revolution & public debate", "marks_weight": 3, "probability": 0.55, "ncert_priority": "optional", "unit": "History"},
    {"id": "g-res", "subject_id": "sst", "chapter": "Resources and Development", "name": "Resource planning & soil", "marks_weight": 5, "probability": 0.82, "ncert_priority": "must", "unit": "Geography"},
    {"id": "g-agri", "subject_id": "sst", "chapter": "Agriculture", "name": "Cropping patterns & types", "marks_weight": 5, "probability": 0.80, "ncert_priority": "must", "unit": "Geography"},
    {"id": "g-min", "subject_id": "sst", "chapter": "Minerals and Energy Resources", "name": "Distribution & conservation", "marks_weight": 4, "probability": 0.70, "ncert_priority": "should", "unit": "Geography"},
    {"id": "g-mfg", "subject_id": "sst", "chapter": "Manufacturing Industries", "name": "Types, location, pollution", "marks_weight": 4, "probability": 0.65, "ncert_priority": "should", "unit": "Geography"},
    {"id": "g-lifeline", "subject_id": "sst", "chapter": "Lifelines of National Economy", "name": "Transport, communication, trade", "marks_weight": 4, "probability": 0.72, "ncert_priority": "should", "unit": "Geography"},
    {"id": "p-power", "subject_id": "sst", "chapter": "Power Sharing", "name": "Belgium, Sri Lanka, forms of sharing", "marks_weight": 5, "probability": 0.90, "ncert_priority": "must", "unit": "Political Science"},
    {"id": "p-fed", "subject_id": "sst", "chapter": "Federalism", "name": "Features & India as a federation", "marks_weight": 5, "probability": 0.86, "ncert_priority": "must", "unit": "Political Science"},
    {"id": "p-gender", "subject_id": "sst", "chapter": "Gender, Religion and Caste", "name": "Social divisions in politics", "marks_weight": 4, "probability": 0.74, "ncert_priority": "should", "unit": "Political Science"},
    {"id": "p-parties", "subject_id": "sst", "chapter": "Political Parties", "name": "Functions, challenges, national parties", "marks_weight": 4, "probability": 0.78, "ncert_priority": "must", "unit": "Political Science"},
    {"id": "p-out", "subject_id": "sst", "chapter": "Outcomes of Democracy", "name": "Accountability, dignity, development", "marks_weight": 3, "probability": 0.70, "ncert_priority": "should", "unit": "Political Science"},
    {"id": "e-dev", "subject_id": "sst", "chapter": "Development", "name": "National income, HDI, sustainability", "marks_weight": 5, "probability": 0.88, "ncert_priority": "must", "unit": "Economics"},
    {"id": "e-sectors", "subject_id": "sst", "chapter": "Sectors of the Indian Economy", "name": "Primary, secondary, tertiary; organised", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "Economics"},
    {"id": "e-money", "subject_id": "sst", "chapter": "Money and Credit", "name": "Formal vs informal credit", "marks_weight": 5, "probability": 0.84, "ncert_priority": "must", "unit": "Economics"},
    {"id": "e-global", "subject_id": "sst", "chapter": "Globalisation and the Indian Economy", "name": "MNCs, WTO, impact", "marks_weight": 4, "probability": 0.76, "ncert_priority": "should", "unit": "Economics"},
    {"id": "e-consumer", "subject_id": "sst", "chapter": "Consumer Rights", "name": "COPRA and consumer awareness", "marks_weight": 2, "probability": 0.50, "ncert_priority": "optional", "unit": "Economics"},
]

TARGETS = {
    "pass": {"label": "Pass comfortably", "percent": 40, "blurb": "Clear every subject with a buffer."},
    "first_division": {"label": "First division (60%)", "percent": 60, "blurb": "A strong, respectable board result."},
    "distinction": {"label": "Distinction (75%)", "percent": 75, "blurb": "Competitive for good schools and streams."},
    "topper": {"label": "Topper band (90%+)", "percent": 90, "blurb": "Leave almost no high-yield topic behind."},
}


def subject_by_id(subject_id: str) -> dict:
    return next(s for s in SUBJECTS if s["id"] == subject_id)


def topic_by_id(topic_id: str) -> dict:
    return next(t for t in TOPICS if t["id"] == topic_id)


def topics_for_subject(subject_id: str) -> list[dict]:
    return [t for t in TOPICS if t["subject_id"] == subject_id]

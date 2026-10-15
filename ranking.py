"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    spots = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            spots.append(row)
    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    
    score  = 0.0
    reasons = []

    # Noise weighs most because a too-loud spot defeats the purpose.
    noise = spot["noise_level"]
    if NOISE_ORDER[noise] <= NOISE_ORDER[profile["max_noise"]]:
        score += 2.0
        reasons.append(f"{noise} is quiet enough")
    else:
        reasons.append(f"{noise} is too loud")

    distance = spot["distance_miles"]
    if distance <= profile["max_distance"]:
        score += 1.5
        reasons.append(f"{distance} mi is close enough")
    else:
        reasons.append(f"{distance} mi is too far")

    seats = spot["seats_available"]
    if seats >= profile["min_seats"]:
        score += 1.0
        reasons.append(f"{seats} seats is enough")
    else:
        reasons.append(f"only {seats} seats")

    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    scored = []
    for spot in spots:
        score, reasons = score_study_spot(profile, spot)
        scored.append((spot, score, reasons))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    for rank, (spot, score, reasons) in enumerate(ranked, start=1):
        print(f"{rank}. {spot['name']} -- Score: {score:.1f} -- Because: {', '.join(reasons)}")


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)

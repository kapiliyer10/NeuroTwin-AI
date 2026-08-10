def evidence_references(purpose: str = "concussion") -> list[dict[str, str]]:
    if purpose == "mental_wellbeing":
        return [
            {
                "title": "Mental health: strengthening our response",
                "publisher": "World Health Organization",
                "url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
                "reviewed": "2026-08-10",
            },
            {
                "title": "Guidelines on mental health at work",
                "publisher": "World Health Organization",
                "url": "https://www.who.int/publications/i/item/9789240053052",
                "reviewed": "2026-08-10",
            },
        ]
    return [
        {
            "title": "Consensus statement on concussion in sport: Amsterdam 2022",
            "publisher": "British Journal of Sports Medicine",
            "url": "https://bjsm.bmj.com/content/57/11/695",
            "reviewed": "2026-08-09",
        },
        {
            "title": "Return-to-Activity / Work / School Considerations",
            "publisher": "Living Concussion Guidelines",
            "url": "https://concussionsontario.org/concussion/guideline-section/return-to-activity_work_school_considerations",
            "reviewed": "2026-08-09",
        },
        {
            "title": "Managing Return to Activities",
            "publisher": "CDC HEADS UP",
            "url": "https://www.cdc.gov/heads-up/hcp/clinical-guidance/index.html",
            "reviewed": "2026-08-09",
        },
    ]

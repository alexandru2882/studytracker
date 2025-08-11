import argparse

from .logic import add_session, list_sessions, total_minutes


def main() -> None:
    parser = argparse.ArgumentParser(prog="studytracker", description="Track study sessions")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a study session")
    p_add.add_argument("topic", type=str, help="What you studied")
    p_add.add_argument("minutes", type=int, help="Minutes spent (positive integer)")
    p_add.add_argument("--date", type=str, default=None, help="YYYY-MM-DD (default: today)")

    sub.add_parser("list", help="List sessions")

    p_report = sub.add_parser("report", help="Total minutes (optionally for a topic)")
    p_report.add_argument("--topic", type=str, default=None, help="Filter by topic")

    args = parser.parse_args()

    if args.cmd == "add":
        s = add_session(args.topic, args.minutes, args.date)
        print(f"Added: {s.topic} for {s.minutes} min on {s.date}")
    elif args.cmd == "list":
        items = list_sessions()
        if not items:
            print("No sessions yet.")
            return
        for i, s in enumerate(items, start=1):
            print(f"{i}. {s.date} — {s.topic}: {s.minutes} min")
    elif args.cmd == "report":
        total = total_minutes(args.topic)
        if args.topic:
            print(f"Total for '{args.topic}': {total} min")
        else:
            print(f"Total minutes: {total}")

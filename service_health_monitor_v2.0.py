def save_report(logs: dict) -> None:
    filename = "report.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("--- LOG REPORT ---\n")
        for endpoint, data in logs.items():
            avg = data["total_ms"] / data["calls"]
            file.write(f"{endpoint} | calls: {data['calls']} | avg: {avg:.0f}ms | errors: {data['errors']}\n")
        file.write("-" * 45)

def parse_log(line: str) -> dict | None:
    line = line.split()
    try:
        parse = {
            "endpoint": line[0], "status": int(line[1]), "ms": int(line[2].strip("ms")),
        }
    except (IndexError, ValueError):
        print("Error: invalid log")
        return None
    return parse

def update_stats(stats: dict, input_log: dict) -> None:
    endpoint = input_log["endpoint"]

    if endpoint not in stats:
        stats[endpoint] = {
            "total_ms": 0,
            "calls": 0,
            "errors": 0,
            "status_code": set()
        }

    endpoint_data = stats[endpoint]
    endpoint_data["total_ms"] += input_log["ms"]
    endpoint_data["calls"] += 1
    endpoint_data["status_code"].add(input_log["status"])

    if input_log["status"] >= 500:
        endpoint_data["errors"] += 1

def main():
    dict_log = {}

    while True:
        user_input = input("Enter a log line ('name - code - latency', ex: /api/v1 300 150ms)"
                           "\nor 'stop' to stop:\n").strip()
        if user_input.lower() == "stop":
            save_report(dict_log)
            print(f"Report saved to report.txt!")
            break

        log = parse_log(user_input)

        if log is None:
            continue

        update_stats(dict_log, log)

        endpoint = log["endpoint"]

        print("="*30)
        print(f"'{endpoint}'")
        for key, value in dict_log[endpoint].items():
            print(f"-{key}: {value}")
        print("=" * 30)


if __name__ == "__main__":
    main()


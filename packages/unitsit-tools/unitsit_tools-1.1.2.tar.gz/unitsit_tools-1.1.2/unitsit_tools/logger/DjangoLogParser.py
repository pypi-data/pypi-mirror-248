import re
from datetime import datetime
from typing import NamedTuple, List


class DjangoLogEntry(NamedTuple):
    """
    Represents a log entry with timestamp, IP address, log level, view name,
    line number, HTTP method, route, status code, and response size.
    """

    timestamp: datetime
    ip: str
    level: str
    view: str
    lineno: int
    method: str
    route: str
    status_code: str
    response_size: str

    def to_json(self):
        """
        Convert the log entry to a JSON-formatted string.

        :return: JSON-formatted string representing the log entry.
        :rtype: str
        """
        import json

        return json.dumps(
            {
                "timestamp": self.timestamp.isoformat(),
                "ip": self.ip,
                "level": self.level,
                "view": self.view,
                "lineno": self.lineno,
                "method": self.method,
                "route": self.route,
                "status_code": self.status_code,
                "response_size": self.response_size,
            }
        )


class DjangoLogParser:
    """
    Parses Django log entries with a specified format and extracts log information.
    """

    log_format = re.compile(
        r"\[(?P<timestamp>.*?)] "
        r"(?P<ip>[\d.]+) "
        r"(?P<level>\w+) "
        r"\[(?P<view>.*?):(?P<lineno>\d+)] "
        r'"(?P<method>[A-Z]+) (?P<route>.*?) HTTP/[\d.]+" '
        r"(?P<status_code>\d+) "
        r"(?P<response_size>\d+)"
    )

    def parse_log_line(self, log_line: str) -> DjangoLogEntry:
        """
        Parses a single log line and returns a DjangoLogEntry if successful.

        :param log_line: Log line to be parsed.
        :type log_line: str
        :return: Parsed DjangoLogEntry or UNPARSED entry.
        :rtype: DjangoLogEntry
        """
        match = self.log_format.match(log_line)
        if match:
            groups = match.groupdict()
            timestamp_str = groups["timestamp"]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            return DjangoLogEntry(
                timestamp=timestamp,
                ip=groups["ip"],
                level=groups["level"],
                view=groups["view"],
                lineno=int(groups["lineno"]),
                method=groups["method"],
                route=groups["route"],
                status_code=groups["status_code"],
                response_size=groups["response_size"],
            )
        else:
            return DjangoLogEntry(
                timestamp=datetime.now(),
                ip="",
                level="UNPARSED",
                view="",
                lineno=0,
                method="",
                route=log_line,
                status_code="",
                response_size="",
            )

    def parse_log_file(self, log_file_path: str) -> List[DjangoLogEntry]:
        """
        Parses a log file and returns a list of DjangoLogEntry objects.

        :param log_file_path: Path to the log file.
        :type log_file_path: str
        :return: List of DjangoLogEntry objects.
        :rtype: List[DjangoLogEntry]
        """
        with open(log_file_path, "r", encoding="utf-8") as file:
            return [
                entry for line in file if (entry := self.parse_log_line(line.strip()))
            ]

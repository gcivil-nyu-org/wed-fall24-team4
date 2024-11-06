from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusFreqTable:
    count: int = 0
    latest_timestamp: datetime = datetime.min


@dataclass
class ReportStatusFreqTable:
    active: StatusFreqTable
    broken: StatusFreqTable
    maintenance: StatusFreqTable

    def get_top_status(self) -> str:
        tuple_set = [
            (self.active.count, self.active.latest_timestamp, "active"),
            (self.broken.count, self.broken.latest_timestamp, "broken"),
            (self.maintenance.count, self.maintenance.latest_timestamp, "maintenance"),
        ]
        return sorted(tuple_set, reverse=True)[0]

from typing import Optional

from rich.text import Text
from rich import filesize
from rich.progress import (ProgressColumn, Task)

class SpeedColumn(ProgressColumn):
    @classmethod
    def render_speed(cls, speed: Optional[float]) -> Text:
        if speed is None:
            return Text("-- it/s", style="progress.percentage")
        unit, suffix = filesize.pick_unit_and_suffix(
            int(speed),
            ["", "×10³", "×10⁶", "×10⁹", "×10¹²"],
            1000,
        )
        data_speed = speed / unit
        return Text(f"{data_speed:.1f}{suffix} it/s", style="progress.percentage")

    def render(self, task: "Task") -> Text:
        return self.render_speed(task.finished_speed or task.speed)



class QpmColumn(ProgressColumn):
    def render(self, task: Task) -> str:
        speed = task.speed
        qpm = "N/A"
        if speed:
            qpm = str(int(speed * 60))
        return f"QPM: {qpm}"
    

col_map = {
    "speed_col": SpeedColumn(),
    "qpm_col": QpmColumn()
}
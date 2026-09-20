import re
import sys
from dataclasses import dataclass
from datetime import timedelta, datetime
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint

console = Console()

# --- Constantes y Patrones ---
TIME_PATTERN = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")


@dataclass
class Subtitle:
    index: int
    start: timedelta
    end: timedelta
    content: List[str]

    @property
    def start_str(self) -> str:
        return self._timedelta_to_srt(self.start)

    @property
    def end_str(self) -> str:
        return self._timedelta_to_srt(self.end)

    @staticmethod
    def _timedelta_to_srt(td: timedelta) -> str:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = int(td.microseconds / 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def __str__(self):
        text = "\n".join(self.content)
        return f"{self.index}\n{self.start_str} --> {self.end_str}\n{text}\n"


class SRTManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.subtitles: List[Subtitle] = []
        self.load()

    def parse_time(self, time_str: str) -> timedelta:
        """Convierte string SRT '00:00:06,519' a timedelta."""
        match = TIME_PATTERN.match(time_str.strip())
        if not match:
            raise ValueError(f"Formato de tiempo inválido: {time_str}")
        h, m, s, ms = map(int, match.groups())
        return timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)

    def load(self):
        """Carga y parsea el archivo SRT."""
        if not self.file_path.exists():
            console.print(
                f"[bold red]Error:[/bold red] El archivo {self.file_path} no existe."
            )
            sys.exit(1)

        try:
            with open(self.file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback para encoding latin-1 si utf-8 falla
            with open(self.file_path, "r", encoding="latin-1") as f:
                content = f.read()

        # Separar por bloques de doble salto de línea
        blocks = re.split(r"\n\s*\n", content.strip())

        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                try:
                    idx = int(lines[0].strip())
                    times = lines[1].strip().split(" --> ")
                    start = self.parse_time(times[0])
                    end = self.parse_time(times[1])
                    text = lines[2:]
                    self.subtitles.append(Subtitle(idx, start, end, text))
                except (ValueError, IndexError):
                    continue  # Saltar bloques corruptos

        console.print(
            f"[green]✔[/green] Cargadas [bold]{len(self.subtitles)}[/bold] líneas de subtítulos."
        )

    def save(self, output_path: Optional[str] = None):
        """Guarda los cambios en el archivo."""
        path = output_path if output_path else self.file_path
        with open(path, "w", encoding="utf-8") as f:
            for sub in self.subtitles:
                f.write(str(sub) + "\n")
        console.print(
            f"[bold green]Archivo guardado exitosamente en: {path}[/bold green]"
        )

    def get_subtitle(self, index: int) -> Optional[Subtitle]:
        # Búsqueda optimizada (asumiendo orden, pero seguro con filter)
        for sub in self.subtitles:
            if sub.index == index:
                return sub
        return None

    # --- Operación 1: Borrar y Renumerar ---
    def delete_subtitle(self, index: int):
        target = self.get_subtitle(index)
        if not target:
            console.print("[red]No se encontró ese índice.[/red]")
            return

        self.subtitles.remove(target)

        # Renumerar
        for i, sub in enumerate(self.subtitles, 1):
            sub.index = i

        console.print(f"[yellow]Línea {index} eliminada. Índices reajustados.[/yellow]")

    # --- Operación 2: Ajustar Texto ---
    def edit_subtitle(self, index: int, new_text: str):
        target = self.get_subtitle(index)
        if not target:
            console.print("[red]No se encontró ese índice.[/red]")
            return

        # Convertir input de una línea a lista si tiene saltos de línea literales
        target.content = new_text.split("\\n")
        console.print(f"[green]Texto de la línea {index} actualizado.[/green]")

    # --- Operación 3: Sincronizar ---
    def sync_subtitles(self, ref_index: int, actual_time_str: str):
        target = self.get_subtitle(ref_index)
        if not target:
            console.print("[red]No se encontró el índice de referencia.[/red]")
            return

        try:
            target_time = self.parse_time(actual_time_str)
        except ValueError:
            console.print("[red]Formato de tiempo inválido. Use HH:MM:SS,mmm[/red]")
            return

        # Calcular el desplazamiento (delta)
        # Delta = Tiempo Real - Tiempo que tiene el subtítulo actualmente
        delta = target_time - target.start

        direction = "adelante" if delta.total_seconds() > 0 else "atrás"
        console.print(
            f"[blue]Aplicando offset de {delta} hacia {direction} a todas las líneas...[/blue]"
        )

        for sub in self.subtitles:
            sub.start += delta
            sub.end += delta

            # Evitar tiempos negativos
            if sub.start.total_seconds() < 0:
                sub.start = timedelta(0)
            if sub.end.total_seconds() < 0:
                sub.end = timedelta(0)


# --- CLI Main ---
def main():
    console.print(
        Panel.fit(
            "[bold magenta]SRT WIZARD 3000[/bold magenta]\nExperto en Python CLI",
            border_style="magenta",
        )
    )

    file_path = Prompt.ask("📂 Introduce la ruta del archivo .srt", default="video.srt")
    manager = SRTManager(file_path)

    while True:
        table = Table(
            title="Menú de Operaciones", show_header=True, header_style="bold cyan"
        )
        table.add_column("Opción", style="dim", width=12)
        table.add_column("Descripción")

        table.add_row("1", "Borrar línea de diálogo (Renumeración auto)")
        table.add_row("2", "Corregir texto/traducción")
        table.add_row("3", "Sincronizar (Shift global)")
        table.add_row("4", "Guardar y Salir")
        table.add_row("0", "Salir sin guardar")

        console.print(table)

        opcion = IntPrompt.ask(
            "Selecciona una opción", choices=["0", "1", "2", "3", "4"]
        )

        match opcion:
            case 1:
                idx = IntPrompt.ask(
                    "¿Qué número de diálogo quieres [bold red]borrar[/bold red]?"
                )
                manager.delete_subtitle(idx)

            case 2:
                idx = IntPrompt.ask(
                    "¿Qué número de diálogo quieres [bold yellow]editar[/bold yellow]?"
                )
                sub = manager.get_subtitle(idx)
                if sub:
                    console.print(
                        f"[dim]Texto actual:[/dim] [italic]{' '.join(sub.content)}[/italic]"
                    )
                    new_txt = Prompt.ask("Nuevo texto (usa \\n para saltos de línea)")
                    manager.edit_subtitle(idx, new_txt)

            case 3:
                idx = IntPrompt.ask(
                    "Número de diálogo de [bold blue]referencia[/bold blue] (el que escuchas)"
                )
                sub = manager.get_subtitle(idx)
                if sub:
                    console.print(
                        f"El diálogo [bold]{idx}[/bold] empieza actualmente en: [bold]{sub.start_str}[/bold]"
                    )
                    real_time = Prompt.ask(
                        "¿En qué momento exacto debería empezar? (HH:MM:SS,mmm)"
                    )
                    manager.sync_subtitles(idx, real_time)

            case 4:
                manager.save()
                console.print("[bold green]¡Hasta luego![/bold green]")
                break

            case 0:
                console.print("[red]Saliendo sin guardar cambios...[/red]")
                break


if __name__ == "__main__":
    main()

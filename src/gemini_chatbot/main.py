import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from .config import load_gemini_client
from .client import GeminiChatSession

console = Console()

def run_chat():
    console.print(
        Panel.fit(
            "[bold cyan]🤖 Gemini 3.1 Flash-Lite 터미널 챗봇[/bold cyan]\n"
            "[dim]Google Interactions API 기반 대화형 CLI[/dim]\n\n"
            "• 종료: [bold yellow]'exit'[/bold yellow], [bold yellow]'quit'[/bold yellow], [bold yellow]'q'[/bold yellow]\n"
            "• 대화 초기화: [bold yellow]'clear'[/bold yellow] 또는 [bold yellow]'reset'[/bold yellow]",
            border_style="cyan"
        )
    )

    client = load_gemini_client()
    session = GeminiChatSession(client=client, model="gemini-3.1-flash-lite")

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                console.print("\n[yellow]대화를 종료합니다. 좋은 하루 되세요![/yellow]")
                break

            if user_input.lower() in ("clear", "reset"):
                session.reset()
                console.print("[dim italic]✨ 대화 문맥이 초기화되었습니다.[/dim italic]")
                continue

            console.print("[bold magenta]Gemini[/bold magenta]: ", end="")

            accumulated_response = []
            try:
                for chunk in session.send_message_stream(user_input):
                    console.print(chunk, end="", highlight=False)
                    accumulated_response.append(chunk)
                console.print()  # 줄바꿈
            except Exception as e:
                console.print(f"\n[bold red]오류 발생:[/bold red] {e}")

        except (KeyboardInterrupt, EOFError):
            console.print("\n\n[yellow]프로그램이 종료되었습니다.[/yellow]")
            sys.exit(0)

def main():
    run_chat()

if __name__ == "__main__":
    main()


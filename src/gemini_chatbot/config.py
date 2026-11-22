import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from rich.console import Console

console = Console()

def load_gemini_client() -> genai.Client:
    """
    .env 및 시스템 환경변수에서 GEMINI_API_KEY를 로드하고 genai.Client를 초기화합니다.
    """
    # 프로젝트 루트의 .env 탐색 및 로드
    base_dir = Path(__file__).resolve().parent.parent.parent
    env_file = base_dir / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        console.print("\n[bold red]❌ 오류: GEMINI_API_KEY가 설정되지 않았습니다![/bold red]")
        console.print("[yellow]아래 방법 중 하나로 API 키를 설정해주세요:[/yellow]")
        console.print("  1. [cyan]gemini-chatbot/.env[/cyan] 파일 생성 후 [bold]GEMINI_API_KEY=your_key[/bold] 입력")
        console.print("  2. 환경 변수로 등록: [bold]export GEMINI_API_KEY='your_key'[/bold] (또는 PowerShell: [bold]$env:GEMINI_API_KEY='your_key'[/bold])")
        console.print("\n👉 [dim]API 키 무료 발급 링크: https://aistudio.google.com/apikey[/dim]\n")
        sys.exit(1)

    return genai.Client(api_key=api_key)


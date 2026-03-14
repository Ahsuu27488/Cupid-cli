"""
Main CLI application for Cupid with beautiful Rich formatting.
"""

import asyncio
import sys
from pathlib import Path

import rich
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.text import Text

from .agent import get_agent
from .config import config

# Rich console setup
console = Console()


def print_banner() -> None:
    """Print the Cupid banner with love."""
    banner = """
╔════════════════════════════════════════════════════════╗
║                    💝 FOR ASHU 💝                     ║
║         🏹 Cupid - A Gift From Ahsan's Heart 🏹       ║
║           An AI Companion Crafted With Love           ║
╚════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold magenta")


def print_help() -> None:
    """Print help message."""
    help_text = """
[bold cyan]Commands:[/bold cyan]
  [green]exit[/green]     - Leave Cupid (but she'll miss you!)
  [green]clear[/green]    - Start fresh, clear conversation memory
  [green]stats[/green]    - Show conversation statistics
  [green]help[/green]     - Show this help message

[bold cyan]Languages:[/bold cyan]
  Type in English or Roman Urdu - Cupid will match your language!

[bold cyan]Tips:[/bold cyan]
  • Keep messages short and sweet
  • Cupid remembers your conversations
  • She's shy at first, but warms up quickly 💕
    """
    console.print(Panel(help_text, title="💝 Help", border_style="magenta"))


async def chat_loop() -> None:
    """Main interactive chat loop."""
    agent = get_agent()

    # Welcome message
    console.print("\n[bold magenta]Hey Ashu![/bold magenta] 😊 I'm Cupid, here to make your day brighter.\n")
    print_help()
    console.print()

    while True:
        try:
            # Get user input with Rich prompt
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()

            if user_input.lower() == 'exit':
                console.print("\n[bold magenta]Catch you later, Ashu![/bold magenta] Take care. 💕\n")
                break

            if user_input.lower() == 'clear':
                agent.clear_history()
                console.print("[yellow]Conversation history cleared. Fresh start! ✨[/yellow]\n")
                continue

            if user_input.lower() == 'help':
                print_help()
                continue

            if user_input.lower() == 'stats':
                agent_instance = get_agent()
                stats = agent_instance.memory.get_stats()
                stats_text = f"""
[bold magenta]Conversation Stats:[/bold magenta]

  [cyan]Messages:[/cyan] {stats['total_messages']} total
  [cyan]Active:[/cyan] {stats['active_messages']} (not summarized)
  [cyan]Summaries:[/cyan] {stats['total_summaries']} generated
  [cyan]Tokens:[/cyan] {stats['total_tokens']} used

[dim]Summarization helps Cupid remember longer conversations![/dim]
                """
                console.print(Panel(stats_text, title="💝 Stats", border_style="magenta"))
                continue

            if not user_input:
                continue

            # Show typing indicator
            with console.status("[italic magenta]Cupid is thinking...", spinner="dots"):
                response = await agent.chat(user_input)

            # Print response with cute formatting
            console.print()
            response_text = Text(f"Cupid: {response}", style="bold pink")
            console.print(response_text)
            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[bold magenta]Agent session interrupted. Goodbye![/bold magenta]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")


async def main() -> None:
    """Main entry point."""
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        console.print("\n[yellow]Please create a .env file with:[/yellow]")
        console.print("  OPENAI_API_KEY=your_key_here")
        console.print("  MODEL=gpt-4o-mini  (or any OpenAI model)")
        sys.exit(1)

    print_banner()

    # Check if running in Termux (nice touch)
    if Path("/data/data/com.termux").exists():
        console.print("[dim]Termux detected 🌟 Perfect for phone chat![/dim]\n")

    try:
        await chat_loop()
    finally:
        # Cleanup
        agent = get_agent()
        agent.close()


if __name__ == "__main__":
    asyncio.run(main())

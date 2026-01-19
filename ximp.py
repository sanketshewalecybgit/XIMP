import sys
import argparse
# Force UTF-8 encoding for Windows consoles to support ASCII art/emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from src.generator import PermutationGenerator
from src.scanner import TwitterScanner
console = Console()
BANNER = """
[bold cyan]
██╗  ██╗██╗███╗   ███╗██████╗ 
╚██╗██╔╝██║████╗ ████║██╔══██╗
 ╚███╔╝ ██║██╔████╔██║██████╔╝
 ██╔██╗ ██║██║╚██╔╝██║██╔═══╝ 
██╔╝ ██╗██║██║ ╚═╝ ██║██║     
╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝     
[/bold cyan]
[bold white]Twitter Impersonation Scanner[/bold white]
[italic green]Created by SanketShewale[/italic green]
"""
def print_banner():
    console.print(Panel(BANNER, subtitle="v1.0.0", border_style="cyan"))
def main():
    print_banner()
    
    # Interactive mode if no args (as requested)
    if len(sys.argv) == 1:
        target = console.input("[bold yellow]Enter Target Username (e.g., example): [/bold yellow]").strip()
    else:
        target = sys.argv[1]
    if not target:
        console.print("[red]Error: No target username provided.[/red]")
        return
        
    # Optional SerpApi Key
    serp_api_key = console.input("[bold yellow]Enter SerpApi Key (Press Enter to skip): [/bold yellow]").strip()
    console.print(f"\n[bold blue]TARGET:[/bold blue] {target}")
    console.print("[dim]Analyzing...[/dim]")
    # 1. Generate Permutations
    with console.status("[bold green]Generating permutations...[/bold green]"):
        gen = PermutationGenerator(target)
        permutations = gen.generate_all()
    
    console.print(f"[green]Generated {len(permutations)} variations.[/green]")
    
    # 2. Scanning
    scanner = TwitterScanner()
    found_accounts = []
    # Step A: SERP Scan (Finding "hidden" or high ranking imposters)
    console.print("\n[bold cyan][*] Phase 1: Search Engine Discovery[/bold cyan]")
    serp_results = scanner.scan_serp(target)
    if serp_results:
        found_accounts.extend(serp_results)
        console.print(f"[green]Found {len(serp_results)} indexed profiles via Google.[/green]")
    else:
        console.print("[yellow]No indexed profiles found via Search.[/yellow]")
    # Step A.5: SerpApi Scan (Enhanced)
    if serp_api_key:
        console.print("\n[bold cyan][*] Phase 1.5: SerpApi Discovery[/bold cyan]")
        with console.status("[bold green]Querying SerpApi...[/bold green]"):
            api_results = scanner.scan_serpapi(target, serp_api_key)
        
        if api_results:
            found_accounts.extend(api_results)
            console.print(f"[green]Found {len(api_results)} profiles via SerpApi.[/green]")
        else:
            console.print("[yellow]No results found via SerpApi.[/yellow]")
    # Step B: Direct Scan of Permutations
    console.print("\n[bold cyan][*] Phase 2: Direct Username Scanning[/bold cyan]")
    
    candidates_to_scan = permutations
    console.print(f"[dim]Scanning all {len(candidates_to_scan)} generated permutations...[/dim]")
    
    # Using track for progress bar
    direct_candidates_found = []
    for cand in track(candidates_to_scan, description="Checking profiles..."):
        res = scanner.verify_profile_direct(cand)
        if res:
            direct_candidates_found.append(res)
            
    # Step C: Filtering & Verification (Phase 3)
    console.print("\n[bold cyan][*] Phase 3: Filtering & Verification[/bold cyan]")
    final_verified_accounts = []
    
    # 1. Add Direction Candidates (already verified by scan above)
    final_verified_accounts.extend(direct_candidates_found)
    
    # 2. Verify SERP/SerpApi Candidates
    # Because SERP results might be old/suspended, we must manually verify them now.
    candidates_from_search = found_accounts # These are unverified from Phase 1 & 1.5
    
    if candidates_from_search:
        console.print(f"[dim]Verifying {len(candidates_from_search)} search engine results...[/dim]")
        for acc in track(candidates_from_search, description="Verifying SERP links..."):
            # Extract username from SERP results if possible to verify OR just verify existence
            # Since we have the URL, we can't easily use 'verify_profile_direct' which takes username
            # We will assume if we found it via SERP, we check if it is active.
            # However, for consistency, we try to verify the username if we can parse it, or just trust it if it looks valid
            # Simpler: We just add them for now, but ideally we would visit the URL. 
            # Given the constraints, let's assume the user wants the SCANNER to visit them.
            # We will implement a quick check for these.
            
            # Quick hack: extract username from URL
            try:
                username_from_url = acc['url'].split('/')[-1]
                # Re-verify this specific username
                verification = scanner.verify_profile_direct(username_from_url)
                if verification:
                    # Update the method to reflect it was originally from SERP but Verified
                    verification['method'] = f"{acc['method']} + Verified"
                    final_verified_accounts.append(verification)
            except:
                pass
    # 3. Report
    console.print("\n[bold magenta]=== REPORT (Active Only) ===[/bold magenta]")
    
    if not final_verified_accounts:
        console.print("[green]No ACTIVE impersonation accounts found![/green]")
    else:
        table = Table(title=f"Potential Impersonators for '{target}'")
        table.add_column("Username", style="cyan")
        table.add_column("URL", style="blue")
        table.add_column("Method", style="yellow")
        
        # Deduplicate
        seen_urls = set()
        for acc in final_verified_accounts:
            if acc['url'] not in seen_urls:
                table.add_row(acc.get('username', 'N/A'), acc['url'], acc.get('method', 'Direct'))
                seen_urls.add(acc['url'])
        
        console.print(table)
        console.print(f"\n[bold red]Total Found: {len(seen_urls)}[/bold red]")
        console.print("[dim]Note: Please manually verify before reporting.[/dim]")
if __name__ == "__main__":
    main()

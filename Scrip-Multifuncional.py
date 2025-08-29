#!/usr/bin/env python3

import sys
import time
import psutil
import platform
import subprocess
import argparse
from datetime import datetime
from pathlib import Path


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class DeepTools:
    def __init__(self):
        self.start_time = time.time()

    def print_banner(self):
        banner = (
            f"{Colors.CYAN}{Colors.BOLD}\n"
            "╔══════════════════════════════════════════════════════════╗\n"
            "║                 DEEPTOOLS - v1.0                         ║\n"
            "║                 Ferramentas Avançadas                    ║\n"
            "╚══════════════════════════════════════════════════════════╝\n"
            f"{Colors.RESET}\n"
        )
        print(banner)

    def system_info(self):
        print(
            f"{Colors.BOLD}{Colors.YELLOW}"
            "=== INFORMAÇÕES DO SISTEMA ==="
            f"{Colors.RESET}"
        )

        info = {
            "Sistema": platform.system(),
            "Versão": platform.release(),
            "Arquitetura": platform.architecture()[0],
            "Processador": platform.processor(),
            "Núcleos Físicos": psutil.cpu_count(logical=False),
            "Núcleos Lógicos": psutil.cpu_count(logical=True),
            "Memória Total": (
                f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
            )
        }

        for key, value in info.items():
            print(
                f"{Colors.GREEN}{key}:{Colors.RESET} {value}"
            )

    def monitor_resources(self, interval: int = 2):
        print(
            f"\n{Colors.BOLD}{Colors.YELLOW}"
            "=== MONITORAMENTO (Ctrl+C para parar) ==="
            f"{Colors.RESET}"
        )

        try:
            while True:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                print(
                    (
                        f"{Colors.CYAN}CPU: {cpu_percent}% | "
                        f"Memória: {memory.percent}% | "
                        f"Disco: {disk.percent}%{Colors.RESET}"
                    ),
                    end='\r'
                )
                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Monitoramento encerrado.{Colors.RESET}")

    def file_operations(self, path: str):
        print(
            f"{Colors.BOLD}{Colors.YELLOW}"
            "=== OPERAÇÕES DE ARQUIVO ==="
            f"{Colors.RESET}"
        )

        p = Path(path)
        if not p.exists():
            print(f"{Colors.RED}Path não existe!{Colors.RESET}")
            return

        if p.is_file():
            print(f"{Colors.GREEN}Arquivo:{Colors.RESET} {p.name}")
            print(
                f"{Colors.GREEN}Tamanho:{Colors.RESET} "
                f"{p.stat().st_size} bytes"
            )
            print(
                f"{Colors.GREEN}Modificado:{Colors.RESET} "
                f"{datetime.fromtimestamp(p.stat().st_mtime)}"
            )

        elif p.is_dir():
            files = list(p.iterdir())
            print(
                f"{Colors.GREEN}Itens no diretório:{Colors.RESET} "
                f"{len(files)}"
            )

            for item in files[:10]:
                prefix = "📁" if item.is_dir() else "📄"
                print(f"  {prefix} {item.name}")

    def network_ping(self, host: str):
        print(
            f"{Colors.BOLD}{Colors.YELLOW}"
            "=== TESTE DE PING ==="
            f"{Colors.RESET}"
        )

        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "4", host]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"{Colors.CYAN}{result.stdout}{Colors.RESET}")

        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}Timeout ao pingar {host}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.RESET}")

    def run_time(self):
        return time.time() - self.start_time


def main():
    parser = argparse.ArgumentParser(
        description="DeepTools - Ferramentas Avançadas"
    )
    parser.add_argument(
        '-s', '--system',
        action='store_true',
        help='Informações do sistema'
    )
    parser.add_argument(
        '-m', '--monitor',
        action='store_true',
        help='Monitorar recursos'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Analisar arquivo/diretório'
    )
    parser.add_argument(
        '-p', '--ping',
        type=str,
        help='Testar ping para host'
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Executar todas as verificações'
    )

    args = parser.parse_args()

    tool = DeepTools()
    tool.print_banner()

    if args.system or args.all:
        tool.system_info()

    if args.monitor or args.all:
        tool.monitor_resources()

    if args.file:
        tool.file_operations(args.file)

    if args.ping:
        tool.network_ping(args.ping)

    if not any(vars(args).values()):
        parser.print_help()

    print(
        f"\n{Colors.PURPLE}Tempo de execução: "
        f"{tool.run_time():.2f} segundos{Colors.RESET}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SubTakeover 3.0 – versão profissional em Python
# Mantém lógica didática original, mas 20x mais rápida

import dns.resolver
import requests
import concurrent.futures
import json
import sys
from datetime import datetime

# =============================
# Configurações
# =============================
TIMEOUT = 4
THREADS = 50
TAKEOVER_PATTERNS = [
    "no such app",
    "there isn't a github pages site",
    "does not exist",
    "not found",
    "heroku",
    "unclaimed",
    "invalid dns",
    "is not a registered domain",
    "you can claim",
]

results = []

# =============================
# Funções
# =============================

def check_subdomain(domain, word):
    full = f"{word}.{domain}"

    try:
        # Busca CNAME (igual ao script do professor)
        answers = dns.resolver.resolve(full, "CNAME", lifetime=TIMEOUT)
        cname = str(answers[0].target)

        info = {"subdomain": full, "cname": cname, "takeover": False}

        # Detectar takeover via conteúdo HTTP
        try:
            r = requests.get(f"http://{full}", timeout=TIMEOUT)
            html = r.text.lower()

            for pattern in TAKEOVER_PATTERNS:
                if pattern in html:
                    info["takeover"] = True
                    break

        except Exception:
            pass  # erro HTTP ignorado

        print(f"[FOUND] {full} -> {cname}")
        if info["takeover"]:
            print(f"[POSSÍVEL TAKEOVER] {full}")

        results.append(info)

    except Exception:
        pass  # sem CNAME → ignora

def load_wordlist(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# =============================
# Main
# =============================

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 subtakeover.py <dominio> <wordlist>")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist = sys.argv[2]

    words = load_wordlist(wordlist)

    print(f"[+] Dominio: {domain}")
    print(f"[+] Wordlist: {len(words)} entradas")
    print(f"[+] Threads: {THREADS}")
    print("[+] Iniciando varredura...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(lambda w: check_subdomain(domain, w), words)

    # salvar resultado final
    print("\n[+] Salvando resultados…")

    with open("subtakeover_results.txt", "w") as f:
        for r in results:
            takeover = "TAKEOVER" if r["takeover"] else "OK"
            f.write(f"{r['subdomain']} -> {r['cname']} [{takeover}]\n")

    with open("subtakeover_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("[+] Arquivos salvos:")
    print("    subtakeover_results.txt")
    print("    subtakeover_results.json")
    print("\n[✓] Finalizado.")

if __name__ == "__main__":
    main()

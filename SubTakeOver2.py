#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import dns.resolver

def banner():
    print("""
______     _   _____     _       _____             ___ 
|   __|_ _| |_|_   _|___| |_ ___|     |_ _ ___ ___|_  |
|__   | | | . | | | | .'| '_| -_|  |  | | | -_|  _|  _|
|_____|___|___| |_| |__,|_,_|___|_____|\\_/|___|_| |___|

""")

def load_wordlist(path):
    if path is None:
        print("[!] Nenhuma wordlist informada. Abortando.")
        sys.exit(1)

    if not os.path.isfile(path):
        print(f"[!] Wordlist não encontrada: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def resolve_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, "CNAME")
        for rdata in answers:
            return str(rdata.target)
    except:
        return None

def check_takeover(cname):
    """
    Detecta padrões comuns de subdomain takeover.
    Basta adicionar fingerprints novos se quiser evoluir o script.
    """
    takeover_patterns = {
        "github.io": "Possível GitHub Pages Takeover",
        "amazonaws.com": "Possível S3 Takeover",
        "herokuapp.com": "Possível Heroku Takeover",
        "azurewebsites.net": "Possível Azure Takeover",
        "cloudfront.net": "Possível CloudFront Takeover",
        "fastly.net": "Possível Fastly Takeover",
        "key.vlab.takeover": "Key encontrada!"
    }

    for key in takeover_patterns:
        if key in cname:
            return takeover_patterns[key]

    return None

def main():
    parser = argparse.ArgumentParser(description="Scanner de Subdomain Takeover via CNAME")
    parser.add_argument("-d", "--domain", required=True, help="Domínio alvo")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist de subdomínios")
    args = parser.parse_args()

    domain = args.domain.strip()
    wordlist = load_wordlist(args.wordlist)

    banner()
    print(f"[+] Domínio: {domain}")
    print(f"[+] Wordlist: {args.wordlist}")
    print(f"[+] Total de entradas: {len(wordlist)}")
    print("-------------------------------------------\n")

    results = []

    for word in wordlist:
        sub = f"{word}.{domain}"
        cname = resolve_cname(sub)

        if cname:
            status = check_takeover(cname)
            if status:
                print(f"[!] POSSÍVEL TAKEOVER ENCONTRADO!")
                print(f"    Subdomínio: {sub}")
                print(f"    CNAME: {cname}")
                print(f"    Status: {status}\n")
                results.append((sub, cname, status))
            else:
                print(f"[OK] {sub} -> {cname}")
        else:
            print(f"[X] {sub}")

    print("\n===========================================")
    print("               RESULTADOS")
    print("===========================================\n")

    if results:
        for sub, cname, status in results:
            print(f"[TAKEOVER] {sub} -> {cname} ({status})")
    else:
        print("Nenhum subdomain takeover encontrado.")

    print("\n[+] Finalizado.")
    

if __name__ == "__main__":
    main()

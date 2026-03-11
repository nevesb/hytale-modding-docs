#!/usr/bin/env python3
"""
Adiciona ponto e vírgula ao final de cada declaração em blocos Mermaid
para que o diagrama seja válido quando o código for passado em uma única linha.
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "src" / "content" / "docs"

def fix_mermaid_block(content: str) -> str:
    """Dentro de um bloco mermaid, adiciona ; onde necessário."""
    lines = content.splitlines()
    out = []
    for line in lines:
        stripped = line.rstrip()
        # Fim do bloco ou linha vazia: não alterar
        if stripped == "```" or not stripped:
            out.append(stripped)
            continue
        # Já termina com ; : não alterar
        if stripped.endswith(";"):
            out.append(stripped)
            continue
        # flowchart TD ou LR sem ; -> adicionar ;
        if re.match(r"^\s*flowchart\s+(TD|LR)\s*$", stripped, re.IGNORECASE):
            out.append(stripped + ";")
            continue
        # Linha de aresta (--> ) ou style -> adicionar ;
        if "-->" in stripped or re.match(r"^\s*style\s+", stripped):
            out.append(stripped + ";")
            continue
        out.append(stripped)
    return "\n".join(out) + "\n"

def process_file(path: Path) -> bool:
    """Processa um arquivo .md e corrige blocos mermaid. Retorna True se alterou algo."""
    text = path.read_text(encoding="utf-8")
    # Aceita \n ou \r\n após ```mermaid
    pattern = r"```mermaid\r?\n(.*?)```"
    blocks = list(re.finditer(pattern, text, re.DOTALL))
    if not blocks:
        return False
    new_text = text
    for m in reversed(blocks):  # reverso para não deslocar índices
        block_content = m.group(1)
        fixed = fix_mermaid_block(block_content)
        if fixed != block_content:
            new_text = new_text[: m.start(1)] + fixed + new_text[m.end(1) :]
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    modified = []
    for path in sorted(DOCS.rglob("*.md")):
        if process_file(path):
            modified.append(str(path.relative_to(DOCS)))
    if modified:
        print("Arquivos alterados:")
        for p in modified:
            print(" ", p)
        print(f"\nTotal: {len(modified)} arquivo(s)")
    else:
        print("Nenhum bloco Mermaid precisou de alteração.")

if __name__ == "__main__":
    main()

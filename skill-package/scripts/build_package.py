from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "package"


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    if PACKAGE.exists():
        for child in PACKAGE.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        PACKAGE.mkdir(parents=True)

    copy_file(ROOT / "SKILL.md", PACKAGE / "SKILL.md")
    copy_file(ROOT / "README.md", PACKAGE / "README.md")

    references_src = ROOT / "references"
    references_dst = PACKAGE / "references"
    for name in ("workflow.md", "templates.md", "examples.md", "execution-guardrails.md"):
        copy_file(references_src / name, references_dst / name)

    agents_src = ROOT / "agents"
    if agents_src.exists():
        for path in agents_src.rglob("*"):
            if path.is_file():
                copy_file(path, PACKAGE / "agents" / path.relative_to(agents_src))


if __name__ == "__main__":
    main()

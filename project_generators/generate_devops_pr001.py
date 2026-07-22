from __future__ import annotations

import os
import textwrap
import time
from pathlib import Path
from typing import Dict, List, Sequence

HEADER = """
====================================================
OpenNetManager Engineering Toolkit
Repository Hardening
====================================================
""".strip("\n")

SETTINGS_MARKERS: Sequence[tuple[str, ...]] = (
    ("config", "settings", "base.py"),
    ("config", "settings.py"),
    ("config", "settings", "__init__.py"),
)

DIRECTORIES: tuple[str, ...] = (
    ".github",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "project_generators",
    "docker",
    "scripts",
    "docs/rfc",
    "docs/deployment",
    "docs/development",
)

FILES: Dict[str, str] = {
    ".github/PULL_REQUEST_TEMPLATE.md": '''
## Objetivo

Descreva com clareza o objetivo desta mudança.

## Tipo da mudança

- [ ] Feature
- [ ] Bug
- [ ] Refactor
- [ ] Documentation
- [ ] DevOps
- [ ] Test

## Checklist

- [ ] Testes adicionados ou atualizados.
- [ ] Documentação atualizada quando aplicável.
- [ ] Lint executado com sucesso.
- [ ] Coverage preservado ou melhorado.
- [ ] Não houve quebra de compatibilidade não documentada.
- [ ] O PR respeita a arquitetura oficial do OpenNetManager.

## Evidências

Inclua logs, screenshots, resultados de testes ou observações relevantes.

## Observações adicionais

Registre trade-offs, limitações conhecidas ou decisões relevantes.
''',
    ".github/CODEOWNERS": '''
# Ajuste este arquivo antes da publicação oficial do repositório.
# Substitua @SEU_USUARIO pelos mantenedores reais do projeto.

* @SEU_USUARIO
''',
    ".github/dependabot.yml": '''
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "python"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "github-actions"
''',
    "README.md": '''
# OpenNetManager

OpenNetManager é uma plataforma Open Source para gerenciamento de equipamentos de rede com arquitetura preparada para múltiplos fabricantes.

## Objetivo

O projeto centraliza coleta, inventário, observabilidade e operações de dispositivos de rede sem acoplar a aplicação a um único fabricante ou modelo.

## Arquitetura

A arquitetura oficial segue o fluxo abaixo:

View

↓

Service

↓

Repository

↓

Driver

↓

SSH

↓

Parser

↓

Domain Objects

Princípios adotados:

- SOLID
- Clean Architecture
- Repository Pattern
- Service Layer
- Driver Pattern
- Parser Pattern
- Separation of Concerns
- Composition over Inheritance

## Tecnologias

- Python 3.13
- Django 5.2
- pytest
- mypy
- Black
- Flake8
- isort

## Roadmap

- Driver SDK Foundation
- SSH Framework
- Parser Framework
- Migração do AP130 para o novo SDK
- Suporte ao Grandstream GWN7600
- Dashboard orientado por capabilities
- Evolução de repositórios, snapshots e histórico
- Fortalecimento de CI/CD e observabilidade

## Como executar

### Com uv

```bash
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

### Com Python

```bash
python manage.py migrate
python manage.py runserver
```

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para detalhes.
''',
    "CHANGELOG.md": '''
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Repository hardening foundation for GitHub publication and engineering workflow.

### Changed
- None.

### Fixed
- None.
''',
    "CONTRIBUTING.md": '''
# Contributing

Obrigado por contribuir com o OpenNetManager.

## Fluxo de desenvolvimento

1. Crie uma branch a partir da base adequada.
2. Implemente uma mudança pequena, coerente e testável.
3. Execute testes e ferramentas de qualidade antes de abrir o PR.
4. Atualize documentação quando a mudança alterar comportamento, arquitetura ou operação.

## Branches

Sugestão de convenção:

- `main` para a linha estável principal.
- `feature/<nome>` para novas funcionalidades.
- `fix/<nome>` para correções.
- `refactor/<nome>` para refatorações internas.
- `docs/<nome>` para documentação.
- `devops/<nome>` para automações e esteira de engenharia.

## Conventional Commits

Utilize mensagens de commit claras e padronizadas, por exemplo:

- `feat(drivers): introduce capability registry`
- `fix(parser): handle empty output safely`
- `docs(rfc): add driver sdk specification`
- `chore(devops): add repository hardening generator`

## Pull Requests

Todo Pull Request deve:

- ter objetivo claro;
- manter o projeto funcional;
- conter escopo pequeno e revisável;
- incluir testes quando aplicável;
- incluir documentação quando aplicável;
- respeitar a arquitetura oficial do projeto.

## Revisão

A revisão deve verificar:

- aderência à arquitetura oficial;
- ausência de acoplamento indevido entre camadas;
- legibilidade e manutenibilidade do código;
- cobertura por testes;
- impacto operacional e de deploy.
''',
    "LICENSE": '''
MIT License

Copyright (c) 2026 OpenNetManager Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
}


class ConsoleReporter:
    """Simple console reporter for the engineering toolkit.

    Attributes:
        created_directories: List of created directories.
        created_files: List of created files.
        skipped_files: List of skipped files.
        existing_directories: List of directories that already existed.
    """

    def __init__(self) -> None:
        self.created_directories: List[str] = []
        self.created_files: List[str] = []
        self.skipped_files: List[str] = []
        self.existing_directories: List[str] = []

    def created_dir(self, path: str) -> None:
        self.created_directories.append(path)
        print(f"[CREATE DIR] {path}")

    def existing_dir(self, path: str) -> None:
        self.existing_directories.append(path)
        print(f"[EXISTS DIR] {path}")

    def created_file(self, path: str) -> None:
        self.created_files.append(path)
        print(f"[CREATE FILE] {path}")

    def skipped_file(self, path: str) -> None:
        self.skipped_files.append(path)
        print(f"[SKIP] {path}")


class RepositoryHardeningGenerator:
    """Generate repository hardening files for OpenNetManager.

    This generator is intentionally conservative: it creates only missing
    directories and files, and never overwrites existing project content.
    """

    def __init__(self) -> None:
        self.reporter = ConsoleReporter()

    def run(self) -> int:
        """Execute the generator.

        Returns:
            Process exit code.
        """
        started_at = time.perf_counter()
        print(HEADER)

        project_root = self._find_project_root(Path.cwd())
        if project_root is None:
            self._print_not_found_diagnostics(Path.cwd())
            return 1

        print()
        print("Projeto localizado")
        print(f"✓ {project_root}")
        print()

        self._create_directories(project_root)
        self._create_files(project_root)
        self._print_summary(started_at)
        return 0

    def _find_project_root(self, start: Path) -> Path | None:
        """Locate the project root walking upward from the current directory.

        Args:
            start: Current working directory.

        Returns:
            The detected root path or None.
        """
        resolved = start.resolve()
        for candidate in (resolved, *resolved.parents):
            if self._is_project_root(candidate):
                return candidate
        return None

    def _is_project_root(self, path: Path) -> bool:
        """Check whether the path matches supported project root markers.

        Args:
            path: Candidate path.

        Returns:
            True when the path contains manage.py and at least one supported
            Django settings marker.
        """
        if not (path / "manage.py").exists():
            return False
        return any((path / Path(*marker)).exists() for marker in SETTINGS_MARKERS)

    def _print_not_found_diagnostics(self, current: Path) -> None:
        """Print a friendly diagnostic when project root is not found.

        Args:
            current: Current working directory.
        """
        print("Projeto OpenNetManager não localizado.")
        print("Certifique-se de executar este script dentro do repositório.")
        print()
        print("Diretório atual")
        print(f"- {current.resolve()}")
        print()
        print("Marcadores verificados no diretório atual")
        print(f"- manage.py: {'OK' if (current / 'manage.py').exists() else 'MISSING'}")
        for marker in SETTINGS_MARKERS:
            marker_path = current / Path(*marker)
            print(f"- {marker_path.relative_to(current)}: {'OK' if marker_path.exists() else 'MISSING'}")
        print()
        print("Layouts aceitos para settings")
        print("- config/settings/base.py")
        print("- config/settings.py")
        print("- config/settings/__init__.py")

    def _create_directories(self, project_root: Path) -> None:
        """Create missing directories only.

        Args:
            project_root: Repository root path.
        """
        for relative_dir in DIRECTORIES:
            destination = project_root / relative_dir
            if destination.exists():
                self.reporter.existing_dir(relative_dir)
                continue
            destination.mkdir(parents=True, exist_ok=True)
            self.reporter.created_dir(relative_dir)

    def _create_files(self, project_root: Path) -> None:
        """Create missing files only.

        Args:
            project_root: Repository root path.
        """
        for relative_path, content in FILES.items():
            destination = project_root / relative_path
            if destination.exists():
                self.reporter.skipped_file(relative_path)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(self._normalize(content), encoding="utf-8")
            self.reporter.created_file(relative_path)

    def _normalize(self, content: str) -> str:
        """Normalize multi-line string content.

        Args:
            content: Raw file content.

        Returns:
            Normalized content.
        """
        return textwrap.dedent(content).lstrip("\n")

    def _print_summary(self, started_at: float) -> None:
        """Print execution summary.

        Args:
            started_at: Start time from perf_counter.
        """
        elapsed = time.perf_counter() - started_at
        print()
        print("Diretórios criados")
        if self.reporter.created_directories:
            for item in self.reporter.created_directories:
                print(f"- {item}")
        else:
            print("- Nenhum")

        print()
        print("Arquivos criados")
        if self.reporter.created_files:
            for item in self.reporter.created_files:
                print(f"- {item}")
        else:
            print("- Nenhum")

        print()
        print("Arquivos ignorados")
        if self.reporter.skipped_files:
            for item in self.reporter.skipped_files:
                print(f"- {item}")
        else:
            print("- Nenhum")

        print()
        print("Diretórios existentes")
        if self.reporter.existing_directories:
            for item in self.reporter.existing_directories:
                print(f"- {item}")
        else:
            print("- Nenhum")

        print()
        print("Tempo de execução")
        print(f"- {elapsed:.3f}s")

        print()
        print("Resumo")
        print("- Nenhum arquivo foi sobrescrito.")
        print(f"- {len(self.reporter.created_directories)} diretórios criados.")
        print(f"- {len(self.reporter.created_files)} arquivos criados.")
        print(f"- {len(self.reporter.skipped_files)} arquivos ignorados.")


def main() -> int:
    """Program entrypoint.

    Returns:
        Process exit code.
    """
    generator = RepositoryHardeningGenerator()
    return generator.run()


if __name__ == "__main__":
    raise SystemExit(main())

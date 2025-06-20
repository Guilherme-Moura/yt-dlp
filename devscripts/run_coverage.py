# devscripts/run_coverage.py
#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).parent.parent

def main():
    args = sys.argv[1:]

    if not args:
        test_path = 'test'
        module_path = 'yt_dlp'
    elif len(args) == 1:
        test_path = args[0]
        module_path = 'yt_dlp'
    else:
        test_path = args[0]
        module_path = args[1]

    # Comando para rodar pytest com coverage
    # O coverage.py irá automaticamente criar arquivos de dados separados em modo paralelo
    cmd = [
        'python', '-m', 'pytest',
        f'--cov={module_path}',
        '--cov-config=.coveragerc',
        '--cov-report=',  # Desabilita o relatório de terminal aqui
        test_path,
    ]

    # Adiciona argumentos extras do pytest se houver
    if len(args) > 2:
        cmd.extend(args[2:])

    print(f'Running coverage on {test_path} for module(s) {module_path}')
    print(f'Command: {" ".join(cmd)}')

    try:
        # Usamos --cov-append para garantir que as execuções não sobrescrevam os dados
        # Adicione `parallel = true` ao seu .coveragerc na seção [run]
        result = subprocess.run(cmd + ['--cov-append'], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f'Error running coverage: {e}')
        return e.returncode


if __name__ == '__main__':
    sys.exit(main())
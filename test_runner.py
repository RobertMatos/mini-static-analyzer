#!/usr/bin/env python3
"""
Test Runner para Static Checker CangaCode2025-1
Script de teste e validação do analisador léxico e tabela de símbolos
"""

import os
import sys
import subprocess
import re
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.test_dir = Path("tests")
        self.output_dir = Path("output")
        self.main_script = Path("main.py")
        self.results = []

    def setup_test_environment(self):
        """Configura ambiente de teste"""
        print("=== CONFIGURANDO AMBIENTE DE TESTE ===")

        # Criar diretórios necessários
        self.test_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

        # Verificar se main.py existe
        if not self.main_script.exists():
            print(f"❌ ERRO: {self.main_script} não encontrado!")
            return False

        print(f"✅ Estrutura de diretórios criada")
        print(f"✅ Script principal encontrado: {self.main_script}")
        return True

    def create_test_file(self):
        """Cria arquivo de teste exemplo.251"""
        test_content = '''program calculadoraSimples
declarations
  varType integer: contador, limite, resultado
  varType real: nota1, nota2, mediaFinal
  varType string: nomeAluno, disciplina
  varType boolean: aprovado
  varType character: opcao
  varType integer[]: numeros[50]
  varType real[]: medias[20]
endDeclararions
functions
  funcType integer: somar(paramType integer: num1; paramType integer: num2)
  {
    // Esta função soma dois números inteiros
    /* Comentário de bloco:
       Implementação simples de soma
       Retorna a soma dos parâmetros */
    resultado := num1 + num2
    return resultado
  }
  endFunction;

  funcType real: calcularMedia(paramType real: n1; paramType real: n2; paramType real: n3)
  {
    // Calcula média de três notas
    return (n1 + n2 + n3) / 3.0
  }
  endFunction;

  funcType void: processarDados()
  {
    contador := 0
    limite := 100

    if (contador < limite)
      print contador
    endIf

    while (contador <= limite)
    {
      contador := contador + 1;
      if (contador >= 50)
        break
      endIf
    }
    endWhile

    /* Loop de processamento concluído */
    // Fim da função
  }
  endFunction
endFunctions
endProgram'''

        test_file = self.test_dir / "exemplo.251"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)

        print(f"✅ Arquivo de teste criado: {test_file}")
        return test_file

    def run_static_checker(self, test_file):
        """Executa o Static Checker"""
        print(f"\n=== EXECUTANDO STATIC CHECKER ===")
        print(f"Analisando arquivo: {test_file}")

        try:
            # Executar main.py com o arquivo de teste (sem extensão)
            test_name = test_file.stem  # Remove extensão
            result = subprocess.run(
                [sys.executable, str(self.main_script), str(test_file.parent / test_name)],
                capture_output=True,
                text=True,
                timeout=30
            )

            print(f"Código de retorno: {result.returncode}")

            if result.stdout:
                print("STDOUT:")
                print(result.stdout)

            if result.stderr:
                print("STDERR:")
                print(result.stderr)

            return result.returncode == 0, result

        except subprocess.TimeoutExpired:
            print("❌ ERRO: Timeout na execução")
            return False, None
        except Exception as e:
            print(f"❌ ERRO na execução: {e}")
            return False, None

    def validate_output_files(self, test_file):
        """Valida se os arquivos de saída foram gerados"""
        print(f"\n=== VALIDANDO ARQUIVOS DE SAÍDA ===")

        base_name = test_file.stem
        lex_file = test_file.parent / f"{base_name}.LEX"
        tab_file = test_file.parent / f"{base_name}.TAB"

        results = {}

        # Verificar arquivo .LEX
        if lex_file.exists():
            print(f"✅ Arquivo .LEX gerado: {lex_file}")
            results['lex_exists'] = True
            results['lex_content'] = self.validate_lex_content(lex_file)
        else:
            print(f"❌ Arquivo .LEX não encontrado: {lex_file}")
            results['lex_exists'] = False

        # Verificar arquivo .TAB
        if tab_file.exists():
            print(f"✅ Arquivo .TAB gerado: {tab_file}")
            results['tab_exists'] = True
            results['tab_content'] = self.validate_tab_content(tab_file)
        else:
            print(f"❌ Arquivo .TAB não encontrado: {tab_file}")
            results['tab_exists'] = False

        return results

    def validate_lex_content(self, lex_file):
        """Valida conteúdo do arquivo .LEX"""
        print(f"\n--- Validando conteúdo .LEX ---")

        try:
            with open(lex_file, 'r', encoding='utf-8') as f:
                content = f.read()

            validation = {
                'has_header': False,
                'has_tokens': False,
                'token_count': 0,
                'expected_tokens': []
            }

            # Verificar cabeçalho
            if "RELATÓRIO DA ANÁLISE LÉXICA" in content:
                validation['has_header'] = True
                print("✅ Cabeçalho encontrado")
            else:
                print("❌ Cabeçalho não encontrado")

            # Contar tokens e verificar formato
            lines = content.split('\n')
            token_pattern = re.compile(r'Lexeme:\s*(\w+),\s*Código:\s*(\d+)')

            expected_tokens = [
                'program', 'calculadoraSimples', 'declarations', 'varType',
                'integer', 'contador', 'limite', 'resultado', 'real',
                'functions', 'funcType', 'somar', 'return'
            ]

            found_tokens = []
            for line in lines:
                match = token_pattern.search(line)
                if match:
                    lexeme = match.group(1)
                    found_tokens.append(lexeme)
                    validation['token_count'] += 1

            validation['found_tokens'] = found_tokens

            # Verificar se tokens esperados foram encontrados
            found_expected = [token for token in expected_tokens if token in found_tokens]
            validation['expected_found'] = found_expected

            print(f"✅ Tokens encontrados: {validation['token_count']}")
            print(f"✅ Tokens esperados encontrados: {len(found_expected)}/{len(expected_tokens)}")

            if validation['token_count'] > 0:
                validation['has_tokens'] = True

            # Mostrar alguns tokens para debug
            print("Primeiros 10 tokens encontrados:")
            for i, token in enumerate(found_tokens[:10]):
                print(f"  {i + 1}. {token}")

            return validation

        except Exception as e:
            print(f"❌ Erro ao validar .LEX: {e}")
            return {'error': str(e)}

    def validate_tab_content(self, tab_file):
        """Valida conteúdo do arquivo .TAB"""
        print(f"\n--- Validando conteúdo .TAB ---")

        try:
            with open(tab_file, 'r', encoding='utf-8') as f:
                content = f.read()

            validation = {
                'has_header': False,
                'has_symbols': False,
                'symbol_count': 0,
                'expected_symbols': []
            }

            # Verificar cabeçalho
            if "RELATÓRIO DA TABELA DE SÍMBOLOS" in content or "TABELA DE SÍMBOLOS" in content:
                validation['has_header'] = True
                print("✅ Cabeçalho encontrado")
            else:
                print("❌ Cabeçalho não encontrado")

            # Contar símbolos
            lines = content.split('\n')
            symbol_pattern = re.compile(r'Entrada:\s*(\d+)|Lexeme:\s*(\w+)')

            expected_symbols = [
                'calculadoraSimples', 'contador', 'limite', 'resultado',
                'nota1', 'nota2', 'mediaFinal', 'nomeAluno', 'disciplina',
                'aprovado', 'opcao', 'numeros', 'medias', 'somar', 'num1',
                'num2', 'calcularMedia', 'n1', 'n2', 'n3', 'processarDados'
            ]

            found_symbols = []
            for line in lines:
                if 'Entrada:' in line or 'Lexeme:' in line:
                    validation['symbol_count'] += 1
                    # Extrair nome do símbolo se possível
                    match = re.search(r'Lexeme:\s*(\w+)', line)
                    if match:
                        found_symbols.append(match.group(1))

            validation['found_symbols'] = found_symbols

            # Verificar símbolos esperados
            found_expected = [sym for sym in expected_symbols if sym in found_symbols]
            validation['expected_found'] = found_expected

            print(f"✅ Símbolos encontrados: {validation['symbol_count']}")
            print(f"✅ Símbolos esperados encontrados: {len(found_expected)}/{len(expected_symbols)}")

            if validation['symbol_count'] > 0:
                validation['has_symbols'] = True

            # Mostrar alguns símbolos para debug
            print("Primeiros 10 símbolos encontrados:")
            for i, symbol in enumerate(found_symbols[:10]):
                print(f"  {i + 1}. {symbol}")

            return validation

        except Exception as e:
            print(f"❌ Erro ao validar .TAB: {e}")
            return {'error': str(e)}

    def check_common_problems(self):
        """Verifica problemas comuns e sugere soluções"""
        print(f"\n=== DIAGNÓSTICO DE PROBLEMAS COMUNS ===")

        problems = []

        # Verificar estrutura de módulos
        required_files = [
            'main.py',
            'lexer/lexer.py',
            'parser/parser.py',
            'symbol_table/table.py'
        ]

        for file_path in required_files:
            if not Path(file_path).exists():
                problems.append(f"Arquivo ausente: {file_path}")

        # Verificar se PLY está instalado
        try:
            import ply
            print("✅ PLY instalado")
        except ImportError:
            problems.append("PLY não instalado: pip install ply")

        # Verificar arquivos __init__.py
        for dir_name in ['lexer', 'parser', 'symbol_table']:
            init_file = Path(dir_name) / '__init__.py'
            if Path(dir_name).exists() and not init_file.exists():
                problems.append(f"Arquivo __init__.py ausente em {dir_name}/")

        if problems:
            print("❌ Problemas encontrados:")
            for problem in problems:
                print(f"  • {problem}")
        else:
            print("✅ Nenhum problema comum detectado")

        return problems

    def generate_report(self, test_file, execution_success, validation_results):
        """Gera relatório final do teste"""
        print(f"\n=== RELATÓRIO FINAL DE TESTE ===")

        report = {
            'test_file': str(test_file),
            'execution_success': execution_success,
            'validation_results': validation_results,
            'overall_success': False
        }

        # Avaliar sucesso geral
        if execution_success and validation_results:
            lex_ok = validation_results.get('lex_exists', False)
            tab_ok = validation_results.get('tab_exists', False)

            if lex_ok and tab_ok:
                lex_content_ok = validation_results.get('lex_content', {}).get('has_tokens', False)
                tab_content_ok = validation_results.get('tab_content', {}).get('has_symbols', False)

                if lex_content_ok and tab_content_ok:
                    report['overall_success'] = True

        # Mostrar resultado
        if report['overall_success']:
            print("🎉 TESTE PASSOU! Static Checker funcionando corretamente.")
        else:
            print("❌ TESTE FALHOU. Verifique os problemas acima.")

        return report

    def run_full_test(self):
        """Executa teste completo"""
        print("🚀 INICIANDO TESTE COMPLETO DO STATIC CHECKER")
        print("=" * 60)

        # 1. Configurar ambiente
        if not self.setup_test_environment():
            return False

        # 2. Verificar problemas comuns
        self.check_common_problems()

        # 3. Criar arquivo de teste
        test_file = self.create_test_file()

        # 4. Executar Static Checker
        execution_success, exec_result = self.run_static_checker(test_file)

        # 5. Validar saídas
        validation_results = None
        if execution_success:
            validation_results = self.validate_output_files(test_file)
        else:
            print("❌ Execução falhou, pulando validação de saídas")

        # 6. Gerar relatório final
        report = self.generate_report(test_file, execution_success, validation_results)

        print("\n" + "=" * 60)
        print("TESTE CONCLUÍDO")

        return report['overall_success']


def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Test Runner para Static Checker CangaCode2025-1

Uso:
  python test_runner.py           # Executa teste completo
  python test_runner.py --help    # Mostra esta ajuda

O script irá:
1. Verificar estrutura do projeto
2. Criar arquivo de teste exemplo.251
3. Executar o Static Checker
4. Validar arquivos .LEX e .TAB gerados
5. Gerar relatório de resultados
        """)
        return

    runner = TestRunner()
    success = runner.run_full_test()

    # Código de saída para integração com CI/CD
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
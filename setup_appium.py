import os
import subprocess
import sys
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

# Função para verificar se um comando existe
def check_command(command):
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False

# Função para verificar se a licença do Xcode foi aceita
def check_xcode_license():
    try:
        # Tenta executar um comando que requer a licença aceita
        subprocess.run(["xcodebuild", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Função para verificar se o Xcode Command Line Tools está instalado
def is_xcode_command_line_tools_installed():
    try:
        # Verifica se o comando xcodebuild está disponível
        subprocess.run(["xcodebuild", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False

# Função para configurar o npm para usar um diretório local
def configure_npm():
    console.print("[bold]Configurando npm para usar um diretório local...[/bold]")
    npm_global_dir = os.path.expanduser("~/.npm-global")
    
    # Criar diretório global do npm, se não existir
    if not os.path.exists(npm_global_dir):
        os.makedirs(npm_global_dir)
    
    # Configurar o prefixo do npm
    subprocess.run(["npm", "config", "set", "prefix", npm_global_dir], check=True)
    
    # Adicionar diretório ao PATH no arquivo de configuração do shell
    shell_config_file = os.path.expanduser("~/.zshrc")  # ou ~/.bashrc, dependendo do shell
    export_path_line = f'export PATH={npm_global_dir}/bin:$PATH'
    
    if not os.path.exists(shell_config_file):
        open(shell_config_file, "w").close()  # Criar arquivo se não existir
    
    with open(shell_config_file, "r+") as f:
        lines = f.readlines()
        if export_path_line not in lines:
            f.write(f"\n{export_path_line}\n")
    
    console.print("[bold green]npm configurado com sucesso![/bold green]")
    console.print("[bold]Por favor, recarregue o shell manualmente com o comando abaixo:[/bold]")
    console.print(f"[bold]source {shell_config_file}[/bold]")
    console.print("[bold]Ou reinicie o terminal.[/bold]")

# Função para instalar o Homebrew
def install_homebrew():
    console.print("[bold]Verificando Homebrew...[/bold]")
    if not check_command("brew"):
        console.print("[bold red]Homebrew não encontrado. Instalando...[/bold red]")
        subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
        
        # Adicionar Homebrew ao PATH
        brew_path = "/opt/homebrew/bin"  # Caminho padrão no macOS com chips Apple Silicon
        if not os.path.exists(brew_path):
            brew_path = "/usr/local/bin"  # Caminho padrão no macOS com chips Intel
        
        shell_config_file = os.path.expanduser("~/.zshrc")  # ou ~/.bashrc, dependendo do shell
        export_path_line = f'export PATH={brew_path}:$PATH'
        
        with open(shell_config_file, "r+") as f:
            lines = f.readlines()
            if export_path_line not in lines:
                f.write(f"\n{export_path_line}\n")
        
        console.print("[bold green]Homebrew instalado com sucesso![/bold green]")
        console.print("[bold]Por favor, recarregue o shell manualmente com o comando abaixo:[/bold]")
        console.print(f"[bold]source {shell_config_file}[/bold]")
        console.print("[bold]Ou reinicie o terminal.[/bold]")
    else:
        console.print("[bold green]Homebrew já está instalado.[/bold green]")

# Função para instalar um pacote via Homebrew
def install_with_brew(package):
    console.print(f"[bold]Instalando {package}...[/bold]")
    subprocess.run(["brew", "install", package], check=True)

# Função para instalar um pacote via npm
def install_with_npm(package):
    console.print(f"[bold]Instalando {package}...[/bold]")
    subprocess.run(["npm", "install", "-g", package], check=True)

# Função para instalar o Xcode Command Line Tools
def install_xcode_command_line_tools():
    console.print("[bold]Verificando Xcode Command Line Tools...[/bold]")
    if not is_xcode_command_line_tools_installed():
        console.print("[bold red]Xcode Command Line Tools não encontrado. Instalando...[/bold red]")
        try:
            subprocess.run(["xcode-select", "--install"], check=True)
            console.print("[bold]Aguarde a conclusão da instalação do Xcode Command Line Tools.[/bold]")
            console.print("[bold]Siga as instruções na tela para concluir a instalação.[/bold]")
            # Aguardar a conclusão da instalação
            while not is_xcode_command_line_tools_installed():
                sleep(5)
            console.print("[bold green]Xcode Command Line Tools instalado com sucesso![/bold green]")
        except subprocess.CalledProcessError:
            console.print("[bold yellow]Xcode Command Line Tools já está instalado.[/bold yellow]")
    else:
        console.print("[bold green]Xcode Command Line Tools já está instalado.[/bold green]")
    
    # Verificar se a licença do Xcode foi aceita
    if not check_xcode_license():
        console.print("[bold red]A licença do Xcode não foi aceita.[/bold red]")
        console.print("[bold]Por favor, execute o seguinte comando para aceitar a licença:[/bold]")
        console.print("[bold]sudo xcodebuild -license[/bold]")
        console.print("[bold]Após aceitar a licença, execute este script novamente.[/bold]")
        sys.exit(1)

# Função para configurar o ambiente
def setup_environment():
    console.print("[bold]Configurando ambiente...[/bold]")
    
    # Verificar e instalar Homebrew
    install_homebrew()
    
    # Verificar e instalar Xcode Command Line Tools
    install_xcode_command_line_tools()
    
    # Configurar npm para usar um diretório local
    configure_npm()
    
    # Verificar e instalar Node.js
    if not check_command("node"):
        install_with_brew("node")
    
    # Verificar e instalar Appium
    if not check_command("appium"):
        install_with_npm("appium")
    
    # Verificar e instalar Appium Doctor
    if not check_command("appium-doctor"):
        install_with_npm("appium-doctor")
    
    # Verificar e instalar Java JDK
    if not check_command("java"):
        install_with_brew("openjdk")
    
    console.print("[bold green]Configuração concluída com sucesso![/bold green]")

# Função para criar um projeto básico de automação
def create_project():
    project_name = "meu-projeto-appium"
    console.print(f"[bold]Criando projeto básico de automação: {project_name}[/bold]")
    
    # Criar pasta do projeto
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    # Inicializar projeto Node.js
    subprocess.run(["npm", "init", "-y"], check=True)
    
    # Instalar dependências
    subprocess.run(["npm", "install", "webdriverio", "@wdio/cli", "--save-dev"], check=True)
    
    # Criar arquivo de teste básico
    with open("test.js", "w") as f:
        f.write("""
        const wdio = require("webdriverio");

        const opts = {
          path: '/wd/hub',
          port: 4723,
          capabilities: {
            platformName: "Android",
            platformVersion: "10",
            deviceName: "emulator-5554",
            app: "/caminho/para/sua/app.apk",
            automationName: "UiAutomator2"
          }
        };

        async function main() {
          const client = await wdio.remote(opts);

          // Exemplo de interação com o app
          const campoTexto = await client.$("~campoTexto");
          await campoTexto.setValue("Hello, Appium!");

          await client.deleteSession();
        }

        main();
        """)
    
    # Adicionar script de teste ao package.json
    with open("package.json", "r+") as f:
        content = f.read()
        content = content.replace('"test": "echo \\"Error: no test specified\\" && exit 1"', '"test": "node test.js"')
        f.seek(0)
        f.write(content)
        f.truncate()
    
    console.print(f"[bold green]Projeto criado em: {os.getcwd()}[/bold green]")
    return os.getcwd()  # Retorna o caminho do projeto

# Função para abrir o IntelliJ IDEA
def open_intellij(project_path):
    console.print("[bold]Verificando a instalação do IntelliJ IDEA...[/bold]")
    if os.path.exists("/Applications/IntelliJ IDEA.app"):
        console.print("[bold]Abrindo o projeto no IntelliJ IDEA...[/bold]")
        subprocess.run(["open", "-a", "IntelliJ IDEA", project_path], check=True)
    else:
        console.print("[bold red]IntelliJ IDEA não está instalado.[/bold red]")
        console.print("[bold]Por favor, baixe e instale a versão mais recente em: https://www.jetbrains.com/idea/download/[/bold]")
        subprocess.run(["open", "https://www.jetbrains.com/idea/download/"], check=True)

# Função principal
def main():
    console.print("[bold blue]Bem-vindo QA ao seu ASSISTENTE DE CONFIGURAÇÃO DE AUTOMAÇÃO MOBILE com Appium![/bold blue]")
    
    # Configurar ambiente
    setup_environment()
    
    # Criar projeto básico
    project_path = create_project()
    
    # Exibir dashboard final
    table = Table(title="Status da Configuração")
    table.add_column("Ferramenta", justify="right", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")

    table.add_row("Homebrew", "✅ Instalado")
    table.add_row("Xcode Command Line Tools", "✅ Instalado")
    table.add_row("Node.js", "✅ Instalado")
    table.add_row("Appium", "✅ Instalado")
    table.add_row("Appium Doctor", "✅ Instalado")
    table.add_row("Java JDK", "✅ Instalado")

    console.print(table)
    console.print("[bold green]QA Seu ambiente está pronto para automação com Appium![/bold green]")
    console.print("[bold green]Projeto básico criado e configurado com sucesso! Agora você esta livre para codar a vontade![/bold green]")
    
    # Abrir o projeto no IntelliJ IDEA
    open_intellij(project_path)

if __name__ == "__main__":
    main()
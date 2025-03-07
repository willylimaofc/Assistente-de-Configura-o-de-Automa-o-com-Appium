# Assistente-de-Configura-o-de-Automa-o-com-Appium
Criacao de um script de assistencia de Configuração de automação com Appium e montagem de primeiro projeto para QAs.

Sua intensao é facilitar uma rapida preparaçao de ambiente para testes automatizados. Dentro das ferramentas instaladas e configuradas temos:

# Ferramenta               

- Homebrew
- Xcode Command Line Tools
- Node.js
- Appium
- Appium Doctor
- Java JDK

Após todo o processo de configuracao e instalacao o script cria um projeto base dentro da pasta onde o arquivo do script esta alocado, facilitando para o QA o start de suas atividades.

# Como Executar o Script:

Salve o código acima em um arquivo chamado setup_appium.py.

No terminal, navegue até a pasta onde o arquivo está salvo.

Execute o script:

     python3 setup_appium.py

# Se o Python não estiver instalado, siga estas etapas e repita o comando do script:

# No macOS:
Instale o Homebrew (gerenciador de pacotes para macOS):

     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale o Python via Homebrew:

     brew install python


# Após a execução:

Se o script instalar o Homebrew, ele vai pedir que você recarregue o shell com o comando:

     source ~/.zshrc

Execute o comando acima ou reinicie o terminal.


# Ao finalizar a instalação será possivel analisar o seguinte retorno via terminal.

Bem-vindo ao Assistente de Configuração de Automação com Appium!

Configurando ambiente...

     Criando projeto básico de automação...
     Projeto criado em: /caminho/do/projeto
     Instalando dependências...
     Dependências instaladas com sucesso!

# Ferramenta - Status 

- Homebrew ✅ Instalado
- Xcode Command Line Tools ✅ Instalado
- Node.js  ✅ Instalado
- Appium ✅ Instalado
- Appium Doctor ✅ Instalado
- Java JDK ✅ Instalado 

# Ao final sera possivel visualizar as seguintes mensagens: 

 Seu ambiente está pronto para automação com Appium!
 Projeto básico criado e configurado com sucesso!

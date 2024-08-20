# Reconhecimento-facial-2.0

Esta é uma atualização do projeto, na qual fiz modificações relacionadas à segurança, usabilidade, e outras melhorias.

**Alterações anteriores:**

- As imagens das pessoas eram armazenadas em uma pasta chamada "pessoas".
- O registro de login era salvo em um arquivo de texto chamado login.txt.
- Alguns avisos e mensagens estavam posicionados de forma inadequada.

**Alterações atuais:**

- Agora, as imagens são armazenadas em um banco de dados, na tabela "colaboradores", contendo as colunas: ID, Nome, CPF, Função e a imagem da face da pessoa.
- Os registros de login também são salvos no banco de dados, mas em uma tabela separada chamada "entradas", que inclui: ID, Nome, CPF, Função, Data e Hora de login.
- Avisos e mensagens foram reposicionados para locais mais adequados, melhorando a clareza.
  
**Observação:** Fiz outras mudanças, mas não lembro de todas no momento. 😅

Este sistema de controle de acesso utiliza reconhecimento facial e Arduino para automatizar ações como abrir portas. Com uma interface gráfica, ele permite cadastrar usuários com foto e função, reconhecê-los em tempo real e controlar dispositivos físicos, oferecendo uma solução prática e segura para gestão de acesso.

![menu](https://github.com/user-attachments/assets/3ce0dfb0-9014-457c-a6ae-a489f38ee946)

Este projeto foi desenvolvido no PyCharm, aproveitando seus recursos para organizar e integrar as diferentes partes do sistema de reconhecimento facial. A interface gráfica foi construída usando o Tkinter, e a funcionalidade de reconhecimento facial se baseia na biblioteca face_recognition, enquanto o Arduino foi utilizado para controle de LEDs e um servo motor. O PyCharm proporcionou um ambiente eficiente para codificação, teste e depuração.

![cadastro](https://github.com/user-attachments/assets/dd3d21ab-a650-480b-8bda-8eeb2de88e95)

Além disso, todas as bibliotecas e dependências necessárias foram listadas no arquivo requirements.txt. Isso inclui as bibliotecas para controle de câmera (opencv-python), manipulação de imagens (Pillow), comunicação com o Arduino (pyFirmata), e outras ferramentas essenciais para o funcionamento do projeto. Dessa forma, o setup do ambiente de desenvolvimento é simplificado, permitindo que outros desenvolvedores possam facilmente replicar o projeto em suas máquinas.

![2024-08-19](https://github.com/user-attachments/assets/6ecfe26d-06e1-4dce-8da5-ddb52fd79491)

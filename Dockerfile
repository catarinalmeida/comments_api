# imagem python
FROM python:3.8-slim

# Defina o diretório de trabalho <C:\Users\catar\Desktop\comments_api\catarina_almeida> no contêiner
WORKDIR /app

# Copiar os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt requirements.txt

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# porta que a aplicação usará
EXPOSE 5000

# Definir o comando para executar a aplicação
CMD ["python", "run.py"]

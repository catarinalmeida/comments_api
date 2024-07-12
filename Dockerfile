# Use a imagem oficial do Python como imagem base
FROM python:3.8-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o restante do código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que a aplicação usará
EXPOSE 5000

# Defina o comando para executar a aplicação
CMD ["python", "run.py"]

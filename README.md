# SubTakeOver2 – Subdomain Takeover Hunter

SubTakeOver2 é uma ferramenta em Python para detecção de possíveis Subdomain Takeovers através da enumeração e análise de registros CNAME.
O script utiliza consultas DNS para identificar subdomínios que apontam para serviços externos potencialmente vulneráveis.

Ideal para estudantes, pentesters e analistas de segurança que desejam automatizar a análise de subdomínios.

Funcionalidades

✔ Enumeração de subdomínios usando wordlist

✔ Resolução de registros CNAME

✔ Deteção automática de padrões de takeover

✔ Relatórios diretos no terminal

✔ Código limpo, estruturado e fácil de manter

✔ Utiliza DNS de forma rápida e eficiente (dnspython)


Requisitos

> Instale as dependências executando:

`pip install -r requirements.txt`

Caso não consiga rodar o comando acima, use:

`python -m venv venv`

E depois:

`source venv/bin/activate`

Após isso, tente novamente o `pip install -r requirements.txt`

# Execute o script

`python3 SubTakeOver2.py -d <site> -w <wordlist.txt>`

# Exemplo de Execução

`python3 SubTakeOver2.py -d businesscorp.com.br -w namelist.txt`


> Saída simplificada:

    `
    [OK] ftp.businesscorp.com.br →  businesscorp.github.io
    
    [!] POSSÍVEL TAKEOVER ENCONTRADO!

    Subdomínio: admin.businesscorp.com.br
    
    CNAME: key.vlab.takeover...
    
    Status: Key encontrada!
    
    `

# Padrões Detectados

- O script identifica takeovers em serviços comuns, como:

- GitHub Pages (github.io)

- Amazon S3 (amazonaws.com)

- Heroku (herokuapp.com)

- Azure (azurewebsites.net)

- CloudFront (cloudfront.net)

- Fastly (fastly.net)

- Outros padrões que você pode adicionar facilmente

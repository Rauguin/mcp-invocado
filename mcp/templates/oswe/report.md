---
title: "OffSec Web Expert Exam Report"
subtitle: "name@email.com"
author: "OSID: 999999999"
subject: "OSWE Exam"
keywords: [OSWE, OffSec, exam]
lang: "en"
titlepage-logo: "offsec.png"
logo-width: "4cm"
titlepage: true
titlepage-color: "FFFFFF"
titlepage-text-color: "000000"
titlepage-rule-color: "000000"
titlepage-rule-height: 2
scrreprt: true
classoption: oneside
code-block-font-size: \scriptsize
---

\newpage

# Introduction

The OffSec Web Expert exam report contains all efforts that were conducted in order to pass the OffSec Web Expert exam. This report will be graded from a standpoint of correctness and fullness to all aspects of the exam. 

The purpose of this report is to ensure that the student has the technical knowledge required to pass the qualifications for the OffSec Web Expert certification.

## Summary

Para inicio do exame foram apresentados 5 hosts distintos, sendo um deles para teste interno, alem de 2 alvos para analise, ambos com um clone para debug.

Todas as maquinas Debug tiveram suas credencias de acesso passadas.
O host de teste interno possuia uma latencia muito menor, sendo orientado o seu uso ao termino de construcao do script de exploracao, como validação final.
The specific IP addresses were:

**Exam Network**

- 192.168.0.1 - Kali linux for final test;
- 192.168.0.2 - ABCD Web Server;
- 192.168.0.3 - Debug ABCD Web Server;
- 192.168.0.4 - EFGH Web Server;
- 192.168.0.5 - Debug EFGH Web Server;

## Recommendations

Os scripts finais foram construidos na linguagem python. Deve ser observado o uso de versao python3.12 ou superior, alem de importacao das bibliotecas necessarias para a correta execução. Os scripts foram construidos e executados em SO Kali Linux 2025/4.
Para uso correto dos scripts, faca a leitura da documentacao com o comando "python3 script.py --help".

O script "scritpABCD.py" solicitara a abertura de um listener para recepcao de uma shell reversa. Sugere-se o uso do comando "nc -lnvp 4444" para isso, antes de iniciar o script. O tempo medio de execucao do script esta entre 15 e 20 minutos.

O script "scriptEFGH.py" faz manuseio de um servidor web interno, utilizando uma porta dinamica conforme argumento passado. Orienta-se que, caso use uma porta que necessite de permissoes administrativas, execute o script com as permissoes necessarias. O tempo medio de execucao do script esta entre 5 e 10 minutos.

\newpage

# Methodologies

Como metodologia de realização desse exame, foi feito uma investigação estilo Black-Box, para melhor entender o funcionamento da aplicação pelo lado do cliente. Após isso, já bem definido onde são os possivei pontos vulnerárveis no serviço web, nos debruçamos sobre o código fonte, para melhor entender o serviço do lado do servidor, assim como funciona o fluxograma de ações encadeadas pelo cliente durante nossa interação. Tal metodologia é conhecida como "Top-Down"

Após iniciar analise do código fonte, caso tenha sido encontrado alguma função não observada no momento do teste do lado do cliente, voltamos a aplicação para verificar como ela funciona de fato, caracterizando a metodologia "Bottom-Up".

A utilização desse workflow torna-se cíclico, não sendo amarrado em apenas um tipo. Tal situação pode-ser tipificada como Hybrid Top-down.

Toda análise de código fonte foi feita nos hosts "Debug".

Para análise do host "ABCD", foi utilizado a ferramenta "jd-gui", ja presente no host debug. O acesso foi feito utilizando o protocolo RDP.



Para análise do host "EFGH", foi utilizada a ferramenta "VS-Code", implantando no host debug. O acesso foi feito utilizando os protocolos SSh(Analise do banco de dados) e HTTP(VS Code).



\newpage

# Web Applications

## Screenshot from Exam Painel with Local.txt and Proof.txt



## Target - ABCD Web Server

### Local.txt / Proof.txt

Segue abaixo as strings de cada arquivo solicitado:
- Local.txt - 2XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX6 
- Proof.txt - dXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXe

### Vulnerabilidade 1 - NOME DA VULNERABILIDADE

Vulnerabilidade classificada na CWE-2XXXX84.
Verificado no momento em que.......



### Vulnerabilidade 2 - NOME DA VULNERABILIDADE

Vulnerabilidade classificada na CWE-2XXXX84.
Verificado no momento em que.......



### Steps

Com base na metodologia Top-down, foi iniciado a exploracao do alvo a partir da pagina web, avaliando funcoes nao autenticadas, area de login, criacao de usuario, recuperacao de senha e funcoes com usuario nao autenticado.



Verificando especificamente a funcao boraBILL, vemos que ela faz download usando Files.readAllBytes.



### PoC Code

Segue abaixo as fases executas pelo script.

- Fase 01, AAAAAAAAAAAAAAA.

- Fase 02, BBBBBBBBBBBBBBB.

Segue abaixo o script de exploracao completa da aplicação:

```python
#!/usr/bin/env python3

print("Hello Avocado!")
```
### Screenshots

Segue abaixo o screenshot do retorno do script.



Segue abaixo o screenshot de captura da Local.txt



Segue abaixo o screenshot de captura da Proof.txt



\newpage

## Target - EFGH Web Server

### Local.txt / Proof.txt

Segue abaixo as strings de cada arquivo solicitado:
- Local.txt - 2XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX6 
- Proof.txt - dXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXe

### Vulnerabilidade 1 - NOME DA VULNERABILIDADE

Vulnerabilidade classificada na CWE-2XXXX84.
Verificado no momento em que.......



### Vulnerabilidade 2 - NOME DA VULNERABILIDADE

Vulnerabilidade classificada na CWE-2XXXX84.
Verificado no momento em que.......



### Steps

Com base na metodologia Top-down, foi iniciado a exploracao do alvo a partir da pagina web, avaliando funcoes nao autenticadas, area de login, criacao de usuario, recuperacao de senha e funcoes com usuario nao autenticado.



Verificando especificamente a funcao boraBILL, vemos que ela faz download usando Files.readAllBytes.



### PoC Code

Segue abaixo as fases executas pelo script.

- Fase 01, AAAAAAAAAAAAAAA.

- Fase 02, BBBBBBBBBBBBBBB.

Segue abaixo o script de exploracao completa da aplicação:

```python
#!/usr/bin/env python3

print("Hello Avocado!")
```
### Screenshots

Segue abaixo o screenshot do retorno do script.



Segue abaixo o screenshot de captura da Local.txt



Segue abaixo o screenshot de captura da Proof.txt



### Additional Items Not Mentioned in the Report

Foi verificado tambem AAAAAAAAAAAAAA. 
# 💰 Dashboard Financeiro

Dashboard interativo para gestão pessoal de despesas, desenvolvido com Python e Streamlit.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Adicione um screenshot ou GIF aqui -->
<!-- ![Dashboard Preview](assets/screenshot.png) -->

---

## 📋 Sobre o Projeto

Aplicação web para controle financeiro pessoal que permite registrar receitas e despesas, visualizar a distribuição dos gastos e acompanhar a evolução mensal das finanças.

### Funcionalidades

- **Registro de gastos** — cadastro de despesas fixas e variáveis por mês
- **Resumo mensal** — visualização do saldo, total de gastos e percentual do salário comprometido
- **Gráficos interativos** — distribuição por tipo (pizza) e evolução mensal (linha)
- **Resumo anual** — visão consolidada de todos os meses
- **Backup e restauração** — exportação e importação de dados via CSV
- **Alertas visuais** — indicadores de gastos controlados, altos ou excedentes

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dashboard-financeiro.git
cd dashboard-financeiro
```

2. Crie e ative o ambiente virtual:
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
streamlit run app.py
```

5. Acesse no navegador: `http://localhost:8501`

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **Python** | Linguagem principal |
| **Streamlit** | Interface web interativa |
| **Pandas** | Manipulação de dados |
| **Plotly Express** | Gráficos interativos |
| **Matplotlib** | Visualizações auxiliares |

---

## 📁 Estrutura do Projeto

```
dashboard-financeiro/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
├── .gitignore          # Arquivos ignorados pelo Git
├── LICENSE             # Licença MIT
└── README.md           # Documentação
```

---

## 📸 Screenshots


### Tela Principal
![Tela Principal](https://private-user-images.githubusercontent.com/228616224/542516948-a19ad462-9774-4a8a-9081-8ce0ee14c3a3.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njk3MzU4NjksIm5iZiI6MTc2OTczNTU2OSwicGF0aCI6Ii8yMjg2MTYyMjQvNTQyNTE2OTQ4LWExOWFkNDYyLTk3NzQtNGE4YS05MDgxLThjZTBlZTE0YzNhMy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTMwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEzMFQwMTEyNDlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zN2Q5ZmZmMDg2ZDIyNGIyZTAzN2Q1N2Q2MzI5Mjk1NTY5OWJkNjIwZGI0NzkyMzQyYzA2NmYxZDY3MDk4MDZiJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.MIEVu5sc1S96PxMmuUGLTpCLNHLyZ_dxYeFuuQ8GQWU)

### Gráficos
![Gráficos](https://private-user-images.githubusercontent.com/228616224/542516946-73463924-840b-4a35-a752-387e02a183e5.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njk3MzU5ODYsIm5iZiI6MTc2OTczNTY4NiwicGF0aCI6Ii8yMjg2MTYyMjQvNTQyNTE2OTQ2LTczNDYzOTI0LTg0MGItNGEzNS1hNzUyLTM4N2UwMmExODNlNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTMwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEzMFQwMTE0NDZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jZjFjZjgwMjcwYWM2NDIyNDlhYTc5MzVkOWYzMzYxMDE5OThlZjFhMjRkMmVmM2M0YTkwNGRlMDgyOGU2ZTJkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.yXa1uMe3h-z2gRFOlIqsvwHjO68dL4cCdQTQVNlIYrY)

### Resumo
![Resumo](https://private-user-images.githubusercontent.com/228616224/542516947-f9c8c0d0-5aa2-4c9d-bdde-f080264fdf05.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njk3MzYxOTEsIm5iZiI6MTc2OTczNTg5MSwicGF0aCI6Ii8yMjg2MTYyMjQvNTQyNTE2OTQ3LWY5YzhjMGQwLTVhYTItNGM5ZC1iZGRlLWYwODAyNjRmZGYwNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTMwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEzMFQwMTE4MTFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05NDUwNTBhY2U3YmQ4NTIzMzhkYzQ2NjQ1YjE3YWQ0MWQzMTQzZGQ1MWZlNTlkMDY0NWFlY2I0ZjAzZDViYjE4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Yq-2alOaDSk2bEBVp-sjEaQ0iMoX-Sa5tvRC9AMAs6g)




---

## 🔮 Melhorias Futuras

- [ ] Autenticação de usuários
- [ ] Persistência em banco de dados
- [ ] Categorização personalizada de gastos
- [ ] Metas de economia por mês
- [ ] Relatórios em PDF
- [ ] Deploy na nuvem (Streamlit Cloud)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

Desenvolvido por **Francisco**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)]([https://linkedin.com/in/seu-perfil](https://www.linkedin.com/in/fabio-soares-ba9240218/))
[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)]([https://github.com/seu-usuario](https://github.com/fabimsoares16-bit))

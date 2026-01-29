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

<!-- Descomente e adicione suas imagens -->
<!--
 Tela Principal
![Captura de tela 2026-01-28 222846.png)

### Gráficos
![Gráficos](assets/graficos.png)
-->

*Em breve*

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

Desenvolvido por **Fabio**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/seu-usuario)

"""
Módulo de persistência com SQLite.

Gerencia o armazenamento de gastos, configurações (salário) e metas mensais.
"""

import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "financeiro.db")


def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão com o banco SQLite, criando as tabelas se necessário."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    _criar_tabelas(conn)
    return conn


def _criar_tabelas(conn: sqlite3.Connection) -> None:
    """Cria as tabelas do banco caso não existam."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL DEFAULT 'Outros',
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes TEXT NOT NULL UNIQUE,
            valor_meta REAL NOT NULL
        );
    """)
    conn.commit()


# --- Gastos ---

def adicionar_gasto(mes: str, tipo: str, categoria: str, descricao: str, valor: float) -> int:
    """Insere um gasto e retorna o ID gerado."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO gastos (mes, tipo, categoria, descricao, valor) VALUES (?, ?, ?, ?, ?)",
        (mes, tipo, categoria, descricao, valor)
    )
    conn.commit()
    gasto_id = cursor.lastrowid
    conn.close()
    return gasto_id


def remover_gasto(gasto_id: int) -> None:
    """Remove um gasto pelo ID."""
    conn = get_connection()
    conn.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
    conn.commit()
    conn.close()


def editar_gasto(gasto_id: int, tipo: str, categoria: str, descricao: str, valor: float) -> None:
    """Atualiza um gasto existente."""
    conn = get_connection()
    conn.execute(
        "UPDATE gastos SET tipo = ?, categoria = ?, descricao = ?, valor = ? WHERE id = ?",
        (tipo, categoria, descricao, valor, gasto_id)
    )
    conn.commit()
    conn.close()


def obter_gastos_mes(mes: str) -> list[dict]:
    """Retorna todos os gastos de um mês como lista de dicionários."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, mes, tipo, categoria, descricao, valor FROM gastos WHERE mes = ? ORDER BY criado_em",
        (mes,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obter_todos_gastos() -> list[dict]:
    """Retorna todos os gastos cadastrados."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, mes, tipo, categoria, descricao, valor FROM gastos ORDER BY criado_em"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def limpar_gastos() -> None:
    """Remove todos os gastos do banco."""
    conn = get_connection()
    conn.execute("DELETE FROM gastos")
    conn.commit()
    conn.close()


def importar_gastos(gastos: list[dict]) -> None:
    """Importa uma lista de gastos (usada na restauração de backup)."""
    conn = get_connection()
    conn.execute("DELETE FROM gastos")
    for g in gastos:
        categoria = g.get("categoria", "Outros")
        conn.execute(
            "INSERT INTO gastos (mes, tipo, categoria, descricao, valor) VALUES (?, ?, ?, ?, ?)",
            (g["mes"], g["tipo"], categoria, g["descricao"], g["valor"])
        )
    conn.commit()
    conn.close()


# --- Configurações ---

def salvar_configuracao(chave: str, valor: str) -> None:
    """Salva ou atualiza uma configuração."""
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)",
        (chave, valor)
    )
    conn.commit()
    conn.close()


def obter_configuracao(chave: str, padrao: str = "0") -> str:
    """Obtém o valor de uma configuração ou retorna o padrão."""
    conn = get_connection()
    row = conn.execute(
        "SELECT valor FROM configuracoes WHERE chave = ?", (chave,)
    ).fetchone()
    conn.close()
    return row["valor"] if row else padrao


# --- Metas ---

def salvar_meta(mes: str, valor_meta: float) -> None:
    """Define ou atualiza a meta de economia para um mês."""
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO metas (mes, valor_meta) VALUES (?, ?)",
        (mes, valor_meta)
    )
    conn.commit()
    conn.close()


def obter_meta(mes: str) -> Optional[float]:
    """Retorna a meta do mês ou None se não definida."""
    conn = get_connection()
    row = conn.execute(
        "SELECT valor_meta FROM metas WHERE mes = ?", (mes,)
    ).fetchone()
    conn.close()
    return row["valor_meta"] if row else None


def obter_todas_metas() -> dict[str, float]:
    """Retorna um dicionário {mês: valor_meta} com todas as metas."""
    conn = get_connection()
    rows = conn.execute("SELECT mes, valor_meta FROM metas").fetchall()
    conn.close()
    return {r["mes"]: r["valor_meta"] for r in rows}


def limpar_tudo() -> None:
    """Remove todos os dados (gastos, configurações e metas)."""
    conn = get_connection()
    conn.executescript("""
        DELETE FROM gastos;
        DELETE FROM configuracoes;
        DELETE FROM metas;
    """)
    conn.commit()
    conn.close()

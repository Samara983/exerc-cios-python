import json
import os
from datetime import datetime


class Logger:
    """Sistema de logs para registrar ações do usuário."""
    @staticmethod
    def log(msg):
        os.makedirs("data", exist_ok=True)
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("data/logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{data}] {msg}\n")


class Task:
    """Modelo de tarefa."""
    def __init__(self, descricao, prioridade="média"):
        self.descricao = descricao
        self.prioridade = prioridade
        self.criada_em = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.concluida = False

    def to_dict(self):
        return {
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "criada_em": self.criada_em,
            "concluida": self.concluida
        }


class TaskManager:
    """Gerenciador das tarefas, com persistência, busca e filtros."""
    def __init__(self, arquivo="data/tasks.json"):
        self.arquivo = arquivo
        os.makedirs("data", exist_ok=True)
        self.tasks = self.carregar()

    def carregar(self):
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def adicionar(self, descricao, prioridade):
        nova = Task(descricao, prioridade)
        self.tasks.append(nova.to_dict())
        self.salvar()
        Logger.log(f"Tarefa adicionada: {descricao} (Prioridade: {prioridade})")

    def listar(self):
        return self.tasks

    def concluir(self, indice):
        try:
            self.tasks[indice]["concluida"] = True
            self.salvar()
            Logger.log(f"Tarefa concluída: {self.tasks[indice]['descricao']}")
        except IndexError:
            raise ValueError("Índice inválido.")

    def buscar(self, termo):
        return [t for t in self.tasks if termo.lower() in t["descricao"].lower()]

    def filtrar_prioridade(self, prioridade):
        return [t for t in self.tasks if t["prioridade"] == prioridade]

    def gerar_relatorio(self):
        total = len(self.tasks)
        concluidas = sum(t["concluida"] for t in self.tasks)
        pendentes = total - concluidas

        Logger.log("Relatório gerado.")

        return {
            "total": total,
            "concluídas": concluidas,
            "pendentes": pendentes
        }


def mostrar_tarefas(lista):
    if not lista:
        print("\nNenhuma tarefa encontrada.")
        return
    for i, t in enumerate(lista):
        status = "✔️" if t["concluida"] else "❌"
        print(f"{i}. [{status}] {t['descricao']} | "
              f"Prioridade: {t['prioridade']} | "
              f"Criada em: {t['criada_em']}")


def menu():
    gestor = TaskManager()

    while True:
        print("\n=== GERENCIADOR INTELIGENTE DE TAREFAS ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Buscar tarefa")
        print("5 - Filtrar por prioridade")
        print("6 - Gerar relatório")
        print("7 - Sair")

        opc = input("Escolha: ")

        if opc == "1":
            desc = input("Descrição: ")
            prioridade = input("Prioridade (baixa/média/alta): ").lower()
            gestor.adicionar(desc, prioridade)
            print("Tarefa adicionada!")

        elif opc == "2":
            mostrar_tarefas(gestor.listar())

        elif opc == "3":
            try:
                indice = int(input("Índice: "))
                gestor.concluir(indice)
                print("Tarefa concluída!")
            except ValueError:
                print("Erro: índice inválido!")

        elif opc == "4":
            termo = input("Buscar por: ")
            resultados = gestor.buscar(termo)
            mostrar_tarefas(resultados)

        elif opc == "5":
            pr = input("Prioridade: ").lower()
            filtradas = gestor.filtrar_prioridade(pr)
            mostrar_tarefas(filtradas)

        elif opc == "6":
            rel = gestor.gerar_relatorio()
            print("\n=== RELATÓRIO ===")
            print(f"Total: {rel['total']}")
            print(f"Concluídas: {rel['concluídas']}")
            print(f"Pendentes: {rel['pendentes']}")

        elif opc == "7":
            print("Saindo... Até mais!")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()


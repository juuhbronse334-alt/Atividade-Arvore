
class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def altura(self, no):
        return no.altura if no else 0

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def atualizar_altura(self, no):
        no.altura = 1 + max(
            self.altura(no.esquerda),
            self.altura(no.direita)
        )

    def rotacao_direita(self, y):
        x = y.esquerda
        subarvore = x.direita

        x.direita = y
        y.esquerda = subarvore

        self.atualizar_altura(y)
        self.atualizar_altura(x)

        print("Rotação LL: rotação simples à direita")
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        subarvore = y.esquerda

        y.esquerda = x
        x.direita = subarvore

        self.atualizar_altura(x)
        self.atualizar_altura(y)

        print("Rotação RR: rotação simples à esquerda")
        return y

    def inserir(self, no, valor):
        if no is None:
            return No(valor)

        if valor < no.valor:
            no.esquerda = self.inserir(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self.inserir(no.direita, valor)
        else:
            print("Valor duplicado! Inserção cancelada.")
            return no

        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        # Caso LL
        if fb > 1 and valor < no.esquerda.valor:
            return self.rotacao_direita(no)

        # Caso RR
        if fb < -1 and valor > no.direita.valor:
            return self.rotacao_esquerda(no)

        # Caso LR
        if fb > 1 and valor > no.esquerda.valor:
            print("Rotação LR: dupla esquerda-direita")
            no.esquerda = self._rotacao_esquerda_silenciosa(
                no.esquerda
            )
            # Evita confundir a rotação interna com um
            # novo caso de balanceamento.
            return self._rotacao_direita_silenciosa(no)

        # Caso RL
        if fb < -1 and valor < no.direita.valor:
            print("Rotação RL: dupla direita-esquerda")
            no.direita = self._rotacao_direita_silenciosa(
                no.direita
            )
            return self._rotacao_esquerda_silenciosa(no)

        return no

    def _rotacao_direita_silenciosa(self, y):
        x = y.esquerda
        subarvore = x.direita
        x.direita = y
        y.esquerda = subarvore
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x

    def _rotacao_esquerda_silenciosa(self, x):
        y = x.direita
        subarvore = y.esquerda
        y.esquerda = x
        x.direita = subarvore
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y

    def menor_valor(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def remover(self, no, valor):
        if no is None:
            return None

        if valor < no.valor:
            no.esquerda = self.remover(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self.remover(no.direita, valor)
        else:
            # Nó sem filho ou com apenas um filho
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            # Nó com dois filhos: sucessor em ordem
            sucessor = self.menor_valor(no.direita)
            no.valor = sucessor.valor
            no.direita = self.remover(
                no.direita, sucessor.valor
            )

        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        # Rebalanceamento após remoção
        if fb > 1:
            if self.fator_balanceamento(no.esquerda) >= 0:
                return self.rotacao_direita(no)
            print("Rotação LR: dupla esquerda-direita")
            no.esquerda = self._rotacao_esquerda_silenciosa(
                no.esquerda
            )
            return self._rotacao_direita_silenciosa(no)

        if fb < -1:
            if self.fator_balanceamento(no.direita) <= 0:
                return self.rotacao_esquerda(no)
            print("Rotação RL: dupla direita-esquerda")
            no.direita = self._rotacao_direita_silenciosa(
                no.direita
            )
            return self._rotacao_esquerda_silenciosa(no)

        return no

    def buscar(self, no, valor):
        if no is None or no.valor == valor:
            return no

        if valor < no.valor:
            return self.buscar(no.esquerda, valor)

        return self.buscar(no.direita, valor)

    def pre_ordem(self, no):
        if no:
            print(no.valor, end=" ")
            self.pre_ordem(no.esquerda)
            self.pre_ordem(no.direita)

    def em_ordem(self, no):
        if no:
            self.em_ordem(no.esquerda)
            print(no.valor, end=" ")
            self.em_ordem(no.direita)

    def pos_ordem(self, no):
        if no:
            self.pos_ordem(no.esquerda)
            self.pos_ordem(no.direita)
            print(no.valor, end=" ")

    def exibir_detalhes(self, no):
        if no:
            self.exibir_detalhes(no.esquerda)
            print(
                f"Valor: {no.valor} | "
                f"Altura: {no.altura} | "
                f"Fator de balanceamento: "
                f"{self.fator_balanceamento(no)}"
            )
            self.exibir_detalhes(no.direita)

    def exibir_arvore(self, no, nivel=0, lado="Raiz"):
        if no:
            self.exibir_arvore(no.direita, nivel + 1, "D")
            print(
                "    " * nivel
                + f"{lado}: {no.valor} "
                + f"(h={no.altura}, "
                + f"FB={self.fator_balanceamento(no)})"
            )
            self.exibir_arvore(no.esquerda, nivel + 1, "E")


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def menu():
    arvore = ArvoreAVL()
    raiz = None

    while True:
        print("\n===== ÁRVORE AVL =====")
        print("1 - Inserir elemento")
        print("2 - Remover elemento")
        print("3 - Buscar elemento")
        print("4 - Percursos")
        print("5 - Exibir alturas e fatores")
        print("6 - Visualizar árvore")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            valor = ler_inteiro("Valor para inserir: ")
            raiz = arvore.inserir(raiz, valor)

        elif opcao == "2":
            valor = ler_inteiro("Valor para remover: ")
            if arvore.buscar(raiz, valor) is None:
                print("Valor não encontrado na árvore.")
            else:
                raiz = arvore.remover(raiz, valor)
                print("Remoção realizada.")

        elif opcao == "3":
            valor = ler_inteiro("Valor para buscar: ")
            if arvore.buscar(raiz, valor):
                print(f"O valor {valor} está na árvore.")
            else:
                print(f"O valor {valor} não está na árvore.")

        elif opcao == "4":
            if raiz is None:
                print("Árvore vazia.")
                continue

            print("Pré-ordem: ", end="")
            arvore.pre_ordem(raiz)
            print()

            print("Em ordem: ", end="")
            arvore.em_ordem(raiz)
            print()

            print("Pós-ordem: ", end="")
            arvore.pos_ordem(raiz)
            print()

        elif opcao == "5":
            if raiz is None:
                print("Árvore vazia.")
            else:
                print(f"Altura da árvore: {raiz.altura}")
                arvore.exibir_detalhes(raiz)

        elif opcao == "6":
            if raiz is None:
                print("Árvore vazia.")
            else:
                arvore.exibir_arvore(raiz)

        elif opcao == "0":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()

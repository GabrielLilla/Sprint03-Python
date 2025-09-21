# Sprint de Python (Estruturas & Algoritmos)

> **Objetivo:** demonstrar, com dados simulados, como **fila**, **pilha**, **buscas** e **ordenações** apoiam as prioridades operacionais do ValiChain (rastreabilidade, FEFO, reposição).

---

## O que cada estrutura/algoritmo faz no contexto

### 1) Modelo de domínio — `@dataclass Insumo`
- **O que é:** estrutura **imutável** (`frozen=True`) com `insumo`, `quantidade`, `exame`, `validade`.
- **Para quê:** padroniza o “registro do insumo” que circula por todas as operações (fila, pilha, buscas e ordenações). Mantém consistência e facilita **rastreabilidade**.

### 2) Simulação de dados — `gerar_lote_insumos(...)`
- **O que é:** gera uma **lista de `Insumo`** com quantidades e validades aleatórias.
- **Para quê:** testar rapidamente cenários reais (estoques e prazos de validade) sem BD. Base para demonstrar **priorizações** (ex.: menor quantidade, validade mais próxima).

### 3) Fila de consumo — `class FilaConsumo`
- **Como funciona:** usa `collections.deque` para enfileirar **`(timestamp, Insumo)`** via `registrar_consumo`.
- **Para quê:** registra o **histórico cronológico** de consumos. Dá visibilidade temporal (“o que saiu e quando”) — essencial para **auditoria** e previsão de picos.

### 4) Pilha de consultas — `class PilhaConsultas`
- **Como funciona:** lista usada como **pilha (LIFO)**, empilhando **`(timestamp, Insumo)`** em `consultar`.
- **Para quê:** mantém atalho aos **itens mais recentemente consultados**, acelerando reconsultas recorrentes no turno (insumos “em evidência”).

### 5) Buscas
**a) Sequencial —** `busca_sequencial(lista, nome)`  
- **Como funciona:** percorre a lista bruta e compara nomes (**case-insensitive**).  
- **Para quê:** solução simples quando a lista **não está ordenada** ou é pequena; consultas diretas sem preparação.

**b) Binária —** `busca_binaria(lista_ordenada, nome)`  
- **Como funciona:** procura por nome em **O(log n)**; exige **lista pré-ordenada** (no código, por `insumo`).  
- **Para quê:** desempenho em catálogos maiores/muitas consultas; mantém **tempo previsível**.  
- **Obs.:** a ordenação prévia é feita com `merge_sort(..., key=lambda x: x.insumo.lower())`.

### 6) Ordenações (priorização operacional)
**a) Merge Sort —** `merge_sort(lista, key=...)` **por quantidade**  
- **Como funciona:** algoritmo **estável** que retorna nova lista ordenada pela chave.  
- **Para quê:** ranking de **menor → maior estoque** (“Top 5 menores quantidades”), priorizando **reposição**.

**b) Quick Sort —** `quick_sort(lista, key=...)` **por validade**  
- **Como funciona:** particiona por pivô e retorna nova lista ordenada pela chave.  
- **Para quê:** ranking das **validades mais próximas** (“Top 5 validades”), aplicando **FEFO** (evita perdas).

### 7) Utilitário de exibição — `_print_insumo(...)`
- **Como funciona:** formata cada `Insumo` com alinhamento e data de validade legível.
- **Para quê:** melhora a leitura operacional no console (identificação rápida de item, quantidade, exame, validade).

### 8) Encadeamento da demonstração — `demo()` e `main()`
**`demo()` executa o fluxo completo:**
1. **Gera dados** → mostra amostra.  
2. **Registra consumos** na fila → exibe histórico.  
3. **Registra consultas** na pilha → exibe últimos consultados.  
4. **Busca** sequencial e **binária** sobre o mesmo alvo (com **ordenação prévia** para a binária).  
5. **Ordena por quantidade (Merge)** e por **validade (Quick)** → exibe **Top 5** de cada (reposição e vencimentos).

**`main()`**: pequeno **menu** para acionar a demo no terminal (fluxo simples para rodar no VS Code).

---

## 🧭 Resumo funcional
- **Fila** → histórico cronológico do consumo (**rastreabilidade**).  
- **Pilha** → acesso rápido aos itens mais consultados (**agilidade**).  
- **Busca sequencial** → consulta simples em lista bruta.  
- **Busca binária** (com ordenação por nome) → consulta **eficiente** para listas maiores.  
- **Merge Sort por quantidade** → prioriza **reposição** (menores estoques primeiro).  
- **Quick Sort por validade** → prioriza **uso/transferência** (**vencimentos** mais próximos / FEFO).

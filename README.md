# 🏙️ Análise Espacial: Transporte e Economia em Belo Horizonte

## 📊 Sobre o Projeto

Análise da relação entre infraestrutura de transporte público e desenvolvimento econômico nos bairros de Belo Horizonte, utilizando dados geoespaciais e técnicas de análise espacial para identificar áreas prioritárias para investimento em políticas públicas.

---

## 🎯 Objetivos

- Mapear a distribuição espacial de empresas e pontos de ônibus
- Calcular correlação entre densidade de transporte e densidade econômica
- Identificar perfil empreendedor por região (análise de MEIs)
- Classificar bairros por nível de desenvolvimento (Matriz 2x2)
- Priorizar áreas para investimento em mobilidade urbana

---
## 📈 Principais Resultados

### Correlação Transporte × Economia
- **Coeficiente de Pearson:** 0.505 (correlação moderada e positiva)
- **Conclusão:** Bairros com mais transporte público TENDEM a ter mais empresas

### Perfil Empreendedor
- **62.7%** das empresas são MEIs (Microempreendedores Individuais)
- **270.788** microempreendedores ativos em BH
- BH é uma cidade **altamente empreendedora**

### Classificação de Bairros
- **64 bairros** identificados como OPORTUNIDADES prioritárias de investimento
- **96 bairros** em situação de PRIORIDADE máxima

### Taxa de Sucesso Geoespacial
- **99.6%** das empresas geolocalizadas com sucesso
- **97.4%** dos pontos de transporte geolocalizados

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12** - Linguagem principal
- **Pandas** - Manipulação de dados tabulares
- **GeoPandas** - Análise espacial e operações geográficas
- **Shapely** - Manipulação de geometrias
- **Folium** - Mapas interativos HTML
- **Plotly** - Visualizações interativas
- **Streamlit** - Dashboard executivo web
- **Matplotlib** - Gráficos estatísticos
- **NumPy** - Operações numéricas

---
## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter Python 3.8+ instalado.

### Instalação

## Clone o repositório:

```bash
git clone https://github.com/seu-usuario/projeto-bh-transporte-economia.git
cd projeto-bh-transporte-economia
```
## Instale as dependências:
```bash
pip install pandas geopandas folium plotly streamlit matplotlib numpy shapely
```
## Execute o dashboard
```bash
streamlit run app_dashboard.py
``` 

## Execute o notebook
```bash
jupyter notebook
```

## 🗺️ Mapas Interativos

Os mapas HTML estão na pasta `mapas_exportados/`:

- **mapa_classificacao_bairros.html** - Matriz 2x2 (4 categorias)
- **mapa_densidade_economica.html** - Gradiente de densidade

Para visualizar, abra os arquivos HTML no navegador.

---

## 🎯 Classificação de Bairros (Matriz 2x2)

| Categoria | Quantidade | % | Características | Ação |
|-----------|------------|---|-----------------|------|
| 🟢 Bem Desenvolvido | 96 | 30% | Alta economia + Alto transporte | Manter políticas |
| 🟡 Oportunidade | 64 | 20% | Alta economia + Baixo transporte | INVESTIR ⭐ |
| 🟠 Potencial | 64 | 20% | Baixa economia + Alto transporte | Incentivar economia |
| 🔴 Prioridade | 96 | 30% | Baixa economia + Baixo transporte | Ação urgente |

---
## 💡 Principais Insights

1. **Relação Positiva** - Bairros com melhor infraestrutura de transporte apresentam maior densidade econômica (r=0.505)

2. **BH Empreendedora** - 62.7% de MEIs, forte cultura empreendedora (alguns bairros com até 96% MEIs)

3. **Oportunidades Identificadas** - 64 bairros com alta economia mas transporte insuficiente

4. **Setores Predominantes**:
   - Serviços de beleza: 21.976 estabelecimentos
   - Condomínios prediais: 21.748 estabelecimentos
   - Promoção de vendas: 18.036 estabelecimentos

---

## 🏆 Top 5 Bairros "Oportunidade"

1. **Buritis** - 6.855 empresas (densidade: 2.332/km²)
2. **Castelo** - 6.653 empresas (densidade: 2.765/km²)
3. **Santa Lúcia** - 4.281 empresas (densidade: 1.808/km²)
4. **Lindéia** - 3.995 empresas (densidade: 1.975/km²)
5. **Sagrada Família** - 3.988 empresas (densidade: 3.087/km²)

---
## 📊 Metodologia

### Análise Espacial (Spatial Join)
Operações geoespaciais para associar pontos (empresas/ônibus) a polígonos (bairros) usando coordenadas geográficas reais.

### Métricas Calculadas
- **Densidade Econômica:** empresas por km²
- **Densidade de Transporte:** pontos de ônibus por km²
- **Percentual de MEIs:** proporção de microempreendedores

### Classificação por Matriz 2x2
Bairros classificados pela mediana de densidade econômica e transporte, gerando 4 categorias.

---

## 📁 Fontes de Dados

- **Bairros Oficiais:** 322 bairros de Belo Horizonte
- **Atividades Econômicas:** 512.952 estabelecimentos
- **Pontos de Ônibus:** 47.815 pontos

**Origem:** https://dados.pbh.gov.br/

---


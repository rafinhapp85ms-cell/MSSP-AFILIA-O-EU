import os
import json

def detectar_e_analisar_erros_persistencia():
    """
    Detecta e analisa erros de persistência nos arquivos críticos da MSSP.
    Retorna um dicionário com o relatório completo de cada arquivo.
    NÃO modifica, apaga ou sobrescreve nenhum arquivo.
    """
    arquivos_criticos = {
        "dados_postar.json": "Redes sociais e configurações de postagem",
        "state.json": "Estado interno do sistema (módulos, automação, logs)",
        "historico_afiliacao.json": "Histórico de análises e anúncios gerados",
        "colaboradores.json": "Acessos temporários de colaboradores"
    }
    
    relatorio = {}
    
    for arquivo, impacto in arquivos_criticos.items():
        # Inicializa resultado para este arquivo
        resultado = {
            "arquivo": arquivo,
            "status": "ok",
            "gravidade": "nenhum",
            "impacto": impacto,
            "detalhes": ""
        }
        
        # PASSO 1: Verificar se o arquivo existe
        if not os.path.exists(arquivo):
            resultado["status"] = "ausente"
            resultado["gravidade"] = "critico"
            resultado["detalhes"] = "Arquivo não encontrado no diretório da aplicação."
            relatorio[arquivo] = resultado
            continue
        
        # PASSO 2: Tentar carregar o JSON
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
        except json.JSONDecodeError:
            resultado["status"] = "corrompido"
            resultado["gravidade"] = "irreversivel"
            resultado["detalhes"] = "Arquivo existe, mas contém JSON inválido (sintaxe quebrada)."
            relatorio[arquivo] = resultado
            continue
        except Exception as e:
            resultado["status"] = "erro_leitura"
            resultado["gravidade"] = "critico"
            resultado["detalhes"] = f"Falha ao ler o arquivo: {str(e)}"
            relatorio[arquivo] = resultado
            continue
        
        # PASSO 3: Verificar se o conteúdo é utilizável
        if conteudo is None:
            resultado["status"] = "vazio"
            resultado["gravidade"] = "recuperavel"
            resultado["detalhes"] = "Arquivo existe, mas está vazio ou nulo."
            relatorio[arquivo] = resultado
            continue
        
        if isinstance(conteudo, dict) and len(conteudo) == 0:
            resultado["status"] = "vazio"
            resultado["gravidade"] = "recuperavel"
            resultado["detalhes"] = "Arquivo existe, mas contém um objeto vazio {}."
            relatorio[arquivo] = resultado
            continue
        
        if isinstance(conteudo, list) and len(conteudo) == 0:
            resultado["status"] = "vazio"
            resultado["gravidade"] = "recuperavel"
            resultado["detalhes"] = "Arquivo existe, mas contém uma lista vazia []."
            relatorio[arquivo] = resultado
            continue
        
        # PASSO 4: Verificar estrutura mínima esperada (baseado no contexto da MSSP)
        estrutura_valida = True
        detalhes_estrutura = ""
        
        if arquivo == "dados_postar.json":
            if not isinstance(conteudo, dict) or "redes" not in conteudo:
                estrutura_valida = False
                detalhes_estrutura = "Estrutura inválida: falta a chave 'redes'."
        elif arquivo == "state.json":
            if not isinstance(conteudo, dict) or "modulos" not in conteudo:
                estrutura_valida = False
                detalhes_estrutura = "Estrutura inválida: falta a chave 'modulos'."
        elif arquivo == "historico_afiliacao.json":
            if not isinstance(conteudo, list):
                estrutura_valida = False
                detalhes_estrutura = "Estrutura inválida: deve ser uma lista de registros."
        elif arquivo == "colaboradores.json":
            if not isinstance(conteudo, list):
                estrutura_valida = False
                detalhes_estrutura = "Estrutura inválida: deve ser uma lista de colaboradores."
        
        if not estrutura_valida:
            resultado["status"] = "estrutura_invalida"
            resultado["gravidade"] = "critico"
            resultado["detalhes"] = detalhes_estrutura
            relatorio[arquivo] = resultado
            continue
        
        # Se chegou até aqui, o arquivo está OK
        relatorio[arquivo] = resultado
    
    return relatorio

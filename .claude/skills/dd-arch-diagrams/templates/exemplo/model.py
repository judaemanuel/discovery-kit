# -*- coding: utf-8 -*-
"""EXEMPLO GENÉRICO — Plataforma de Assinaturas (SaaS, cobrança recorrente).

Todo o conteúdo é fictício. Serve de modelo para o gerador dd-arch-diagrams:
copie esta pasta (model.py + views.py), troque as entidades/relações/ADRs/fluxos e ajuste as coordenadas em views.py.
"""

STATUS = {
    'novo':      dict(label='Novo (a construir)',                       fill='#DCE8FF', stroke='#2563EB', dash=False),
    'reuso':     dict(label='Reaproveita padrão/serviço (a validar)',   fill='#FFF0C9', stroke='#B45309', dash=True),
    'existente': dict(label='Existente na organização',                 fill='#EEF1F5', stroke='#64748B', dash=False),
    'pessoa':    dict(label='Pessoa / papel',                           fill='#0F2A4A', stroke='#0F2A4A', dash=False),
}

E = {}
def ent(id, kind, name, tech='', desc='', status='novo', parent=None, adr=(), open=(), refs=()):
    """kind: person | ext | system | container | db | bus | component. status: novo | reuso | existente | pessoa."""
    E[id] = dict(id=id, kind=kind, name=name, tech=tech, desc=desc, status=status, parent=parent,
                 adr=list(adr), open=list(open), refs=list(refs))

# ---------- pessoas ----------
ent('assinante','person','Assinante',desc='Contrata, altera e cancela planos; acompanha faturas',status='pessoa')
ent('convidado','person','Usuário convidado',desc='Usa o serviço sob a assinatura de outra pessoa',status='pessoa')
ent('parceiro','person','Parceiro / Revendedor',desc='Vende planos e gerencia a carteira de clientes',status='pessoa')
ent('analista','person','Analista de Cobrança',desc='Trata exceções de cobrança e autoriza ajustes',status='pessoa')
ent('suporte','person','Suporte ao Cliente',desc='Consulta o histórico de faturas e executa alterações de plano',status='pessoa',
    open=['Suporte não tem acesso ao CRM de cobrança hoje — como executar alterações de plano?'])
ent('financeiro','person','Financeiro / Fiscal',desc='Valida regras de preço, concilia recebimentos e emite relatórios fiscais',status='pessoa',
    open=['Ainda não participou das sessões de levantamento'])

# ---------- sistemas externos ----------
ent('app_cli','ext','App e Site do Assinante','Mobile / Web (existente)','Autosserviço de contratação e acompanhamento',status='existente',
    open=['Canal de contratação por parceiro ainda indefinido'])
ent('portal_par','ext','Portal do Parceiro','Web (existente)','Canal de venda dos parceiros. Fora do 1º ciclo (a confirmar)',status='existente',
    open=['Sem API formal; esforço e dono das mudanças não definidos'])
ent('crm','ext','CRM','SaaS de CRM (existente)','Cadastro de clientes, atendimento e casos de cobrança',status='existente',
    open=['Incluir o novo produto é configuração ou desenvolvimento? Fornecedor ainda não consultado'])
ent('erp','ext','ERP / Sistema legado','Monolito (existente)','Contratos, contas a receber e contabilidade',status='existente',
    open=['O cadastro de contratos não tem campo para o novo tipo de plano','O que precisa voltar ao ERP a cada fatura paga?'])
ent('gateway','ext','Gateway de Pagamento','API do provedor','Autorização e captura de cartão, Pix e boleto',status='existente',adr=['ADR-08'],
    open=['SLA, callback e limites de taxa não documentados'])
ent('sched','ext','Agendador','A confirmar','Dispara o ciclo diário de cobrança',status='existente',
    open=['Confirmar qual agendador corporativo executa jobs HTTP'])
ent('notif','ext','Provedor de Notificação','E-mail / SMS (existente)','Comunicados e avisos de fatura ao assinante',status='existente',
    open=['Contrato de integração não documentado'])
ent('fisco','ext','Fiscal e Contábil','Emissor de notas / contabilidade','Notas fiscais, conciliação e relatórios fiscais',status='existente',
    open=['Relatórios fiscais hoje saem de planilha e não têm dono'])
ent('idp','ext','Provedor de Identidade','OIDC','Autenticação de clientes e colaboradores',status='existente')

# ---------- sistema e contêineres ----------
ent('sys','system','Plataforma de Assinaturas','Bounded context "Assinaturas"','Fonte da verdade da assinatura: contratação, preço, cobrança recorrente e acompanhamento',status='novo')
ent('api','container','Experience API','BFF por canal + gateway de APIs','Expositor de jornada: contratos por canal e autenticação; sem regra de negócio',adr=['ADR-05'],
    open=['Quais canais entram no 1º ciclo','BFF existente × BFF dedicado'])
ent('orq','container','Orquestrador de Processo','Máquina de estados / workflow (a decidir)','Sagas de ativação, cobrança de fatura e troca de plano; compensações',adr=['ADR-02','ADR-06'],
    open=['Tecnologia: nenhum padrão corporativo de BPM/Saga identificado'])
ent('core','container','Serviço de Assinatura','Serviço de domínio (Java/Spring?)','Fonte da verdade: Plano, Assinatura, Calendário e Fatura (ledger imutável)',adr=['ADR-01'],
    open=['Onde a assinatura fica gravada e o que volta ao ERP'])
ent('preco','container','Serviço de Precificação','Stateless + regras versionadas','Simulação, preço, recálculo por ciclo, impostos e memória de cálculo',adr=['ADR-04'],
    open=['Regras oficiais de desconto e arredondamento','Tabela de impostos por município'])
ent('cobr','container','Serviço de Cobrança Recorrente','Padrão de outro produto: jobs HTTP + estados','Transforma a fatura vencida em ordem idempotente; retry e conciliação',status='reuso',adr=['ADR-03','ADR-08'],
    open=['Caminho A (via ERP) × B (direto no gateway)','Reuso de código do outro produto não validado'])
ent('qry','container','Serviço de Consulta (Read Model)','Projeção CQRS','Faturas pagas/pendentes, saldo e alertas para App, Site, CRM e dashboard',adr=['ADR-07'],
    open=['Formato do extrato por fatura ainda não desenhado'])
ent('aCrm','container','Adaptador CRM','REST + eventos (ACL)','Traduz casos do CRM ↔ domínio de assinatura; recebe a autorização do analista',
    open=['Fornecedor do CRM: configuração ou desenvolvimento?'])
ent('aErp','container','Adaptador ERP','REST + eventos (ACL)','Lê contratos; espelha assinatura e faturas; traduz o modelo do ERP',
    open=['A API de contratos suporta o novo tipo de plano?'])
ent('aGw','container','Adaptador Gateway','A: telas do ERP · B: API do gateway','Formata a ordem e traz o retorno (callback ou polling)',status='reuso',adr=['ADR-08'],
    open=['Decidir o caminho A × B — a decisão mais pesada do desenho'])
ent('aNotif','container','Adaptador Notificação','Evento → provedor de e-mail/SMS','Converte evento em comunicado (fatura emitida, falha, renovação)',status='reuso',
    open=['Comunicado por fatura ainda sem requisito'])
ent('aFisco','container','Adaptador Fiscal','Arquivo / evento','Notas fiscais, conciliação e relatórios fiscais',
    open=['Relatórios fiscais sem dono'])
ent('kafka','bus','Barramento de Eventos','Kafka','Eventos de domínio, comandos, callbacks e filas de exceção',status='existente',adr=['ADR-09'],
    open=['Confirmar cluster, schema registry e fila de exceção disponíveis'])
ent('coreDb','db','Assinatura DB','PostgreSQL','Escrita: assinatura, calendário, ledger, outbox/inbox')
ent('qryDb','db','Read DB','PostgreSQL','Modelos de leitura')
ent('precoDb','db','Regras e Log de Cálculo','Versionado + append-only','Tabelas de preço, impostos e memória de cálculo')

# ---------- componentes ----------
def comp(id, parent, name, tech, desc, status='novo'):
    ent(id,'component',name,tech,desc,status=status,parent=parent)
comp('o_listener','orq','Event Listener','Consumidor Kafka','Consome eventos com deduplicação (inbox)')
comp('o_defs','orq','Definições de Saga','Máquina de estados','Ativação, Cobrança e Troca de Plano (versionadas)')
comp('o_engine','orq','Motor de Execução','Workflow engine / máquina de estados','Avança passos, persiste estado e aplica timeout')
comp('o_comp','orq','Gerenciador de Compensação','Handler','Desfaz passos efetivados: cancelar calendário, estornar ordem')
comp('o_human','orq','Gateway de Tarefa Humana','Espera por evento','Aguarda a aprovação do analista no CRM')
comp('o_retry','orq','Política de Retry / DLQ','Backoff + jitter','Repete o passo; encaminha ao operacional após o limite')
comp('o_state','orq','Repositório de Estado','PostgreSQL','Instância, passo e chave de correlação')
comp('p_endpoint','preco','API de Precificação','REST síncrono','simular | calcular | recalcular (idempotente por entrada + versão)')
comp('p_guard','preco','Validações','Componente','Plano elegível, moeda, limites de desconto')
comp('p_resolver','preco','Resolvedor de Versão','Componente','Escolhe a tabela de preço vigente na data de referência')
comp('p_engine','preco','Motor de Regras','DMN ou código (a decidir)','Preço base, descontos, proporcional (pro-rata) e arredondamento')
comp('p_tax','preco','Módulo Fiscal','Regras de imposto','Impostos por fatura (tabela a validar com o Fiscal)')
comp('p_memo','preco','Gerador de Memória de Cálculo','Componente','Entradas, regra + versão, passos e resultado (extrato por fatura)')

# ---------- relacionamentos (origem, destino, texto, tecnologia, tipo: sync|async|batch) ----------
R = [
 ('assinante','app_cli','Contrata e altera o plano','','sync'),
 ('convidado','app_cli','Usa e acompanha','','sync'),
 ('parceiro','portal_par','Vende e altera planos','','sync'),
 ('analista','crm','Analisa e autoriza','','sync'),
 ('suporte','crm','Consulta faturas','','sync'),
 ('financeiro','fisco','Consome relatórios fiscais','','sync'),
 ('app_cli','api','Contratação, simulação e consulta','HTTPS/JSON','sync'),
 ('portal_par','api','Contratação e simulação','HTTPS/JSON','sync'),
 ('api','idp','Valida identidade e papéis','OIDC','sync'),
 ('api','core','Registra a assinatura (comando)','HTTPS','sync'),
 ('api','preco','Simula o preço (síncrono)','HTTPS','sync'),
 ('api','qry','Consulta o acompanhamento','HTTPS','sync'),
 ('crm','aCrm','Pedido de preço / aprovação','HTTPS / evento','sync'),
 ('aCrm','crm','Resultado, memória de cálculo e status','HTTPS','sync'),
 ('aCrm','kafka','Publica pedidos e aprovações','Evento','async'),
 ('kafka','aCrm','Entrega o resultado do cálculo','Evento','async'),
 ('kafka','orq','Inicia e avança sagas','Evento','async'),
 ('orq','kafka','Publica o andamento das sagas','Evento','async'),
 ('orq','preco','Calcula / recalcula','HTTPS síncrono','sync'),
 ('orq','core','Comanda o estado da assinatura','Comando idempotente','sync'),
 ('orq','cobr','Emite a ordem de cobrança','Comando idempotente','sync'),
 ('cobr','core','Lista as faturas vencidas','HTTPS','sync'),
 ('core','coreDb','Lê / escreve','JDBC','sync'),
 ('core','kafka','Publica eventos (outbox)','Evento','async'),
 ('preco','precoDb','Lê regras; grava a memória de cálculo','','sync'),
 ('cobr','kafka','Publica ordens e resultados','Evento','async'),
 ('kafka','aGw','Entrega a ordem de cobrança','Evento','async'),
 ('aGw','kafka','Publica o resultado da cobrança','Evento','async'),
 ('aGw','gateway','Ordem (caminho B) ou via ERP (A)','API / arquivo','sync'),
 ('gateway','aGw','Retorno: callback (B) ou polling (A)','','sync'),
 ('aGw','erp','Caminho A: lança a cobrança no ERP','API do ERP','sync'),
 ('sched','cobr','Dispara o ciclo diário','Job','sync'),
 ('kafka','qry','Projeta os eventos','Evento','async'),
 ('qry','qryDb','Lê / escreve','JDBC','sync'),
 ('kafka','aErp','Espelha assinatura e faturas','Evento','async'),
 ('aErp','erp','Lê contratos; escreve o espelho','API + fila','async'),
 ('kafka','aNotif','Aciona comunicados','Evento','async'),
 ('aNotif','notif','Envia comunicados','API do provedor','async'),
 ('kafka','aFisco','Alimenta notas e relatórios','Evento','async'),
 ('aFisco','fisco','Entrega arquivos fiscais','Arquivo','batch'),
]
R1 = [
 ('assinante','app_cli','Contrata e altera o plano','','sync'),
 ('convidado','app_cli','Usa e acompanha','','sync'),
 ('parceiro','portal_par','Vende e altera planos','','sync'),
 ('analista','crm','Analisa e autoriza','','sync'),
 ('suporte','crm','Consulta faturas','','sync'),
 ('financeiro','sys','Valida regras; consome relatórios','','sync'),
 ('app_cli','sys','Contratação, simulação, consulta','HTTPS / Experience API','sync'),
 ('portal_par','sys','Contratação e simulação','HTTPS / Experience API','sync'),
 ('crm','sys','Preço, aprovação, consulta','HTTPS + eventos','sync'),
 ('sys','erp','Espelho de assinatura e faturas','API + eventos','async'),
 ('sys','gateway','Ordem de cobrança / retorno','API ou via ERP','sync'),
 ('sched','sys','Dispara o ciclo diário','Job','sync'),
 ('sys','notif','Comunicados por fatura','Evento','async'),
 ('sys','fisco','Dados fiscais','Arquivo / evento','batch'),
 ('sys','idp','Valida identidade e papéis','OIDC','sync'),
]
RC_ORQ = [
 ('kafka','o_listener','Eventos e comandos','Kafka','async'),
 ('o_listener','o_engine','Dispara / avança','','sync'),
 ('o_engine','o_defs','Lê a definição','','sync'),
 ('o_engine','o_state','Persiste o estado','JDBC','sync'),
 ('o_engine','o_human','Pausa até a aprovação','','sync'),
 ('o_engine','o_comp','Em falha de passo','','sync'),
 ('o_engine','o_retry','Em erro transitório','','sync'),
 ('o_engine','preco','Calcula','HTTPS','sync'),
 ('o_engine','core','Comanda o estado','HTTPS','sync'),
 ('o_engine','cobr','Ordena a cobrança','HTTPS','sync'),
]
RC_PRECO = [
 ('api','p_endpoint','Simula','HTTPS','sync'),
 ('orq','p_endpoint','Calcula / recalcula','HTTPS','sync'),
 ('p_endpoint','p_guard','Valida','','sync'),
 ('p_endpoint','p_resolver','Resolve a versão','','sync'),
 ('p_endpoint','p_engine','Executa','','sync'),
 ('p_resolver','precoDb','Lê tabelas e índices','','sync'),
 ('p_engine','p_tax','Imposto','','sync'),
 ('p_engine','p_memo','Registra os passos','','sync'),
 ('p_memo','precoDb','Grava o log imutável','','sync'),
]
RC = RC_ORQ + RC_PRECO

# ---------- decisões (ADR-lite): (id, decisão, alternativas, depende de, estado, nota) — estado: aberto | tend | nossa ----------
ADR = [
 ('ADR-01','Fonte da verdade da assinatura fora do ERP; o legado recebe só um espelho mínimo','Tudo no ERP; CRM como hub','Q-01 · D-02','tend','Tendência de 1 arquiteto, sem artefato'),
 ('ADR-02','Orquestração: máquina de estados em PostgreSQL como ponto de partida; engine de workflow só se a Arquitetura já operar uma','Engine BPM · serviço gerenciado de workflow · coreografia pura','D-03','aberto','Nenhum padrão corporativo identificado'),
 ('ADR-03','Reusar o padrão de cobrança de outro produto (jobs + estados + retry + fila manual) e avaliar reuso de código','Construir do zero · reusar o serviço como está','Idempotência e agendador não documentados','tend','Hipótese'),
 ('ADR-04','Precificação isolada e síncrona; o mesmo código serve à simulação e ao cálculo real','Regras dentro do CRM · dentro do ERP','Q-04','tend','Regras de desconto em aberto'),
 ('ADR-05','Contratação capturada em qualquer canal por uma Experience API única','Cada canal grava direto no legado','Q-05','tend','Escopo de canais é indício'),
 ('ADR-06','Calendário de cobrança como dado + saga curta por fatura','Uma instância de processo viva por assinatura (anos)','—','nossa','Decisão de design nossa, contestável'),
 ('ADR-07','CQRS para o acompanhamento de faturas','Consulta direta ao serviço de assinatura ou ao ERP','Extrato por fatura ainda não desenhado','nossa','Decisão de design nossa'),
 ('ADR-08','Caminho de cobrança: A (via ERP, retorno por polling) × B (direto no gateway, callback)','—','Q-02 · D-01','aberto','Decisão central; sem evidência para recomendar'),
 ('ADR-09','Barramento: confirmar o cluster e se há schema registry e fila de exceção','Outbox + polling de banco se não houver','Q-09','aberto','Depende da equipe de plataforma'),
]
ADR_STATE = {'aberto':'Em aberto','tend':'Tendência / hipótese','nossa':'Proposta nossa'}

# ---------- fluxos (diagramas de sequência) ----------
FLOWS = {
 'f_contratacao': dict(
   title='Fluxo 1 — Contratação de plano (autosserviço)',
   parts=[('S','Assinante'),('C','App / Site'),('J','Experience API'),('M','Serviço de Precificação'),('B','Serviço de Assinatura'),('K','Kafka'),('Q','Consulta'),('I','Adaptador ERP')],
   msgs=[
    ('S','C','Escolhe plano e periodicidade','call'),
    ('C','J','POST /assinaturas (Idempotency-Key)','call'),
    ('J','M','simular(plano, periodicidade, cupom)','call'),
    ('M','J','valor estimado + versão da regra','ret'),
    ('J','C','exibe a simulação (p95 ≤ 3 s)','ret'),
    ('S','C','Confirma a contratação','call'),
    ('C','J','confirmar(assinatura)','call'),
    ('J','B','registrarAssinatura (idempotente)','call'),
    ('B','B','grava Assinatura + outbox na mesma transação','self'),
    ('B','J','201 (protocolo)','ret'),
    ('J','C','"assinatura registrada"','ret'),
    ('B','K','AssinaturaRegistrada (outbox)','async'),
    ('K','Q','projeta a visão de consulta','async'),
    ('K','I','espelhar no ERP','async'),
    ('I','I','escreve o espelho (API / fila) com retry e DLQ','self'),
    ('note','I','K','Escrita no ERP é eventual (minutos a horas). O canal mostra "registrada", não "refletida no ERP".'),
   ]),
 'f_ativacao': dict(
   title='Fluxo 2 — Saga de Ativação (contrato especial aprovado por analista)',
   parts=[('A','Analista'),('CR','CRM'),('AC','Adaptador CRM'),('K','Kafka'),('O','Orquestrador'),('M','Serviço de Precificação'),('B','Serviço de Assinatura'),('P','Cobrança Recorrente'),('AE','Adaptador ERP'),('N','Notificação')],
   msgs=[
    ('CR','CR','Analisa documentação e crédito','self'),
    ('A','CR','Solicita o preço do contrato','call'),
    ('CR','AC','SolicitarPreço(contratoId, condições)','call'),
    ('AC','K','PreçoSolicitado','async'),
    ('K','O','inicia a Saga de Ativação (correlação = contratoId)','async'),
    ('O','B','obterCondiçõesVigentes(cliente)','call'),
    ('B','O','condições (padrão | negociadas)','ret'),
    ('O','M','calcular(entradas)','call'),
    ('M','O','preço, calendário, impostos, memória, versão','ret'),
    ('O','K','PreçoConcluído','async'),
    ('K','AC','devolve resultado + memória','async'),
    ('AC','CR','exibe ao analista','ret'),
    ('A','CR','Aprova (alçada)','call'),
    ('CR','AC','ContratoAprovado','call'),
    ('AC','K','ContratoAprovado','async'),
    ('K','O','retoma a saga (tarefa humana concluída)','async'),
    ('O','B','ativarAssinatura (gera calendário e faturas)','call'),
    ('O','P','cobrarFatura(1) — chave = assinatura:1','call'),
    ('P','K','OrdemCobrançaEmitida','async'),
    ('O','K','AssinaturaAtivada','async'),
    ('K','AE','espelhar a ativação no ERP','async'),
    ('K','N','comunicar a 1ª fatura','async'),
    ('alt','Falha em passo após a ativação'),
    ('O','B','cancelarCalendário (compensação)','call'),
    ('O','K','AtivaçãoFalhou → alerta operacional','async'),
    ('end',),
   ]),
 'f_cobranca': dict(
   title='Fluxo 3 — Saga de Cobrança de Fatura (ciclo recorrente)',
   parts=[('AU','Agendador'),('P','Cobrança Recorrente'),('B','Serviço de Assinatura'),('K','Kafka'),('O','Orquestrador'),('M','Serviço de Precificação'),('AG','Adaptador Gateway'),('X','Gateway de Pagamento'),('AE','Adaptador ERP')],
   msgs=[
    ('AU','P','dispara o ciclo diário','call'),
    ('P','B','listar faturas vencidas e não pagas','call'),
    ('loop','Para cada fatura vencida (idempotente)'),
    ('P','K','FaturaVencida(assinatura, competência)','async'),
    ('K','O','inicia a Saga de Cobrança — chave = assinatura:competência','async'),
    ('O','M','recalcular(valor, impostos, competência)','call'),
    ('M','O','valor da fatura + memória + versão','ret'),
    ('O','B','congelarFatura (snapshot imutável)','call'),
    ('O','P','emitirOrdem(chave = assinatura:competência)','call'),
    ('P','K','ordem de cobrança','async'),
    ('K','AG','entrega a ordem','async'),
    ('AG','X','B: API do gateway · A: lança no ERP → remessa','call'),
    ('X','AG','B: callback · A: polling do status no ERP','ret'),
    ('AG','K','ResultadoCobrança','async'),
    ('K','O','avança a saga','async'),
    ('alt','Paga'),
    ('O','B','baixarFatura (ledger)','call'),
    ('O','K','FaturaPaga','async'),
    ('K','AE','atualiza contas a receber no ERP','async'),
    ('alt','Recusada · cartão expirado · saldo insuficiente'),
    ('O','O','retry com backoff (erro transitório)','self'),
    ('O','K','FaturaFalhou → régua de cobrança + alerta','async'),
    ('note','O','B','Compensação: a fatura volta a "pendente"; a assinatura fica "suspensa" após N falhas; aviso ao assinante.'),
    ('end',),
    ('end',),
   ]),
}

# fluxos para o Structurizr (dynamic) — evite acentos/aspas nos nomes das vistas
DYN = {
 'Fluxo_Contratacao': ('Contratacao de plano (autosservico)', [
   ('assinante','app_cli','Escolhe e confirma o plano'),
   ('app_cli','api','POST /assinaturas'),
   ('api','preco','Simula o preço'),
   ('api','core','Registra a assinatura (idempotente)'),
   ('core','kafka','AssinaturaRegistrada (outbox)'),
   ('kafka','qry','Projeta a visão de consulta'),
   ('kafka','aErp','Espelha no ERP'),
   ('aErp','erp','Escreve o espelho (eventual)'),
 ]),
 'Fluxo_Ativacao': ('Saga de Ativacao (contrato especial)', [
   ('analista','crm','Solicita o preço'),
   ('crm','aCrm','SolicitarPreço'),
   ('aCrm','kafka','PreçoSolicitado'),
   ('kafka','orq','Inicia a saga'),
   ('orq','core','Obtém as condições vigentes'),
   ('orq','preco','Calcula o preço'),
   ('orq','kafka','PreçoConcluído'),
   ('kafka','aCrm','Devolve resultado e memória'),
   ('aCrm','crm','Exibe ao analista'),
   ('analista','crm','Aprova'),
   ('crm','aCrm','ContratoAprovado'),
   ('aCrm','kafka','ContratoAprovado'),
   ('kafka','orq','Retoma a saga'),
   ('orq','core','Ativa a assinatura e gera o calendário'),
   ('orq','cobr','Cobra a fatura 1'),
   ('cobr','kafka','Ordem de cobrança emitida'),
   ('orq','kafka','AssinaturaAtivada'),
   ('kafka','aErp','Espelha a ativação'),
   ('kafka','aNotif','Comunica a 1ª fatura'),
 ]),
 'Fluxo_Cobranca': ('Saga de Cobranca de Fatura', [
   ('sched','cobr','Dispara o ciclo diário'),
   ('cobr','core','Lista as faturas vencidas'),
   ('cobr','kafka','FaturaVencida'),
   ('kafka','orq','Inicia a saga da fatura'),
   ('orq','preco','Recalcula valor e impostos'),
   ('orq','core','Congela a fatura'),
   ('orq','cobr','Emite a ordem (chave assinatura:competência)'),
   ('cobr','kafka','Ordem de cobrança'),
   ('kafka','aGw','Entrega a ordem'),
   ('aGw','gateway','Caminho B: API · Caminho A: via ERP'),
   ('gateway','aGw','Retorno: callback ou polling'),
   ('aGw','kafka','ResultadoCobrança'),
   ('kafka','orq','Avança a saga'),
   ('orq','core','Baixa a fatura no ledger'),
   ('orq','kafka','FaturaPaga'),
   ('kafka','aErp','Atualiza contas a receber'),
 ]),
}

# ---------- metadados do projeto (textos que o motor não conhece) ----------
META = dict(
    stem='exemplo',                               # arquivos: exemplo.dsl, exemplo.drawio, exemplo-arquitetura.html
    sys_id='sys',                                 # id da entidade kind='system'
    agent='dd-arch-diagrams',
    download_prefix='exemplo-',
    page_title='Plataforma de Assinaturas · Arquitetura conceitual v1',
    title='Plataforma de Assinaturas — Arquitetura conceitual v1',
    badge='EXEMPLO FICTÍCIO · HIPÓTESE DE TRABALHO',
    subtitle='Modelo C4 · exemplo genérico do gerador dd-arch-diagrams',
    chips=['Experience API', 'Orquestrador', 'Assinatura', 'Precificação', 'Cobrança recorrente', 'Consulta (CQRS)', 'Adaptadores (ACL)', 'Kafka'],
    flow_hint='Sequência conceitual · setas tracejadas roxas = eventos (Kafka)',
    slide_legend=[('Novo', 'novo'), ('Aproveita padrão existente (a validar)', 'reuso'), ('Existente na organização', 'existente')],
    tabs=[
        ('c1', 'C1 · Contexto', 'blk'),
        ('c2', 'C2 · Contêineres', 'blk'),
        ('c3o', 'C3 · Orquestrador', 'blk'),
        ('c3p', 'C3 · Precificação', 'blk'),
        ('f_contratacao', 'Fluxo 1 · Contratação', 'seq'),
        ('f_ativacao', 'Fluxo 2 · Ativação', 'seq'),
        ('f_cobranca', 'Fluxo 3 · Cobrança', 'seq'),
        ('adr', 'Decisões', 'doc'),
        ('slide', 'Slide executivo', 'blk'),
        ('sobre', 'Sobre', 'doc'),
    ],
    drawio_views=['c1', 'c2', 'c3o', 'c3p', 'slide'],
    drawio_flows=['f_contratacao', 'f_ativacao', 'f_cobranca'],
    open_limits=[
        ('Caminho da cobrança (A × B)', 'Depende de resposta do Financeiro e do time do ERP, que ainda não participaram.'),
        ('O que volta ao ERP a cada fatura', 'Sem o time do ERP na mesa; o cadastro de contratos não tem campo para o novo plano.'),
        ('Regras oficiais de preço e imposto', 'Financeiro e Fiscal não validaram tabelas nem arredondamento.'),
        ('Migração da base atual', 'Convivência ou corte único: sem decisão.'),
        ('Alteração de plano pelo Suporte', 'Fluxo não validado; Suporte não acessa o CRM de cobrança.'),
        ('Idempotência, agendador e cluster de eventos', 'O padrão reaproveitado não documenta idempotência; agendador não confirmado.'),
    ],
    adr_sub='Todas são <b>propostas</b>. Nenhuma foi validada por Arquitetura, ERP, CRM, Financeiro ou Segurança.',
    principles=[
        '<li><b>Fonte da verdade fora do legado</b> e anti-corrupção: nenhum serviço de negócio conhece o modelo do ERP ou do CRM.</li>',
        '<li><b>Síncrono só onde o usuário espera</b> (simulação, registro); o resto é assíncrono e idempotente.</li>',
        '<li><b>Orquestração</b> para o que tem compensação (dinheiro saindo); <b>coreografia</b> para reações.</li>',
        '<li><b>Cálculo reprodutível</b>: versão da regra + snapshot das entradas + memória de cálculo em toda fatura.</li>',
        '<li><b>Processo longo = dado + sagas curtas</b>; CQRS no acompanhamento; <b>sem Event Sourcing</b> na v1.</li>',
    ],
    sobre=dict(
        sub='Plataforma de Assinaturas (exemplo) · arquitetura conceitual v1',
        cards=[
            ('O que é', [
                '<li>Exemplo <b>fictício</b> do gerador dd-arch-diagrams: um desenho conceitual (modelo C4) de cobrança recorrente.</li>',
                '<li><b>Não descreve nenhum sistema real.</b> Serve de molde para outros projetos.</li>']),
            ('Evidência × hipótese', [
                '<li><b>Evidência</b>: o que foi confirmado em fonte rastreável (cores sólidas).</li>',
                '<li><b>Hipótese</b>: tudo que está em âmbar, os ADRs e os nomes de serviços.</li>']),
            ('Como usar', [
                '<li>Abas C1 → C3 descem em detalhe; clique nos blocos para ver decisões e pontos em aberto.</li>',
                '<li>“Baixar SVG” em cada aba gera imagem vetorial (cola em PowerPoint e Visio).</li>',
                '<li>Imprimir (Ctrl+P) imprime apenas a aba ativa.</li>']),
            ('Arquivos irmãos', [
                '<li><code>exemplo.dsl</code> — Structurizr DSL (fonte textual, versionável)</li>',
                '<li><code>exemplo.drawio</code> — mesmas vistas, editáveis no draw.io</li>']),
        ]),
    dsl=dict(
        workspace_name='Plataforma de Assinaturas — Arquitetura conceitual v1',
        workspace_desc='Exemplo fictício do gerador dd-arch-diagrams. Desenho conceitual (C4) de cobrança recorrente; hipótese de trabalho.',
        c1='C1 — Contexto da Plataforma de Assinaturas',
        c2='C2 — Contêineres da Plataforma de Assinaturas',
        c3=[('orq', 'C3_Orquestrador', 'C3 — Componentes do Orquestrador de Processo'),
            ('preco', 'C3_Precificacao', 'C3 — Componentes do Serviço de Precificação')],
    ),
)

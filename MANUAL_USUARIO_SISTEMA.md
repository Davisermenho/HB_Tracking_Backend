# Manual do Usuário (V1.1.1)
Este manual orienta o uso do sistema por qualquer perfil (Dirigente, Coordenador, Treinador, Atleta), alinhado ao RAG REGRAS_SISTEMAS.md (V1.1).

Sumário
1. Perfis e acessos
2. Primeiros passos (login, senha, perfil)
3. Cadastro de pessoas (cadeia hierárquica)
4. Temporadas e equipes
5. Atividades: treinos e jogos
6. Convocações e participações
7. Estados da atleta e disciplina
8. Estatísticas e relatórios
9. Rascunhos, correções e reaberturas
10. Notificações e operação offline
11. Perguntas frequentes (FAQ)

1) Perfis e acessos
- Atleta: vê seus próprios dados, histórico e estatísticas pessoais; modo somente leitura se sem vínculo ativo (R42).
- Treinador: opera apenas equipes onde for responsável (RF7); pode criar treinos e jogos com o Coordenador (RF9).
- Coordenador: acesso operacional amplo; cria treinos/jogos/estatísticas; reabre/exclui logicamente jogos (RF15).
- Dirigente: acesso administrativo total; cria temporadas e equipes; troca treinador responsável; aprova encerramentos (RF7, RF5).
- Super Administrador: existe apenas no seed; não é gerenciável pelo fluxo comum.

2) Primeiros passos
- Login:
  - Informe e-mail e senha. A senha exige no mínimo 8 caracteres.
  - Em caso de esquecimento, use “Esqueci minha senha” para redefinir.
- Perfil:
  - Atualize telefone, endereço e foto (opcionais).
  - Campos derivados (idade, categoria da temporada) são exibidos e não editáveis.

3) Cadastro de pessoas (cadeia hierárquica) — RF1
- Dirigente cria Coordenadores.
- Coordenador cria Treinadores.
- Treinador cria Atletas.
- Observação: não é necessário escolher equipe no cadastro; o sistema cria vínculos mínimos nos bastidores.

4) Temporadas e equipes
- Temporadas:
  - Podem ser criadas por Dirigentes, Coordenadores e Treinadores (RF4).
  - O encerramento é automático ao final do período; cancelamento só antes do início e sem dados vinculados (RF5).
- Equipes:
  - Criadas por Dirigentes/Coordenadores (RF6).
  - A atleta sempre tem participação em alguma equipe: competitiva ou Institucional (R38–R39).

5) Atividades: treinos e jogos
- Treinos:
  - Podem ser criados por Coordenadores e Treinadores (RF9).
  - Edição: até 10 minutos livre; até 24 horas com aprovação superior; após 24 horas, somente por ação administrativa auditada (R40/R27).
- Jogos:
  - Podem ser criados e finalizados por Dirigentes, Coordenadores e Treinadores (RF14).
  - Reabertura: apenas pelo Coordenador (ou também Diretor se configurado) via ação administrativa auditada; ao reabrir, o jogo volta a “Em Revisão” (RF15).

6) Convocações e participações
- Convocação:
  - A atleta só participa se estiver convocada (RP3).
  - Limite: no máximo 16 atletas relacionadas por jogo (RD18).
- Participação:
  - Disciplinar: presença em súmula (banco + quadra).
  - Estatística: exige tempo efetivo em quadra (RP1–RP2).
  - Ausências, banco, amistosos e oficiais são registrados conforme regras RD51–RD66.

7) Estados da atleta e disciplina
- Estados: ativa, lesionada, dispensada (R13–R14).
  - Lesionada: participa normalmente, com alertas (R14).
  - Dispensada: não participa de novas atividades; aparece somente em histórico.
- Disciplina:
  - Suspensa: participação em quadra é irregular; o sistema sinaliza “Atleta Irregular”, mas as estatísticas contam (RD16).
  - Acúmulo de cartões/exclusões é controlado automaticamente, sem suspensão automática (RD17, RD38, RD70).

8) Estatísticas e relatórios
- Estatísticas individuais pertencem à atleta e acumulam por temporada e carreira (RD5).
- Estatísticas coletivas são derivadas das individuais (RD20).
- Dashboards e rankings usam dados validados; ajustes aparecem após validação (RF29, RD85).

9) Rascunhos, correções e reaberturas
- Rascunhos:
  - Podem ser salvos incompletos; visíveis à comissão técnica; sem efeito operacional/analítico (RF18, RF22).
- Correções:
  - Sempre com justificativa (admin_note); valor anterior é preservado em auditoria (R23–R24).
- Reabertura de jogo:
  - Retorna o status a “Em Revisão”; estatísticas deixam de alimentar relatórios até nova finalização (RF15).

10) Notificações e operação offline
- Notificações críticas bloqueiam ações até serem lidas e confirmadas (RF24).
- Operação offline:
  - É possível registrar eventos offline em jogos; o sistema sincroniza depois, preservando ordem e integridade (RF25).

11) FAQ
- Por que não consigo operar se acabei de me cadastrar?
  - Sem vínculo ativo não há operação (R42). Após cadastro, o sistema cria vínculos mínimos; para operar em equipe, podem ser exigidos RG/CPF, posição defensiva e responsabilidade (Seção 7 do RAG).
- Sou goleira e o campo de posição ofensiva sumiu. É normal?
  - Sim, goleira não recebe posição ofensiva; tempo e estatísticas de linha são bloqueados (RD13).
- Posso atuar em equipes diferentes no mesmo dia?
  - Sim, o sistema permite e alerta sobre carga; não há limite diário extra (RD62–RD63).
- Por que não consigo finalizar um jogo?
  - Verifique se há convocação válida e se não ultrapassou o limite de 16 atletas (RP3, RD18). Em conflitos de edição, é necessária decisão autorizada (R41).
- Quem pode reabrir um jogo?
  - Coordenador. O Dirigente também pode se a configuração permitir (RF15/6.1.2).

Dicas
- Em dúvidas de uso, procure as mensagens do sistema: elas indicam a regra violada e o que precisa ser corrigido.
- O histórico é preservado; mudanças não reescrevem o passado e sempre geram auditoria.

'use strict';
const copy = {
  zh: {
    figureEvidenceLabel:'实际诊断图',openFigure:'查看完整图 ↗',figureEvidenceTitle:'相同场景，不同上下文释放方式。',figureEvidenceCaption:'完整保留三个合成分支、十二个读回数组。中间失败分支保留初始化填充值；其余对照图像逐字节一致。仅证明最小释放机制，不证明历史 RoboCasa 图像损坏原因。',
    skip:'跳到内容',navOverview:'概览',navProposal:'研究方案',navEvidence:'证据记录',navTimeline:'进展',
    eyebrow:'具身智能 · 经验迁移 · 公开研究记录',heroTitle:'换一个任务，\n旧经验还能帮忙吗？',
    heroSubtitle:'在权重冻结的机器人策略中，把任务记忆与执行条件拆开，追踪经验从输入、压缩到检索和行动的每一步。',
    exploreDesign:'阅读研究方案',inspectEvidence:'查看现有证据 →',heroFootnote:'当前处于运行与观测资格验证阶段。正式迁移评估尚未开始。',
    figureTitle:'经验的去向',figureCaption:'概念示意 · 神经参数冻结，研究者干预初始记忆。',
    metricFormal:'已完成正式 query',metricFormalSub:'尚未授予物理与信息资格',metricTasks:'固定任务',metricCells:'核心反事实条件',metricCellsSub:'任务匹配 × 执行增益匹配',metricSmoke:'计划 smoke queries',metricSmokeSub:'4 worlds × 12 条件 · 未运行',
    currentLabel:'当前进展',questionLabel:'研究问题',questionTitle:'经验里，究竟是什么在迁移？',questionIntro:'任务外观、执行响应、状态延续与额外尝试很容易混在一起。方案通过配对的来源条件，审计它们各自的作用边界。',
    claimOneTitle:'初始经验的条件效应',claimOneText:'在完整 reset 和相同当前任务下，来源执行增益是否匹配，会怎样改变同一冻结策略的闭环表现？',claimTwoTitle:'信息利用与误用的边界',claimTwoText:'信息是否进入压缩表示、被检索并影响行动？用合法对照和同观察校准，限制解释，而不把日志当作因果机制证明。',scopeLabel:'研究范围',scopeText:'针对公开冻结 PIM 策略的研究者记忆移植。关闭成功轨迹重放；不重新训练策略，也不声称原生跨任务自我改进。',
    designLabel:'反事实设计',designTitle:'同一个 query，四种旧经历。',designIntro:'所有组共享名义标定 R₀。分别改变来源任务与执行增益，保留真实来源身份，再恢复到当前 query 的初始记忆。',gainMismatch:'增益不匹配',gainMatch:'增益匹配',taskMatch:'任务匹配',taskMismatch:'任务不匹配',h10:'相同任务 · 不同增益',h11:'相同任务 · 相同增益',h00:'不同任务 · 不同增益',h01:'不同任务 · 相同增益',matrixNote:'点击条件查看其含义。这里展示实验设计，尚无成功率结果。',conditionLabel:'所选条件',contrastNote:'预定主比较：任务匹配时，增益匹配带来的差异。按独立 query world 配对；不挑选最大差异。',
    protocolLabel:'执行协议',protocolTitle:'先取得资格，再统计迁移。',protocolIntro:'正式实验有固定的信息权限、预算和停止规则。调试证据不会自动解锁正式评估。',groupsCaption:'完整路线：每个 world 的 12 个条件',group:'条件族',count:'数量',initialMemory:'初始 PIM',extraInput:'额外读取',
    evidenceLabel:'证据记录',evidenceTitle:'保留结果，也保留失败。',evidenceIntro:'以下是开发诊断与资格检查，不是正式任务成功率。查看每条记录的范围、观察和解释边界。',all:'全部',verified:'已验证',blocked:'受阻',inProgress:'进行中',searchLabel:'搜索证据',searchPlaceholder:'搜索记录…',noResults:'没有符合条件的记录。',details:'查看记录 ↗',reviewNote:'核验项数只描述记录一致性，不代表独立样本数或机器人成功次数。审查为继续使用的同系列模型，未取得全新独立审查资格。',
    progressLabel:'进展与下一步',progressTitle:'从能运行，到能解释。',progressIntro:'用明确的门槛串起实验。运行成功、观测有效、信息可辨识和任务收益是不同的结论。',nextLabel:'下一步',download:'下载进展快照 ↓',referencesLabel:'参考与来源',referencesTitle:'放在已有工作的坐标里。',referencesIntro:'研究背景、基础代码和页面形式的参考。外部项目的结果不作为本项目的实验结果。',footer:'持续更新的研究记录 · 展示方案、证据与未解决的问题。',recordDetails:'记录详情',observations:'实际观察',limits:'解释边界',nextAction:'后续动作',provenance:'来源',reviewChecks:'核验项数',close:'关闭详情',loadError:'进展数据加载失败。请通过 HTTP 预览页面并检查 data/progress.json。',updated:'快照更新'
  },
  en: {
    figureEvidenceLabel:'Observed diagnostic figure',openFigure:'Open full figure ↗',figureEvidenceTitle:'The same scene. Different context-release rules.',figureEvidenceCaption:'All three synthetic branches and twelve readback arrays are retained. The failing middle branch preserves initialization fills; control images remain byte-exact. This establishes a minimal release mechanism, not the historical cause of RoboCasa image corruption.',
    skip:'Skip to content',navOverview:'Overview',navProposal:'Research design',navEvidence:'Evidence',navTimeline:'Progress',
    eyebrow:'Embodied intelligence · Experience transfer · Open notebook',heroTitle:'When the task changes,\nwhat carries over?',
    heroSubtitle:'Separate task memory from execution conditions in a frozen robot policy. Follow experience through input, compression, retrieval, and action.',
    exploreDesign:'Explore the design',inspectEvidence:'Inspect the evidence →',heroFootnote:'Runtime and observation qualification are in progress. Formal transfer evaluation has not started.',
    figureTitle:'Where experience goes',figureCaption:'Conceptual diagram · Frozen neural parameters, researcher-controlled initial memory.',
    metricFormal:'Formal queries completed',metricFormalSub:'Physical and information gates remain open',metricTasks:'Fixed tasks',metricCells:'Counterfactual source cells',metricCellsSub:'Task match × execution-gain match',metricSmoke:'Planned smoke queries',metricSmokeSub:'4 worlds × 12 conditions · Not run',
    currentLabel:'Current frontier',questionLabel:'The research question',questionTitle:'What, exactly, transfers in experience?',questionIntro:'Task appearance, execution response, persistent state, and extra attempts can be confounded. Paired source conditions help audit their boundaries.',
    claimOneTitle:'The conditional effect of initial experience',claimOneText:'After a full reset and under the same current task, how does a matching source execution gain change the closed-loop behavior of a frozen policy?',claimTwoTitle:'Boundaries of information use and misuse',claimTwoText:'Does information enter the compressed representation, get retrieved, and affect action? Legal controls and matched-observation calibration constrain interpretation; logs alone do not prove a causal mechanism.',scopeLabel:'Scope',scopeText:'Researcher-controlled memory transplantation in a public frozen PIM policy. Success-trajectory replay is disabled. No policy retraining or claim of native cross-task self-improvement.',
    designLabel:'Counterfactual design',designTitle:'One query. Four kinds of prior experience.',designIntro:'All groups share nominal calibration R₀. Vary the source task and execution gain, preserve the true source identity, and restore the history into the current query memory.',gainMismatch:'Gain mismatch',gainMatch:'Gain match',taskMatch:'Task match',taskMismatch:'Task mismatch',h10:'Same task · Different gain',h11:'Same task · Same gain',h00:'Different task · Different gain',h01:'Different task · Same gain',matrixNote:'Select a cell to inspect the design. No task success rates have been measured here.',conditionLabel:'Selected condition',contrastNote:'Prespecified primary contrast: the effect of gain matching when the task matches. Paired by independent query world; no selection of the largest contrast.',
    protocolLabel:'Execution protocol',protocolTitle:'Qualify first. Evaluate transfer second.',protocolIntro:'Formal experiments have fixed information permissions, budgets, and stopping rules. Debugging evidence does not automatically unlock formal evaluation.',groupsCaption:'Full route: 12 conditions per world',group:'Condition family',count:'Count',initialMemory:'Initial PIM',extraInput:'Additional input',
    evidenceLabel:'Evidence ledger',evidenceTitle:'Keep the findings. Keep the failures.',evidenceIntro:'These are development diagnostics and qualification checks, not formal task success rates. Inspect each record’s scope, observations, and limits.',all:'All',verified:'Verified',blocked:'Blocked',inProgress:'In progress',searchLabel:'Search evidence',searchPlaceholder:'Search records…',noResults:'No matching records.',details:'Inspect record ↗',reviewNote:'Check counts describe record consistency, not independent samples or robot successes. Reviews reuse the same model family and do not establish fresh independent-review qualification.',
    progressLabel:'Progress and next steps',progressTitle:'From running to understanding.',progressIntro:'Explicit gates connect the experiments. Runtime success, valid observations, identifiable information, and task benefit are separate findings.',nextLabel:'Next frontier',download:'Download progress snapshot ↓',referencesLabel:'References and sources',referencesTitle:'Place the work in context.',referencesIntro:'Research context, source code, and presentation references. External project results are not results of this project.',footer:'A living research notebook: designs, evidence, and open questions.',recordDetails:'Record details',observations:'Observed results',limits:'Interpretation limits',nextAction:'Next action',provenance:'Provenance',reviewChecks:'Record checks',close:'Close details',loadError:'Progress data could not load. Preview over HTTP and check data/progress.json.',updated:'Snapshot updated'
  }
};
const views = new Set(['overview','proposal','evidence','timeline']);
const states = new Set(['all','verified','blocked','in_progress']);
let data, lang = 'zh', view = 'overview', filter = 'all', condition = 'H11', dialogRecord = null;
const $ = (s) => document.querySelector(s);
const t = (value) => typeof value === 'string' ? value : (value?.[lang] || value?.en || '');
const node = (tag, value, cls) => { const el = document.createElement(tag); if (value !== undefined) el.textContent = value; if (cls) el.className = cls; return el; };
function readRoute() {
  const query = new URL(location.href).searchParams;
  lang = query.get('lang') === 'en' ? 'en' : 'zh';
  view = views.has(query.get('view')) ? query.get('view') : 'overview';
}
function route(nextView, nextLang, push = true) {
  view = views.has(nextView) ? nextView : 'overview';
  lang = nextLang === 'en' ? 'en' : 'zh';
  const url = new URL(location.href); url.searchParams.set('lang',lang); url.searchParams.set('view',view);
  url.hash = '';
  if (push) history.pushState({},'',url); else history.replaceState({},'',url);
  render();
}
function applyCopy() {
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.title = lang === 'zh' ? 'awesome ICL — 冻结策略的经验迁移审计' : 'awesome ICL — Experience, under examination';
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const value = copy[lang][el.dataset.i18n];
    if (value === undefined) return;
    const lines = value.split('\n'); el.replaceChildren();
    lines.forEach((line,i) => { if(i) el.append(document.createElement('br')); el.append(document.createTextNode(line)); });
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => { el.placeholder = copy[lang][el.dataset.i18nPlaceholder]; });
  $('#language-toggle').textContent = lang === 'zh' ? 'EN' : '中文';
  $('#language-toggle').setAttribute('aria-label',lang === 'zh' ? 'Switch to English' : '切换到中文');
  $('#navigation').setAttribute('aria-label',lang === 'zh' ? '主导航' : 'Main navigation');
  $('#close-dialog').setAttribute('aria-label',copy[lang].close);
  document.querySelectorAll('[data-view]').forEach(link => {
    link.href = `?lang=${lang}&view=${link.dataset.view}`;
    if (link.closest('nav')) { if(link.dataset.view === view) link.setAttribute('aria-current','page'); else link.removeAttribute('aria-current'); }
  });
  document.querySelectorAll('[data-filter]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.filter === filter)));
  document.body.className = `page-view ${view}`;
  document.querySelectorAll('.view-section').forEach(section => section.hidden = !section.dataset.views.split(' ').includes(view));
}
function badge(status) { return node('span',copy[lang][status === 'in_progress' ? 'inProgress' : status],`badge ${status}`); }
function renderCondition() {
  if (!data) return;
  $('#condition-name').textContent = condition;
  $('#condition-description').textContent = t(data.conditions[condition]);
  document.querySelectorAll('[data-condition]').forEach(button => { const selected = button.dataset.condition === condition; button.classList.toggle('selected',selected); button.setAttribute('aria-pressed',String(selected)); });
}
function renderEvidence() {
  if (!data) return;
  const query = $('#evidence-search').value.trim().toLocaleLowerCase();
  const records = data.records.filter(record => (filter === 'all' || record.status === filter) &&
    [t(record.title),t(record.summary),record.spec_id,record.metric].join(' ').toLocaleLowerCase().includes(query));
  const grid = $('#evidence-grid'); grid.replaceChildren();
  records.forEach(record => {
    const card = node('article',undefined,'evidence-card'); card.dataset.record = record.id;
    const top = node('div',undefined,'card-top'); top.append(badge(record.status),node('span',record.spec_id,'mono')); card.append(top);
    card.append(node('h3',t(record.title)),node('p',t(record.summary)),node('div',record.metric,'record-metric'),node('div',t(record.metric_label),'metric-label'));
    const bottom = node('div',undefined,'card-bottom'); const button = node('button',copy[lang].details); button.type = 'button'; button.addEventListener('click',()=>openRecord(record.id));
    const time = node('time',record.date); time.dateTime = record.date; bottom.append(button,time); card.append(bottom); grid.append(card);
  });
  $('#empty-state').hidden = records.length > 0;
}
function renderDialog(record) {
  const target = $('#dialog-content'); target.replaceChildren(); target.append(badge(record.status),node('h2',t(record.title)),node('p',t(record.summary)));
  target.append(node('h3',copy[lang].observations)); const list = node('ul'); record.observations.forEach(value=>list.append(node('li',t(value)))); target.append(list);
  target.append(node('h3',copy[lang].limits),node('p',t(record.limits)),node('h3',copy[lang].nextAction),node('p',t(record.next)));
  const provenance = node('div',undefined,'record-provenance'); provenance.append(node('strong',copy[lang].provenance));
  provenance.append(node('div',`${record.date} · ${record.spec_id} · ${record.provenance.source_type}`));
  if (record.provenance.review_checks) provenance.append(node('div',`${copy[lang].reviewChecks}: ${record.provenance.review_checks.join(' / ')}`));
  const hash = record.provenance.review_publication_sha256 || record.provenance.source_sha256;
  if (hash) provenance.append(node('code',`SHA-256: ${hash}`)); target.append(provenance);
}
function openRecord(id) {
  const record = data?.records.find(item=>item.id === id); if (!record) return;
  dialogRecord = id; renderDialog(record); $('#evidence-dialog').showModal();
}
function render() {
  applyCopy();
  if (!data) return;
  $('#current-summary').textContent = t(data.current);
  $('#snapshot-date').textContent = `${copy[lang].updated} · ${new Date(data.updated_at).toISOString().slice(0,10)} UTC`;
  renderCondition(); renderEvidence();
  const protocol = $('#protocol-cards'); protocol.replaceChildren(); data.protocol.forEach(item=>{const card=node('article',undefined,'protocol-card');card.append(node('h3',t(item.title)),node('p',t(item.text)));protocol.append(card);});
  const table = $('#condition-table'); table.replaceChildren(); data.groups.forEach(item=>{const row=node('tr');[t(item.name),String(item.count),item.memory,t(item.extra)].forEach(value=>row.append(node('td',value)));table.append(row);});
  const timeline = $('#timeline'); timeline.replaceChildren(); data.timeline.forEach(item=>{const entry=node('li',undefined,item.status);const time=node('time',item.date);time.dateTime=item.date;entry.append(time,node('h3',t(item.title)),node('p',t(item.text)));timeline.append(entry);});
  $('#next-title').textContent=t(data.next.title);$('#next-description').textContent=t(data.next.description);
  const gates=$('#gates');gates.replaceChildren();data.gates.forEach(item=>{const entry=node('div',undefined,'gate');entry.append(node('span',t(item.label)),node('span',t(item.status)));gates.append(entry);});
  const references=$('#reference-links');references.replaceChildren();data.references.forEach(item=>{const url=new URL(item.url);if(url.protocol!=='https:')return;const link=node('a');link.href=url.href;link.target='_blank';link.rel='noopener noreferrer';link.append(node('span',item.title),node('span','↗'));references.append(link);});
  const repository=$('#repository-link');repository.hidden=true;
  if(data.repository_url && /^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$/.test(data.repository_url)){repository.href=data.repository_url;repository.hidden=false;}
  if(dialogRecord && $('#evidence-dialog').open)renderDialog(data.records.find(item=>item.id===dialogRecord));
}
document.querySelectorAll('[data-view]').forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;event.preventDefault();route(link.dataset.view,lang);window.scrollTo(0,0);}));
$('#language-toggle').addEventListener('click',()=>route(view,lang==='zh'?'en':'zh'));
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{filter=states.has(button.dataset.filter)?button.dataset.filter:'all';applyCopy();renderEvidence();}));
document.querySelectorAll('[data-condition]').forEach(button=>button.addEventListener('click',()=>{condition=button.dataset.condition;renderCondition();}));
$('#evidence-search').addEventListener('input',renderEvidence);
$('#close-dialog').addEventListener('click',()=>$('#evidence-dialog').close());
$('#evidence-dialog').addEventListener('close',()=>{dialogRecord=null;});
$('#evidence-dialog').addEventListener('click',event=>{if(event.target===$('#evidence-dialog')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();}});
window.addEventListener('popstate',()=>{readRoute();render();});
readRoute();applyCopy();
fetch('data/progress.json').then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json();}).then(snapshot=>{
  if(snapshot.schema!=='awesome-icl.public-progress.v1'||!Array.isArray(snapshot.records)||snapshot.records.some(record=>!states.has(record.status)))throw new Error('Invalid public snapshot');
  data=snapshot;render();document.documentElement.dataset.ready='true';
}).catch(error=>{console.error('Public snapshot unavailable:',error.message);$('#load-error').hidden=false;document.documentElement.dataset.ready='error';});

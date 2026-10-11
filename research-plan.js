'use strict';
const $ = selector => document.querySelector(selector);
const el = (tag,text,className) => {const item=document.createElement(tag);if(text!==undefined)item.textContent=text;if(className)item.className=className;return item;};
const copy={
  zh:{hiddenStimulus:'程序图：侧标记未知',visibleStimulus:'程序图：补看后的信息',packLink:'八个离散视觉输入包 ↗',packLimits:'输入权限与限制 ↗',symbolicLink:'30个符号控制结果 ↗',skip:'跳到内容',archive:'原方案与记录',method:'具体方法',experiments:'最小实验',sources:'查新依据',start:'查看第一项实验 ↗',full:'完整中文方案 ↗',exampleLabel:'一个能讲清楚的例子',methodLabel:'只改一个机制',methodTitle:'输入、选择、执行。',pilotLabel:'先反证，再投入',pilotTitle:'最小实验和停止条件。',baselineCaption:'六组必要对照：最优规划另作成本下界',baseline:'对照',question:'它排除什么解释',stop:'什么时候应停止',evidenceLabel:'实际完成的工作',evidenceTitle:'分析证据与待做实验分开。',backupLabel:'有条件的备选',sourcesLabel:'直接前作',sourcesTitle:'贡献要越过这些工作。',error:'方案数据加载失败。',footer:'公开研究记录 · 方案尚待闭环验证'},
  en:{hiddenStimulus:'Drawn stimulus: side mark unseen',visibleStimulus:'Drawn stimulus: information after inspection',packLink:'Eight discrete input packs ↗',packLimits:'Input permissions and limits ↗',symbolicLink:'Thirty symbolic controls ↗',skip:'Skip to content',archive:'Earlier design & records',method:'Method',experiments:'Minimum experiment',sources:'Prior work',start:'View the first experiment ↗',full:'Full proposal in Chinese ↗',exampleLabel:'One concrete example',methodLabel:'Change one mechanism',methodTitle:'Input, selection, execution.',pilotLabel:'Falsify before scaling',pilotTitle:'Minimum experiments and stop rules.',baselineCaption:'Six necessary controls; optimal planning is a cost lower bound',baseline:'Control',question:'What it rules out',stop:'When to stop',evidenceLabel:'Work actually completed',evidenceTitle:'Separate analysis from robot results.',backupLabel:'Conditional alternative',sourcesLabel:'Closest prior work',sourcesTitle:'The contribution must go beyond these.',error:'Research plan data could not load.',footer:'Open research notebook · Closed-loop validation pending'}
};
let lang=new URL(location.href).searchParams.get('lang')==='en'?'en':'zh';let data;let selected=0;
const t=value=>value[lang];
function fill(selector,value){$(selector).textContent=t(value);}
function renderCase(){
  const tabs=$('#case-tabs');tabs.replaceChildren();
  data.example.cases.forEach((item,index)=>{const button=el('button',t(item.label));button.type='button';button.setAttribute('aria-pressed',String(selected===index));button.addEventListener('click',()=>{selected=index;renderCase();});tabs.append(button);});
  const flow=$('#case-flow');flow.replaceChildren();data.example.cases[selected].stages.forEach((stage,index)=>{const card=el('article');card.append(el('span',`0${index+1}`,'mono'),el('h3',t(stage.title)),el('p',t(stage.text)));flow.append(card);});
}
function render(){
  document.documentElement.lang=lang==='zh'?'zh-CN':'en';
  document.querySelectorAll('[data-copy]').forEach(node=>node.textContent=copy[lang][node.dataset.copy]);
  $('#plan-language').textContent=lang==='zh'?'EN':'中文';$('#plan-language').setAttribute('aria-label',lang==='zh'?'Switch to English':'切换到中文');
  $('#archive-link').href=`index.html?lang=${lang}&view=proposal`;
  if(!data)return;
  [['#plan-title',data.title],['#plan-intro',data.intro],['#plan-status',data.status],['#example-title',data.example.title],['#example-scope',data.example.scope],['#case-limit',data.example.limits],['#method-scope',data.method_scope],['#budget',data.budget],['#stop-text',data.stop],['#review-limit',data.review_limit],['#backup-title',data.backup.title],['#backup-intro',data.backup.intro],['#backup-gate',data.backup.gate],['#novelty-summary',data.novelty_summary]].forEach(([selector,value])=>fill(selector,value));
  $('#plan-date').textContent=`2026-10-11 / ${lang==='zh'?'ARIS 重新选题':'ARIS research rethink'}`;
  const metrics=$('#plan-metrics');metrics.replaceChildren();data.metrics.forEach(item=>{const row=el('div');row.append(el('strong',String(item.value)),el('span',t(item.label)));metrics.append(row);});
  const steps=$('#method-steps');steps.replaceChildren();data.steps.forEach(item=>{const row=el('li');const body=el('div');body.append(el('h3',t(item.title)),el('p',t(item.text)));row.append(body);steps.append(row);});
  const pilots=$('#pilot-grid');pilots.replaceChildren();data.pilots.forEach(item=>{const card=el('article');card.append(el('span',t(item.label),'eyebrow'),el('h3',t(item.title)),el('p',t(item.text)),el('p',t(item.decision),'decision'));pilots.append(card);});
  const table=$('#baseline-table');table.replaceChildren();data.baselines.forEach(item=>{const row=el('tr');row.append(el('td',t(item.name)),el('td',t(item.purpose)));table.append(row);});
  const evidence=$('#plan-evidence');evidence.replaceChildren();data.evidence.forEach(item=>evidence.append(el('li',t(item))));
  const priors=$('#prior-grid');priors.replaceChildren();data.priors.forEach(item=>{const url=new URL(item.url);if(url.protocol!=='https:')return;const card=el('article');const link=el('a',item.title+' ↗');link.href=url.href;link.target='_blank';link.rel='noopener noreferrer';card.append(el('h3',item.title),el('p',t(item.covered)),el('p',t(item.delta)),link);priors.append(card);});
  renderCase();document.documentElement.dataset.ready='true';
}
$('#plan-language').addEventListener('click',()=>{lang=lang==='zh'?'en':'zh';const url=new URL(location.href);url.searchParams.set('lang',lang);history.pushState({},'',url);render();});
window.addEventListener('popstate',()=>{lang=new URL(location.href).searchParams.get('lang')==='en'?'en':'zh';render();});
render();
fetch('data/research-plan.json').then(response=>{if(!response.ok)throw Error(`HTTP ${response.status}`);return response.json();}).then(snapshot=>{if(snapshot.schema!=='awesome-icl.research-plan.v1')throw Error('Invalid plan schema');data=snapshot;render();}).catch(()=>{$('#plan-error').hidden=false;document.documentElement.dataset.ready='error';});

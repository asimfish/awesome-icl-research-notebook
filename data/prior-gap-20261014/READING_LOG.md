# 原文阅读覆盖与访问边界

2026-10-14。以下记录是本轮核对的章节，不能解释为逐页完整复现，也不声称检索穷尽所有前作。源PDF/HTML只用于本地阅读，不发布全文。

| 名称 | 核对范围 | 访问 |
|---|---|---|
| ReSYNC v2（2026-10-08） | §3–4、5的协议、6、附录D/J/H；K新增替代采样、接触丰富任务和视觉识别；与v1对照 | 两版arXiv HTML本地与Web |
| Zeva v2 | §III记忆更新／检索、IV-A/E/F、V；尤其跨任务替换协议 | arXiv HTML本地与Web |
| OHCAM | 公式1–5、量化假设、实验采集／噪声协议、B规划预算、D传感／技能 | arXiv HTML本地与Web |
| PACTS | III–IV接口、VI重规划实例、VII作者局限 | arXiv HTML本地与Web |
| DICP | §3–6训练／规划／尺度／上下文；Alg.3 | arXiv HTML本地；主记录经Web核对 |
| DPT | §3部署与查询监督、§6覆盖／拟合理论；相关bandit讨论 | arXiv HTML本地与Web |
| DREAM | §3–4、6的目标条件探索、训练步数口径；附录B Cooking without goals实际协议 | arXiv HTML本地与Web |
| VariBAD | §2–3 Bayes-adaptive设定与近似推断 | arXiv HTML本地；主记录经Web核对 |
| PSGI/MTSGI | §3–4 option、completion／eligibility、CART／先验共享 | arXiv HTML本地；主记录经Web核对 |
| SAM | Problem statement、Inference rules中的输入与安全／保守性 | arXiv HTML本地；主记录经Web核对 |
| OLAM | §2–3动作更新和观察、§6边界 | IJCAI正式PDF本地 |
| GLIB | §3–5无外部目标／奖励的探索协议与goal/action babbling | 作者正式论文PDF本地；Web方法摘录 |
| Stochastic relational rules | §1–2动机、完全观察接口、随机／噪声规则与派生概念存在性 | CSAIL作者PDF本地；Web主记录 |
| REX | §2–4给定奖励、概率规则、置信度和探索／利用 | JMLR正式PDF本地与Web |
| Learning Guided Planning | Background、Integrating Planning and Learning、失败／成本更新及实验段落 | 作者正式PDF本地与Web |
| Parameterised execution diagnosis | §III–V映射、局部修正、把手抓取及未来增量更新边界 | arXiv HTML本地；Web主记录 |
| FAVOR/FaRe | 方法、当前任务恢复协议和结果解释 | arXiv HTML本地；原文按篇检查 |
| NOLAM | 正式PDFBackground／Method、噪声定义与随机变量建模 | Web可读；本地下载经代理失败，OpenReview备用返回403 |
| Counter-example model repair | 正式发表页面摘要 | 完整PDF的本地／Web访问失败；仅摘要级，不推断内部限制 |

SOURCE_INDEX.json中19个成功本地捕获，1个下载失败条目；additional_access_notes另记NOLAM与模型修复页面。EMG和ChipMEM在广检中出现，未进行原文方法审计，未据它们声称机器人能力或新颖性结论。一次猜测的ICAPS编号31488指向无关论文，已排除；实际NOLAM编号31493。

本轮修正了以下容易制造虚假gap的说法：ReSYNC已解决复用概念歧义，并测试反向课程和带噪声初始谓词；OHCAM已有噪声及真实执行误差处理，不是只用成功数据或只取一个假设探索；Zeva已有跨任务正证据；DICP使用POMDP设定和模型规划；DREAM已处理任务相关信息，并含探索时目标未公布的变体。

版本复核：ReSYNC最新v2为10月8日；Zeva为9月22日v2；OHCAM／PACTS主记录目前为v1。ReSYNC v2新增平稳随机动力学说明、关系增广的拒绝采样替代、接触丰富Flip组合任务以及SAM3/GPT-5.6视觉识别失败对象的初测；依此修正不足表述。附录J仍明确对象投影的信息损失，K.3仍注明带识别误差的端到端恢复／规划待验证。v1捕获另存，不能把新增内容隐藏为原v1已读事实。

分析采用ARIS research-review证据核对原则，未调用原生Codex MCP或其他外部审稿人，不能宣称通过了该skill的外部接受流程。所有可能不足均保留为未测假设，本轮未运行方法适配或效能试验。

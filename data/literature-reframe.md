2026-10-12更新：原提案已进入实测；15策略训练完成，主经验完成率门槛失败。请读[实验结果](pilot-results.md)与[论文故事](paper-story-zh.md)。以下保留2026-10-11提案原文与历史边界。

# 当前 ICL 主问题的前作与边界

2026-10-11；以论文原文/作者项目页为技术依据。调研仓库和 Robotensor 文章用于问题地图，不把二手汇总数字作为独立实验结论。新增检索围绕算法蒸馏、自己的交互、学生分布、部分可观测教师、恢复迁移和经验选择展开；不声称完成穷尽检索或 ARIS 机器文献核验。

| 前作 / 一手来源 | 已经解决或明确提出的内容 | 我们不能再声称的创新；仍需检验的区别 |
|---|---|---|
| [RL²](https://arxiv.org/abs/1611.02779) | 递归状态跨回合执行快速学习，外层 RL 训练学习算法 | 跨回合记忆不是新贡献；机器人操作的反馈、预算与规则迁移需具体测试 |
| [Algorithm Distillation](https://arxiv.org/abs/2210.14215) | 从 RL 学习历史训练序列策略，冻结参数在上下文中改善 | “蒸馏学习过程而非最终专家”已有；不能仅换成机器人再命名 |
| [DPT](https://arxiv.org/html/2306.14892v1) | 最优动作监督可产生上下文 RL 与后验采样；理论区分 compliant 数据生成 | 不能声称动作监督原则上只能识别任务；隐藏任务泄露的原则也已有分析 |
| [AdA](https://arxiv.org/abs/2301.07608) | 开放任务分布上的大规模 meta-RL、跨试次适应 | 多任务 RL 加长记忆不是新学习范式；规模与操作成本不可直接类比 |
| [DAgger](https://arxiv.org/abs/1011.0686) | 在学生访问分布上聚合专家动作标签 | student-state labeling 本身不构成“真正 OPD”的独有贡献 |
| [RoboTTT](https://arxiv.org/html/2607.15275v1) / [作者项目](https://research.nvidia.com/labs/gear/robottt/) | 长上下文快权重；失败进入上下文，人的纠正作为动作目标；学得在线纠正 | failure→correction 蒸馏已有；其快权重测试时梯度更新与严格无梯度 ICL 分开比较；不能复现作者 16 GB200 训练作为便宜基线 |
| [Zeva](https://arxiv.org/html/2608.30880v1) | 自己的动作—效果编码、两时间尺度记忆、冻结策略注入；有跨任务相似信号替换实验 | 自反馈、因果记忆、跨任务信号迁移都已有；不能笼统称前作只会当前恢复；需测试新机制与新目标组合上的学习 |
| [PhysMem](https://arxiv.org/abs/2602.20323) / [作者项目](https://phys-mem.github.io/) | 交互、假设、验证、物理原则记忆，适应条件变化 | “验证失败经验后变成规则”已有；需区分外部记忆的能力与学生学得更新算法 |
| [RoboICL](https://arxiv.org/abs/2609.34261) | 示范与自身执行记忆共享 observation–action–receipt–observation 接口，锚点记忆 | 加 receipt、失败反馈或历史锚点不是新贡献；是否学得新部署映射需另测 |
| [World–Task Factorization](https://arxiv.org/abs/2606.02027) | 世界估计器与任务成本结构的因式分解 | 仅拆世界/任务的图不是创新；部署时如何利用新经验另属问题 |
| [Privileged POMDP RL](https://arxiv.org/abs/2412.00985) | 分析特权信息训练与专家蒸馏的局限，提出信念加权方法 | 特权老师不一定可模仿已经是已知问题；不能把信息不公平当全新发现 |
| [Realizable Students](https://arxiv.org/abs/2505.09546) | 策略查询、恢复起点处理老师/学生观察不对称 | 学生恢复分布与适时查询已有具体方法；需更强的冻结适应或任务规则区别 |
| [Guided Policy Optimization](https://arxiv.org/abs/2505.15418) | 特权 guider 与 learner 对齐共同训练，部分观察控制 | “让老师对齐学生信息”也有直接前作；固定专家与学习算法不能概念混用 |
| [DREAM](https://arxiv.org/html/2008.02790v3) | 解耦探索与利用；§6 明确设置未来不同目标/配方与重置回合 | 跨目标获得可复用信息已有；不能仅以“以后换目标”声称新问题或方法 |
| [Symmetric Meta-RL](https://arxiv.org/abs/2109.10781) | 用对称结构改善任务、观察/动作重排列的泛化 | 新标签重排列要有此强基线，不能用它轻易宣布学到通用算法 |
| [Pure Exploration ICL](https://arxiv.org/abs/2506.01876) | ICL 的纯探索与识别最优决策问题 | 无即时奖励的信息动作并非空白；机器人不可逆代价需单独定位 |
| [MTSGI](https://proceedings.mlr.press/v180/sohn22a.html) / [MSGI](https://arxiv.org/abs/2001.00248) | 未知子任务依赖推断和少样本结构迁移 | 未知任务图与结构更新不是空白；依赖图方向必须比较子任务推断方法 |
| [Learning to Explore via Meta-Policy Gradient](https://proceedings.mlr.press/v80/xu18d/xu18d.pdf) | 用实际学生更新前后的回报差优化探索 | 学生可利用的经验价值已有；冻结上下文与跨目标差别不能只靠减去 baseline 的公式证明 |
| [In-Context RLVR](https://aclanthology.org/2026.findings-acl.1523/) | 在语言推理中用 demonstration utility / evidence gain 评价示范教学作用 | “正确数据不等于有效教学数据”与数据效用指标已有；操作中的自主获取/恢复闭环需要具体差异 |

| [E-RL²](https://arxiv.org/abs/1803.01118) | 探索回合通过后续利用回报获得信用，探索回报仍作为观察 | 必须给同样未来目标与任务流，不能只用当前回报弱meta-RL对照 |
| [Hindsight Foresight Relabeling](https://arxiv.org/pdf/2109.09031) | 通过适应后控制回报及上下文critic估计经验效用，重标注已有经验 | 效用critic本身不新；它未改变采集，但我们的新采集估计器也尚未提出 |
| [Can ICL Support Intrinsic Curiosity?](https://arxiv.org/html/2606.19476v1) | 冻结ICL预测器，通过有无观察的反事实未来预测差奖励采集 | 反事实上下文教学价值已有；实际控制效用区别存在，但差分目标本身不新 |
| [PSGI](https://ojs.aaai.org/index.php/AAAI/article/view/20718) | 参数化子任务图推断与向新子任务迁移 | 关系组合与迁移已有，局部学习更新方向需证明结构外推增量 |
| [Filtering Learning Histories Enhances ICRL](https://arxiv.org/abs/2505.15143) | 研究学习历史筛选对上下文RL的影响 | verifier筛选不是空白；我们需隔离可信失败被删后的具体训练后果 |
| [FACT](https://arxiv.org/abs/2608.10232) | 失败感知的上下文训练近邻；本轮主要由jury核对 | 不能把加入失败作为首创；深入算法比较需继续逐节核查 |

## 用户提供的系统故事怎样使用

[awesome_agentic_robot](https://github.com/asimfish/awesome_agentic_robot) 的学习对象上移与 verifier 瓶颈是有价值的系统视角，但其中 [HARVEST 提案](https://github.com/asimfish/awesome_agentic_robot/blob/main/docs/proposal/PROPOSAL_agent_data_engine_zh.md) 已组合 agent 采集、独立验证、阶段与失败标签、动作头回流。不能靠再串 DP/offline RL/online RL/OPD 声称方法创新。它的源论文数字应逐篇核验，不合并为我们的成绩。

[awesome_ICL](https://github.com/asimfish/awesome_ICL) 含 Zeva、RoboTTT 与算法蒸馏谱系。主问题应追问“自己的交互如何形成可迁移适应”，而不是长期重复在一个已知规则的感知选择玩具中优化调度器。

[Robotensor ICL 文章](https://www.robotensor.ai/blog/what-in-context-robot-learning-asks) 分开专家示范与自身多回合 RL 两轨；[task-space 文章](https://www.robotensor.ai/blog/the-missing-variable-in-robot-benchmarking-the-task-itself) 区分连续场景变化与任务目标/依赖变化；[2026 总览](https://www.robotensor.ai/blog/robotics-in-2026-from-imitation-to-self-improving-physical-intelligence) 把 ICL/记忆与 VLA/WAM 的预训练路线分开。采用这些区分，不能把“任何多回合提升都是 task learning”或“所有参数更新都是 ICL”反推为事实。

## 最强替代解释

更多重试；新物理观测；老师接管；完整隐藏规则进入上下文；历史泄露任务 ID；只是调用预训练技能；恢复策略反应更好但下一回合不变；更大模型/更长上下文/更多采集预算；评测 verifier 的真值被当部署反馈。每一种都要靠相应的公平实验，而非措辞排除。

# 方法级查新边界

这里只记录已核对的机制，不提供原创性接受证书。arXiv 的存在核验也不证明方法新颖。部分分镜只读摘要；根代理另读下列直接方法部分以纠正判断。

| 原始来源 | 核对范围与实际机制 | 本轮不能主张的内容 |
|---|---|---|
| [RAD](https://arxiv.org/html/2609.35333v1) | 方法工作/长时记忆、压缩器及门控递归更新；AD 动作预测损失联合训练 | 递归压缩、学习记忆更新、冻结部署权重本身 |
| [PSGI](https://arxiv.org/pdf/2203.15034) | 参数化前置条件/作用，任务结构泛化；接口含 completion/eligibility（分镜阅读全文接口核对） | 任务图、关系复用、泛化到未见实体本身；比较需匹配接口 |
| [OHCAM](https://arxiv.org/html/2608.30955v1) | 方法：似然/复杂度评分、条件假设动态扩展、量化效果、BALD 想象轨迹探索；非纯 eligibility oracle 接口 | 在线从后果修正规则、复杂条件、主动消歧本身 |
| [Twin](https://arxiv.org/html/2608.14490v1) | 方法：从 raw grid/命令后果写 executable twin，Validate 对所有日志执行重放；随后探索/规划 | 可执行任务知识、反例修补、防止旧转移退化本身 |
| [PatchWorld](https://arxiv.org/html/2605.30880v1) | §3–4：POMDP belief 程序，按动作/结果筛选例子，typed counterexamples，全验证集 replay gate；重构与决策效用可不同 | 程序修补、对比经验筛选、验证反馈、保持旧经验本身 |
| [Symbolic-Geometric Repair](https://arxiv.org/pdf/2105.06537) | 本轮根只核对摘要；分镜读取局部规则修补方法 | 机器人里用反例增删符号条件的宽泛主张；未完成根全文审计 |
| [ICQL](https://arxiv.org/html/2509.24067v2) | §3.2–3.3：检索局部转移，线性注意力预条件 TD 迭代，组合局部 Q | 从上下文组合行为价值本身 |
| [DREAM](https://proceedings.mlr.press/v139/liu21s/liu21s.pdf) | 原始方法/作者项目：task-relevant problem encoding，探索获取后来利用所需的潜变量 | 为未来目标采集有用信息、只编码任务相关知识本身 |
| [OCEAN](https://proceedings.mlr.press/v124/ren20a/ren20a.pdf) | Fig1/§3：全局多 episode 后验与局部 recurrent 子任务推断、不同潜变量分布、在线更新 | 全局/局部任务状态拆分、在线组合任务推断本身 |
| [SimpleICL](https://arxiv.org/html/2609.38173v1) | §3/4：语义区分数据、跨组 pairing、视频上下文及未来预测 | ICL 数据需消除捷径、不同动作/对象/顺序对比本身 |
| [IIT](https://proceedings.mlr.press/v162/geiger22a/geiger22a.pdf) | Eq4/Fig1d：对齐高层/神经变量，交换内部变量，并匹配反事实输出；方法可用于展开的动态计算图 | 交换监督、因果结构蒸馏本身；不能以“动态而非静态”认定区分 |
| [Causal Distillation](https://arxiv.org/html/2112.02505v2) | 原始正文：学生模仿教师干预计算而非仅输出/hidden states | 蒸馏知识内部更新过程的宽泛主张 |

新增事实：我们最初想把 counterexample editing 当成主要算法，已被直接前作收紧。第二轮 R1 更新对象交换也面临 IIT/因果蒸馏强近邻。当前没有方法被确认为新；11 个候选均保留，当前重点是建立最小必要性而非扩大系统。

当前已存在的 own-stream 数字只表明保留过去经验有行为收益。它们没有区分任务识别、关系学习、外部程序知识与控制状态适应，也不构成本轮候选的实验支持。

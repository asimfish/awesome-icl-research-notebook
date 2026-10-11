# 本轮深入思考的约束与新检索

2026-10-11。延续A3，未重做已完成9候选生成、30符号控制或八包视觉刺激。现有研究仍same-family/provisional，冻结策略调用和机器人新回合0。使用ARIS research-lit的针对性补查及research-review的后续审查，不启动第二轮全域选题。

新增原始前作：

- See2Act，Learning to See While Learning to Act（2026-06，arXiv:2606.23625v1），原文§1、§3.1–3.4、§4.1。从离线操作示范与渲染相机轨迹训练视角—动作耦合，不能再主张首次从示范学习看哪里。作者使用动作关键帧监督相机轨迹；测试时冻结不等于用新任务示范做in-context绑定。https://arxiv.org/html/2606.23625v1
- ActiveUMI（2025-10，arXiv:2510.01607v1），项目页与原文。同步记录人类观察/操纵、学习动态视角。‘学习老师的主动观察’已有工作。https://arxiv.org/html/2510.01607v1 ; https://activeumi.github.io/
- CIVIL（2025-04原版，2026-09期刊版），原文§III–IV，利用人类标记和语言解释因果相关特征，并训练策略与因果编码；任务相关特征不是新概念。不是未经训练的few-shot上下文适应。https://arxiv.org/html/2504.17959v1 ; https://link.springer.com/article/10.1007/s10514-026-10266-3
- Causal Transfer for Imitation Learning and Decision Making under Sensor-Shift（AAAI2020），已研究老师自身传感、观察老师的传感、学生传感之间的差异与可识别性。当前只取得官方摘要，不以未读到的实验作排除判决。https://ojs.aaai.org/index.php/AAAI/article/view/6571
- Causal Confusion in Imitation Learning（NeurIPS2019），原文摘要与引言/因果结构：相关特征不等于动作原因，改变信息可能导致错误策略。不能把相关性与因果性区别当本轮原创。https://arxiv.org/html/1905.11979v1
- 用户Robotensor博客的task recognition / task learning区分，作为问题来源而非新颖性证据。https://www.robotensor.ai/blog/what-in-context-robot-learning-asks

本轮执行检索式（2026-10-11）：
1. robot learning active perception information gathering policy from demonstrations imitation task conditioned
2. robot in context learning demonstration epistemic actions sensing policy information gathering
3. learning from demonstrations active sensing task relevant features causal imitation robot
4. "imitation learning" "information gathering" "demonstrations" robot
5. "in-context" "active perception" robot demonstrations
6. "causal confusion" "imitation learning" de Haan paper
7. "inverse" "POMDP" "demonstrations" "sensing" robot

需要更严厉地检验的三件事：
1. 二选一颜色/符号规则可能主要是识别预先存在的规则；加入每轮新随机的映射并保留识别性，才更强地要求使用当前示范。不能把留出新外观值、却从未展示其任意映射算作可解任务。
2. 老师曾经看过哪里不能直接决定学生该看哪里；当前信息足够、获取途径换了、未知变量不影响当前决策时，都应改变动作。
3. 任务规则不明确与当前物体状态未知不是同一种缺口。多拍当前物体无法识别两个都与示范一致但在该物体上冲突的任务；合成歧义控制要允许defer/可选教学澄清，不能制造不可能任务再计作模型失败。

这不是新主动感知算法。目前最合理的贡献候选是新任务上下文中信息取得行为的严格能力诊断；是否有新现象仍未测。

## 对SimpleICL再读原文后的边界

本轮再次读取 [SimpleICL](https://arxiv.org/html/2609.38173v1) §3.1–3.2、§4.3.2–4.3.3。它已明确对象位置变化时不复制人手轨迹，并以跨组配对、同场景不同动作/顺序/affordance来解除意图与布局绑定。仅改变学生观察运动的左右方向，不能证明超越这些不变性设计。仍可测试的具体差别是：同一任务、同一终态目标下，只改变学生合法信息历史，最优动作由观察变为直接执行；条件规则中全局相关变量对当前动作不再必要。原文已读部分没有展示这两种干预，但这不是全领域无前作的证明，也不是能力缺口结果。

还须承认：当前12例把可见性途径作为人工表格给定，老师look_left只是注释。仅凭这些输入正确选动作，不能声称已从视觉示范学出老师为何观察。任务真值表加经典决策树足以解题。

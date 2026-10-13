# 重复反馈与交互记忆的直接前作

2026年10月14日。查新发生在本轮实验设计冻结后，没有据此调参或选择结果。

## 交互经验复用

[Zeva](https://arxiv.org/html/2608.30880v2) 的III节使用state/action/effect的GRU编码、双时间尺度记忆和冻结策略的context conditioning。IV-F测试跨任务信号检索与替换。因此，“自己的交互形成记忆并用于其他任务”已是直接前作。该实验不等同于未执行目标关系的普遍可识别性证明，后者也不能仅凭我们的符号结果宣称。

## 额外计算与实际动作

[Guez等2019](https://proceedings.mlr.press/v97/guez19a/guez19a.pdf) 的2.1与4.3节研究重复内部计算及无环境效果步骤。[Taufeeque等2024](https://arxiv.org/html/2407.15421v2) 的3.2节将Sokoban中的pacing cycles与额外thinking steps进行替换比较。“把外部重复换成内部思考”已有明确前作。我们的去重失败只证实固定输入的局部循环，尚未识别规划计算。

## 当前边界

本轮只实现既有GRU和标准版本空间约束，没有复现Zeva或上述规划模型。此前40项候选及其前作审查保留；本次查新补充直接邻近工作，不将23项旧来源的清单改写为它已经包含这些新来源。

检索式包括recurrent reinforcement learning thinking without acting repeated observations、recurrent policy no-op internal computation、in context robot repeated failures，以及三篇确切题名。上述机制结论核对了主文方法与实验段落。Learning to select computations in recurrent neural circuits只读到bioRxiv摘要；全文抓取受阻，不用于正文机制结论。

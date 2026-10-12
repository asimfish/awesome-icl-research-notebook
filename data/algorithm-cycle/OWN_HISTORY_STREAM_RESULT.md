# Own required-attempt history transfers across new goals

Completed 2026-10-12, after the fresh code gate. Development diagnostic, same family as the previous learned pilot. No new training runs or physical episodes.

The three existing covered-query checkpoints (11/29/47) executed 6 distinct required goal labels per stream, with physical reset before each goal, on 256 closure-disjoint fresh rules and 8 streams per rule. Both arms retained current-action feedback; retain additionally kept its last 12 own earlier-task receipts. No separate collection was charged or performed. All goals were assigned before acting; no success filtering. Failed tasks cost the full 12-command horizon and did not stop the remaining stream. Exactly 73,728 episode branches executed. First-task identities and complete frozen state dictionaries were checked.

| Whole-stream outcome | Erase prior history | Retain own prior history | Paired effect |
|---|---:|---:|---:|
| Commands per 6-task stream | 38.8999 | 30.8200 | saving 8.0799, rule-bootstrap 95% CI [7.5394,8.6083] |
| Completion per assigned task | 96.6715% | 98.6301% | +1.9586 pp, CI [1.4105,2.5527] |
| Blocked non-repeat commands/stream | 15.1937 | 7.6213 | descriptive reduction 7.5724 |
| Repeated completed commands/stream | 0.4639 | 0.1056 | descriptive reduction 0.3582 |

One CPU process, two Torch threads; measured construction/loading/evaluation/bootstrap span 10.2287s (excludes subsequent CSV serialization/reporting). Each stream has one initialization plus five between-task resets in both arms. Actual and capped commands coincide in this run because neither arm issues premature STOP. The uncertainty unit is one rule after averaging 8 streams and 3 checkpoints, with 4,000 paired rule bootstrap draws; coordinate-wise intervals, not a simultaneous deployment gate.

Checkpoint-specific command savings: 8.0181,7.8472,8.3745. Completion deltas: +2.7344,+1.2451,+1.8962 pp. First-task differences are exactly zero; later arm histories diverge, so this is a whole-stream policy intervention, not causal attribution to a particular receipt.

Interpretation: a learned consumer can benefit from experience produced by its own required attempts when solving subsequently assigned goals after reset. This resolves the planned own-history necessity diagnostic positively. It does not identify a relation graph, demonstrate autonomous information acquisition, distinguish task learning from task recognition over the distribution, or establish a new algorithm. The deterministic five-operation family is still nearly solved in retained context. Additional algorithm complexity on this family needs a separately observed failure boundary. This cohort is method-development evidence and cannot become a final held-out test for an algorithm chosen using it.

Raw artifacts: [result.json](results-own-stream/result.json), [episodes.csv](results-own-stream/episodes.csv), [by_task.csv](results-own-stream/by_task.csv), [descriptive_summary.json](results-own-stream/descriptive_summary.json), [fresh code gate](own-stream-code-review.response.md).

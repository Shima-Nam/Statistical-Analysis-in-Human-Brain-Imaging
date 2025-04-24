This repository presents a segment of my work focused on human brain electrophysiology. The study explores EEG data that was collected and preprocessed at the school of Health, Concordia University and is now being structured for linear modeling.

The primary objective is to investigate whether specific brain activations can be identified following a cognitive task, indicating the formation of memory traces. In particular, this project aims to:

- Detect EEG signatures associated with task-induced memory trace formation.

- Determine which frequency bands exhibit such signatures.

- Identify which electrodes show the most prominent task-related activations.

The results of this analysis can provide insight into the neural correlates of memory encoding, with potential implications for cognitive neuroscience and clinical research.

OUTPUT: significant meaningful results in the targeted brain areas

Contrast: M - C
Indicating the neuronal activity when contrasting performing the task vs the baseline of the task
+---+---------+----------+---------+------+---------+
| # | Channel |   Band   |  Diff   |  SE  | p-value |
+---+---------+----------+---------+------+---------+
| 1 |   FC2   | lowgamma | -4.2339 | 1.63 | 0.0094  |
+---+---------+----------+---------+------+---------+

Contrast: M - R
Indicating the neuronal activity when contrasting performing the task vs the rest condition
+---+---------+----------+---------+--------+---------+
| # | Channel |   Band   |  Diff   |   SE   | p-value |
+---+---------+----------+---------+--------+---------+
| 1 |   FC2   |   beta   | -2.6414 |  0.99  | 0.0081  |
| 2 |   C4    | lowgamma | -2.9863 |  1.01  |  0.003  |
| 3 |   CP2   | lowgamma | -3.1265 |  1.14  | 0.0063  |
+---+---------+----------+---------+--------+---------+

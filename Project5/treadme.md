$$
\begin{array}{|c|ccc|l|}
\hline { \text{jump} } & j1 & j 2 & j 3 & \text { effect } \\
\hline  { null } & 0 & 0 & 0 & \text { no jump } \\
\hline { JGT } & 0 & 0 & 1 & \text { if } out\gt0 \text{ jump }\\
\hline { JEQ} & 0 & 1 & 0 & \text{ if } out= 0 \text{ jump } \\
\hline { JGE } & 0 & 1 & 1 & \text { if } out\ge0 \text{ jump } \\
\hline { JLT } & 1 & 0 & 0 & \text{ if } out\le0 \text{ jump } \\
\hline { JNE} & 1 & 0 & 1 & \text { if } out\ne0 \text{ jump } \\
\hline { JLE} & 1 & 1 & 0 & \text { if } out\le0 \text{ jump } \\
\hline { JMP } & 1 & 1 & 1 & \text { Unconditional jump} \\
\hline
\end{array}
$$
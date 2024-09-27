# 关于扭结不变量的区分能力的实验报告

## 序言

- 由于本文主要面向拓扑扭结区分在工程上的应用，因此在数学上难免会有不严谨的地方，希望各位专长拓扑学的读者批评指正。
  - 如果您感兴趣本文的项目、愿意指出本文中存在的问题，欢迎联系 `premierbob AT qq.com` 以获得支持。
- 概述
  - 扭结区分不仅在理论上是一个尚未被彻底解决的问题，在工程上同样是如此。天下没有免费的午餐，具有良好区分能力的扭结不变量往往具有多种等多样的计算上的困难。
  - 例如，从理论上讲，我们确实可以使用 Wirtinger Presentation 区分两个不同的扭结。但不幸的事，这种做法在当下的工业界仍然无法被普及，因为我们能够从理论上证明群表示的等价性是一个不可计算问题。
  - 在未来，我们或许会有数据驱动而非算法驱动的方式解决这一问题。但在当下，我们仍然没有良好的方式利用 Wirtinger Presentation 使用编程的手段区分扭结。
  - 因此，综合考虑了时间复杂度，空间复杂度以及数学上的严谨性。本文采用了 **HOMFLY-PT 多项式**、**Khovanov 同调**以及**扭结补空间体积**三种扭结不变量作为区分不同扭结的依据，在小于等于 11 crossing 的扭结（含非素扭结）集合上衡量了以上三者各自的区分能力。
- 以下三个文件中分别给出了从扭结名称到指定扭结不变量的映射关系：
  - [HOMFLY-PT-reg.txt](./HOMFLY-PT-reg.txt)
  - [khovanov-reg.txt](./khovanov-reg.txt)
  - [volume_info_list-reg.txt](./volume_info_list-reg.txt)
  - 我们的一切分析基于上述三个文件。
- 需要注意的是，其中 volume 的计算使用了 python snappy 中的 Manifold 类中的 volume 函数。
  - 无论被计算的扭结是否是 hyperbolic knot,该函数往往能计算出一个实数作为结果。
    - 根据本文作者的观察，计算素扭结的 volume 时，**对于 non-hyperbolic-knot，该函数的返回值往往接近于零**。
  - 由于这些行为与我们对扭结补空间的体积的理解不符，因此本文作者强烈建议不要使用该函数作为区分扭结的依据。
    - 但由于本文作者没有找到更合适的，计算扭结补空间 volume 的函数库，因此我们在进行实验时**权宜地**使用了该函数库。
    - 具体库的使用请参考： https://snappy.computop.org/
- 我们的统计程序在 [reader.py](./reader.py) 中给出。
  - 我们也非常欢迎读者来校验此统计程序的正确性。
- 本实验中考虑了 1783 种小于等于 11 crossing 的扭结。
  - 其中包含素扭结 1582 个
  - 非素扭结 200 个
  - 平凡扭结 1 个（正如 0 既不是质数也不是合数，我们的话语体系中认为，平凡扭结既不是素扭结，也不是非素扭结）
  - 可以看到，小于等于 11 crossing 时大多数的扭结都是素扭结。
- 在进行实验时我们基于了这一假设构建了我们的非素扭结数据库：
  - 任意一扭结的最小 crossing 数**等于**其各个素分量的最少交叉点数（实际上现有的数学工作只能证明出小于等于，而无法证明大于等于）。
  - 倘若这一假设成立，则我们对小于等于 11 crossing 扭结的枚举是**完备的**。
  - 倘若这一假设并不成立，我们的实验仍然是有价值的，因为我们相信这种枚举方式能够枚举出小于等于 11 crossing 的绝大多数扭结。

## 使用 khovanov 同调以及 HOMFLY-PT 多项式区分扭结

### khovanov 同调的区分能力

- 使用 khovanov 同调作为唯一区分工具时，本质不同的 1783 种扭结被划分为 1549 种不同的等价类。
  - 其中包含一元等价类 1349 个（即，不冲突的情况）。
  - 二元等价类 167 个。
  - 三元等价类 4 个。
  - 四元等价类 1 个。
- 在算法上我们使用了 JavaKhV2 作为 khovanov 同调的计算程序。
  - 相比于 HOMFLY-PT 多项式以及 volume 的计算算法而言，该程序在时间复杂度与空间复杂度上都相对稳定。
  - 因此 khovanov 同调作为我们在**实践中**最主要的使用的扭结区分工具。
    - 什么叫做 “**最主要**的区分扭结的工具”？
      - 每当我们拿到一个扭结、想要知道他的具体类型时，首先我们会计算这个扭结的 khovanov 同调，并将该 khovanov 同调与数据库中的信息进行比对。
      - 倘若此时已经能够唯一确定出一种扭结，那么我们不再需要使用其他不变量进行进一步区分扭结类型。
      - 倘若此时仍然不能区分出唯一的一种扭结，我们会尝试使用 HOMFLY-PT 多项式进行进一步区分。
    - 由于我们总是最先计算扭结的 khovanov 同调，因此在实践中 khovanov 同调被计算的次数最多。

### HOMFLY-PT 多项式的区分能力

- 使用 HOMFLY-PT 多项式作为唯一区分工具时，本质不同的 1783 种扭结被划分为 1669 种不同的等价类。
  - 其中包含一元等价类 1559  个（即，不冲突的情况）。
  - 二元等价类 106 个。
  - 三元等价类 4 个。
- 因此，我们可以不太严谨得说，在小于等于 11 crossing 的扭结上 HOMFLY-PT 多项式对扭结的区分能力与 khovanov 同调基本一致。
  - 甚至略强于 khovanov 同调。
- 但需要注意到的是，我们使用了来自 sagemath 的计算的 HOMFLY-PT 多项式的算法。
  - 当输入扭结的未约简交叉点个数过多时，该算法可能无法在 20 分钟内停止。
  - 出于工程上的考虑，在这种情况下，我们会不再使用 HOMFLY-PT 多项式作为区分扭结的依据。

### 联合使用 khovanov 同调以及 HOMFLY-PT 多项式的区分能力

- 联合使用 khovanov 同调以及 HOMFLY-PT 多项式作为区分扭结的工具时，本质不同的 1783 种扭结被划分为 1677 种不同的等价类。
  - 其中包含一元等价类 1575  个（即，不冲突的情况）。
  - 二元等价类 98 个。
  - 三元等价类 4 个。

- 可以看到 HOMFLY-PT 多项式的引入确实有助于扭结的区分。
  - 与仅使用 khovanov 同调相比，在 HOMFLY-PT 多项式引入后，一元等价类数量略有增多，二元等价类数量略有减少。

## 使用 volume 区分扭结

- 再次声明，本文使用了 snappy 中提供的 Manifold 类中的 volume 函数计算扭结补空间的体积。
  - 该函数对 non-hyperbolic 扭结本不应给出计算结果，本文作者并不了解该函数对 non-hyperbolic 扭结给出的计算结果的具体意义。
  - 以及该计算结果是否能够被视为一种扭结不变量。
- 考虑 volume 的性质：
  - 由于 volume 是一个实数，我们在使用 volume 进行扭结类型区分时会遇到一个困境。
    - 计算机上的所有实数都是使用浮点数近似表示的，因此我们需要给出一个精度误差值 $\varepsilon$，然后断言，若两个扭结计算出的 volume 的差的绝对值如果小于 $\varepsilon$（$\varepsilon > 0$），则认为这两个扭结具有相同的 volume 值。
      - 在实践中我们的实验表明 $\varepsilon=10^{-4}$ 是一个合理的取值。
    - 这种方法看似合理，但却为我们本文的分析带来了很大的困难。
    - 由于 $|x_1-x_2| < \varepsilon$ 在 $x_1, x_2\in \textbf R$ 上只满足自反性、的对称性，而不满足传递性。因此它不是一个等价关系。
    - 我们在上文中对 HOMFLY-PT 多项式以及 khovanov 同调都使用了 “等价类划分的思想” 来分析扭结不变量对扭结的区分能力。这是因为我们能比较方便得从上述两种扭结不变量中导出一个等价关系。但对于 volume，直接使用这种思路是不行的。
  - 另一方面，一个扭结与其镜像扭结一定具有相同的 volume，因此扭结补空间体积一定不能识别出扭结的手性。
    - 对于手性扭结的两种构型而言，使用 volume 一定会得到一致的结果。
    - 但这并不意味着 HOMFLY-PT 多项式以及 khovanov 同调就具有严谨区分手性的能力。
    - 在后面的章节中我们会详细讲述上述两种扭结不变量各自在区分手性的能力上的异同。
- 综合考虑上述两个性质，我们指出，衡量 volume 对扭结区分能力时，我们可以使用两种方式。
  - 第一种方式：我们对计算出的 volume 在十进制下保留三位小数，我们可以证明，倘若 $\varepsilon=10^{-4}$ 是一个合理的取值，则以保留三位小数的 volume 为特征构建等价类在工程上可以作为一种正确的等价类划分方式。
    - 我们可以给出证明：
      - 若不存在具有相同构型的扭结 $K_1, K_2$ 使得在精度误差的作用下 $|\text{volume}(K_1)-\text{volume}(K_2)|\geq 10^{-4}$，则保留小数点后三位的做法一定不会错误地将本来同痕等价的扭结视为不等价。
    - 但是也要看到，这种方法虽然成功得将所有扭结放置在了等价类中，但是它有小概率出错。
    - 另一方面它大大得削弱了 volume 本身对扭结的区分能力。
  - 第二种方式：我们可以枚举所扭结构成的有序对，看其中有多少个不同的有序对的 volume 会被视为相同。

- 另外，由于大量的扭结都是手性扭结，因此这使得 volume 区分能力在统计数据上来看看起来很差。
  - 这使得上文中的评价扭结不变量区分能力的方式对 volume 而言显得“**十分不公平**“。
  - 因此，在本文中，我们仅仅衡量在**不考虑手性意义下**，volume 对小于等于 11 crossing 的**素扭结**的区分能力。

### 第一种方法：有序对意义下衡量 volume 的区分能力

- 在小于等于 11 crossing 的所有扭结中，在不考虑手性的意义下，有 801 种本质不同的素扭结。
  - 因此我们能够构建出 $\binom{801}{2}=320400$ 种扭结组合，这些组合内的两个扭结本质不同。
  - 值得欣慰的是，在上述 320400 个扭结组合中，只有 45 个被错误的认为是同种扭结。
  - 因此我们基本上可以断言，扭结补空间体积确实在理论上，在不考虑手性的前提下，是良好的扭结区分工具。

### 第二种方法：保留三位置有效数字

- 使用保留小数点后三位的思想，我们可以利用 volume 得到一个等价关系。
  - 使用这种衡量方式，本质不同的 801 种素扭结被划分为 749 个等价类。
  - 其中一元等价类 703 个。
  - 二元的等价类 44 个。
  - 三元的等价类 1 个。
  - 七元等价类 1 个（这个等价类即 volume 等于零对应的的等价类，具体原因详见序言）。

## 针对手性的区分能力

- 本节主要讨论 HOMFLY-PT 多项式以及 khovanov 同调各自对于手性素扭结的区分能力。
  - 在考虑手性的意义下，小于等于 11 crossing 的扭结中有 1582 个素扭结。
  - 其中包含 781 对手性素扭结。
  - 以及 20 个非手性素扭结。
- 在本节中，我们只需要关注这  781 对手性素扭结，而不需要关注那 20 个非手性素扭结。
- 对 khovanov 同调而言：
  - 在总共 781 对扭结中，khovanov 同调正确地区分了其中 777 对，有四对扭结的手性无法被区分。
    - 它们是：`['K10a104', 'K10a48', 'K10a71', 'K10a91']`
- 对 HOMFLY-PT 多项式而言：
  - 在总共 781 对扭结中，HOMFLY-PT 的多项式正确地区分了其中的 773 对，有八对扭结的手性仍然无法被区分。
    - 它们是：`['K10a104', 'K10a48', 'K10a71', 'K10a91', 'K10n2', 'K11n24', 'K11n82', 'K9n1']`
- 我们无法断言在任意 crossing 的扭结上 HOMFLY-PT 多项式与 khovanov 同调对扭结手性的区分孰强孰弱。
  - 但在小于等于 11 crossing 的素扭结上
    - HOMFLY-PT 多项式能区分的手性对，khovanov 同调也总能区分。
    - 因此我们认为在小于等于 11 crossing 的素扭结集合上，khovanov 同调对手性的区分能力略强于 HOMFLY-PT 多项式。


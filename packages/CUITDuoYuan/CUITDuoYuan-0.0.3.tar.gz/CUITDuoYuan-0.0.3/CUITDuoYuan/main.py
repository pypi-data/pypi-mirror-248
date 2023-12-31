class Question:
    def __init__(self, question, answer):
        self.question_text = question
        self.answer = answer


question = [
    Question('主成分分析时，对数据进行标准化的过程可能抹杀原始变量离散程度差异。', 'T'),
    Question('主成分分析要求数据来自于正态总体。', 'F'),
    Question('对来自多元正态总体的数据，主成分分析的主成分就是按数据离散程度最大的方向进行坐标轴旋转。', 'T'),
    Question('在主成分分析的过程中，得到的各个主成分的方差依次递减。', 'T'),
    Question('对于两组的判别，最大后验概率法的判别规则可使两个误判概率之和达到最小。', 'F'),
    Question(
        '对于两组皆为正态组及协差阵相同的情形下，两组先验概率相同及两个误判代价也相等时的贝叶斯判别等价于距离判别，也等价于费希尔判别。',
        'T'),
    Question('主成分分析实质上是线性变换，无假设检验。', 'T'),
    Question('一般地说，从同一原始变量的协方差矩阵出发求得的主成分与从原始变量的相关矩阵出发求得的主成分相同。', 'F'),
    Question('选取主成分还可根据特征值的变化来确定。', 'T'),
    Question('求解主成分的过程实际就是对矩阵结构进行分析的过程。', 'T'),
    Question('对于度量单位不同的指标或是取值范围彼此差异非常大的指标，可直接从协方差矩阵出发进行主成分分析。', 'F'),
    Question('主成分分析只是要达到目的的一个中间结果（或步骤），没有实际意义。', 'F'),
    Question('选取主成分还可根据特征值的变化来确定。', 'T'),
    Question('求解主成分的过程实际就是对矩阵结构进行分析的过程。', 'T'),
    Question('对于度量单位不同的指标或是取值范围彼此差异非常大的指标，可直接从协方差矩阵出发进行主成分分析。', 'F'),
    Question('为了使得因子分析的结果更易于解释，进行正交因子旋转，旋转后，新的公共因子仍然彼此独立。', 'T'),
    Question('因子得分是为了考察每一个样品性质之间的关系。', 'F'),
    Question('因子分析中，载荷矩阵中的每一个元素代表的是变量Xi与公共因子Fj之间的关系。', 'T'),
    Question('因子分析中，利用主成分法求解的载荷系数与主成分分析中的主成分线性方程的系数一样。', 'F'),
    Question('因子分析中，公因子Fj的方差贡献表示的是公共因子Fj对于原始数据X中的每一分量Xi（i=1，2，…，p）所提供的方差的总和。',
             'T'),
    Question('利用主成分法得到的因子载荷是唯一的。', 'F'),
    Question('主成分的数目大大少于原始变量的数目。', 'T'),
    Question('Logistic回归对于自变量有要求，度量变量或者非度量变量都不可以进行回归。', 'F'),
    Question('因子分析把变量分成公共因子和独立因子两部分因素。', 'F'),
    Question('因子载荷经正交旋转后，各变量的共性方差和各因子的贡献都发生了变化。', 'F'),
    Question('因子分析只能用于研究变量之间的相关关系。', 'F'),
    Question('主成分分析是将原来较少的指标扩充为多个新的的综合指标的多元统计方法。', 'F'),
    Question('Logistic回归对于自变量有要求，度量变量或者非度量变量都不可以进行回归。', 'F'),
    Question('因子载荷量是指因子结构中原始变量在因子分析时抽取出的公共因子的相关程度。', 'T'),
    Question('主成分分析中，A', 'A.有必要考虑变量的量纲，避免出现“大数吃小数”'),
    Question('关于第一个主成分，下列描述正确的是', 'D.其累积方差贡献率最大'),
    Question('主成分分析中各主成分之间是', 'D.互不相关'),
    Question('在利用主成分分析进行综合评价时，要对样本观测进行一些变换，最常用的是', 'A.同向化变换'),
    Question('为了更充分有效地代表原始变量的信息，不同的主成分应携带不同的信息。以第一、第二主成分Y1\\Y2为例，',
             'C.cov(Y1,Y2)=0'),
    Question('主成分分析的主要任务有', 'B.确定主成分个数'),
    Question('利用主成分分析得到的各个主成分之间为下面哪个选项？', 'D.最小'),
    Question('因子分析中对于因子载荷的求解最不常用的方法是。', 'D.极小似然法'),
    Question('第k个主成分yk的系数向量是下面哪个？', 'B.第k个特征根所对应的特征向量'),
    Question('利用主成分分析得到的各个主成分之间为下面哪个选项？', 'D.互不相关'),
    Question('因子分析把变量分成下列两部分因素。', 'D.公共因子和特殊因子'),
    Question('单纯依靠相关与回归分析，无法判断事物之间存在的因果关系', 'T'),
    Question('距离判别法考虑到了误判之后所造成的损失的差异。', 'F'),
    Question('判别分析最基本要求是分组类型在两组以上且解释变量必须是可测量的。', 'T'),
    Question('在回归分析中，变量间的关系若是非确定关系，那么因变量不能由自变量唯一确定。', 'T'),
    Question('聚类分析仅能进行样本聚类。', 'F'),
    Question('聚类分析属于有指导的学习分类方法。', 'F'),
    Question('进行样品聚类分析时，“靠近”往往由某种距离来刻画。', 'T'),
    Question(
        '类平均法进行系统聚类的的思想是来于方差分析，如果类分得正确，同类样品的离差平方和应当较小，类与类之间的离差平方和应当较大。',
        'F'),
    Question('聚类分析时可通过碎石图确定最终的分类数。', 'T'),
    Question('针对同一多元数据，不同的方法聚类的结果相同。', 'F'),
    Question('系统聚类法中，对于那些先前已被“错误”分类的样品不再提供重新分类的机会。', 'T'),
    Question('K-均值法只能用于对样品的聚类，而不能用于对变量的聚类。', 'T'),
    Question('有序样品的聚类的实质上是需要找出一些分点，将数据划分成几个分段，每个分段看作一类，称这种分类也可称为分割。',
             'T'),
    Question('k均值法的类个数需事先指定。', 'T'),
    Question('进行多元数据的指标聚类时，可根据相关系数或某种关联性度量来聚类。', 'T'),
    Question(
        '最长距离法中，选择最小的距离作为新类与其他类之间的距离，然后将类间距离最小的两类进行合并，一直合并到只有一类为止。',
        'F'),
    Question('K均值聚类分析中，样品一旦划入某一类就不可改变。', 'F'),
    Question('名义尺度的指标用一些类来表示，这些类之间有等级关系，但没有数量关系。', 'F'),
    Question('下图为应用SPSS软件制作的散点图矩阵，图中城镇人口比重与平均预期寿命存在强线性相关性。', 'T'),
    Question('如果相关系数为0，则表明两个变量间不存在线性相关。', 'T'),
    Question('聚类分析的目的就是把相似的研究对象归类。', 'T'),
    Question('判别分析中,若两个总体的协差阵相等,则 Fisher判别与距离判别等价。', 'T'),
    Question('一般而言，不同聚类方法的结果不完全相同。', 'T'),
    Question('在系统聚类过程中，聚合系数越大，合并的两类差异越小。', 'F'),
    Question('下列变量中，属于负相关的是', 'D.价格下降，消费增加'),
    Question('在以下四个散点图中，适用于做线性回归的是？', 'B.①③'),
    Question(
        '假如你在训练一个线性回归模型，有下面两句话：如果数据量较少，容易发生过拟合。如果假设空间较小，容易发生过拟合。关于这两句话，下列说法正确的是？',
        'B.1 正确，2 错误'),
    Question('两个变量与x的回归模型中，通常用R方来刻画回归的效果，则正确的叙述是', 'D.=R方.jpg越小，残差平方和越大'),
    Question('下列说法中正确的是', 'B.人的知识与其年龄具有相关关系'),
    Question(
        '一位母亲记录了儿子3~9岁的身高，由此建立的身高与年龄的回归直线方程为y\'=7.19x+73.93，据此可以预测这个孩子10岁时的身高，则正确的叙述是',
        'D.升高在145.83cm左右'),
    Question('在画两个变量的散点图时，下面哪个叙述是正确的', 'B.自变量在x轴上，因变量在y轴上'),
    Question(
        '在对两个变量x，y进行线性回归分析时，有下列步骤：①对所求出的回归直线方程作出解释; ②收集数据对.jpg，i=1,2,....,n； ③求线性回归方程; ④求未知参数; ⑤根据所搜集的数据绘制散点图。如果根据可行性要求能够作出变量x，y具有线性相关结论，则在下列操作中正确的是',
        'D.②⑤④③①'),
    Question('线性回归中普通最小二乘估计的缺点是', 'D.回归直线被拉向方差大的项；'),
    Question('在回归分析中，代表了数据点和它在回归直线上相应位置的差异的是', 'B.残差平方和'),
    Question('对两变量的散点图拟合最好的回归线，必须满足一个基本的条件是', 'A.回归1.jpg最小'),
    Question('下面哪一项不是判别分析的方法？', 'C.协方差阵判别'),
    Question('决策树中不包含以下哪种结点？', 'C.外部结点（external node）'),
    Question('下面哪一个选项不是判别分析的方法：', 'D.协方差阵判别'),
    Question('三个总体.....x应该归入总体', 'D.G3'),
    Question('设有样本X（0,3），Y（1,2），求XY的欧式距离', 'A.1'),
    Question('使用“最大后验概率准则”得到的贝叶斯判别规则为', 'A.A'),
    Question('以下哪种判别方法既可用于判别分类也可用于分离各组。', 'D.费希尔判别'),
    Question('两组情形下的最小期望误判代价法的判别规则包含三个比值，其中最富有实际意义的是', 'C.误判代价之比'),
    Question('如果对某公司在一个城市中的各个营业点按彼此之间的路程远近来进行聚类，则最适合采用的距离是', 'B.绝对值距离'),
    Question('聚类分析的目的是', 'A.降维'),
    Question('对样本分类还不清楚的时候，适合首先进行哪种分析', 'C.聚类分析'),
    Question('适合对大样本数据进行聚类分析的方法是', 'B.K-均值聚类'),
    Question('根据聚类的对象不同，聚类可以分为', 'A.样本聚类和变量聚类'),
    Question('根据聚类的对象不同，聚类可以分为', 'A.样本聚类和变量聚类'),
    Question('聚类分析中，通常使用（    ）来衡量两个对象之间的相异度', 'A.距离'),
    Question('一项研究中对中国、香港等12 个国家或地区的多项经济指标进行了聚类分析，得到的树状图如下，说法不正确的是',
             'D.分为四类时，日本、中国、马来西亚构成一个类'),
    Question('当不知道数据所带标签时，可以使用哪种技术促使带同类标签的数据与带其他标签的数据相分离？', 'B.聚类'),
    Question('设，则x离μ越远（近）密度越小（大）。度量这里远近的距离应是:', 'C.马氏距离'),
    Question('聚类分析方法中，下列哪种方法也称为快速聚类法。', 'B.Kmeans聚类'),
    Question('不适合对变量聚类的方法有', 'C.K均值法'),
    Question('相关系数为0表明两个变量之间不存在任何关系', 'F'),
    Question('密度函数可以是负的', 'F'),
    Question('当总体G1和G2为正态总体且协方差相等时，选用马氏距离。', 'T'),
    Question('标准化随机变量的协方差阵与原变量的相关系数相同。', 'T'),
    Question('样本相关系数r∈(－1,1)', 'F'),
    Question('密度函数可以是负的。', 'F'),
    Question('如果相关系数为0，则表明两个变量间不存在线性相关。', 'T'),
    Question('一个行列式中某一行（列）所有元素的公因子可以提到行列式符号的外边。', 'T'),
    Question('numpy中产生全1的矩阵使用的方法是empty。', 'F'),
    Question('相关关系是指变量间不确定性的依存关系', 'T'),
    Question('pandas中head(n)的意思是获取最后的n行数据。', 'F'),
    Question('Numpy的ndarray(数组)中，使用shape()来表示数组的维度尺寸。', 'T'),
    Question('Python语言是非开源的语言。', 'F'),
    Question('脸谱图是用脸部特征表达变量间的相关性。', 'F'),
    Question('通过对多变量的脸谱图分析，可以直观地对原始数据资料进行归类或比较研究。', 'T'),
    Question('设要分析的资料共有p个变量，当p值较大时一张雷达图也可以清晰表达各观测之间的接近程度。', 'F'),
    Question(
        '雷达图是目前应用较为广泛的多元资料进行作图的方法，利用雷达图可以很方便地研究个样本点之间的关系并对样品进行归类。',
        'T'),
    Question('星图和星座图很相似，甚至有的文献把两者看成是一回事。', 'F'),
    Question('利用星座图可以方便地对样本点进行分类，再星座图上比较靠近的样本点比较相似，可分为一类。', 'T'),
    Question('多变量的图表示法使资料的呈现方式更直观、更形象，可以作为定量分析的研究结果并形成结论。', 'F'),
    Question('只要变量的指标数目不变，对应脸谱图的特征就不变。', 'F'),
    Question('马氏距离在协差阵为单位阵时退化为欧氏距离。', 'T'),
    Question('马氏距离受单位的影响。', 'F'),
    Question('相关系数度量了两个随机变量之间依赖关系的强弱。', 'T'),
    Question('Cov(X,Y)=0, 称X与Y是不相关的。', 'T'),
    Question('随机向量X的协方差阵是对称矩阵。', 'T'),
    Question(
        '若p维随机向量X的协方差阵存在,且每个分量的方差大于零，则X的相关阵的元素计算公式为:r_ij=(cov(X_i,X_j))/(D(X_i)D(X_j)),i,j=1,2,…,p。',
        'F'),
    Question(
        '设两个随机向量X和Y是相互独立的，F(x,y)为(X,Y)的联合分布函数，G(x)和H(y)分别为X和Y的分布函数，则F(x,y)=G(x)H(y)。',
        'T'),
    Question(
        '设两个随机向量X和Y是相互独立的，f(x,y)为(X,Y)的密度函数，g(x)和h(y)分别为X和Y的密度函数，则f(x,y)=g(x)+h(y)。',
        'F'),
    Question('正态分布的条件分布仍为条件分布。', 'T'),
    Question('相关关系数不会取负值。', 'F'),
    Question('相关系数的绝对值不会大于1。', 'T'),
    Question('若A是退化矩阵，则A-1一定存在。', 'F'),
    Question('若A为p阶对称矩阵，则存在正交矩阵T和对角矩阵Λ=diag(λ_1,λ_2,⋯λ_p)，使得A=TΛT\'。', 'T'),
    Question('若向量x和y的内积为0，则说明向量x和y垂直。', 'T'),
    Question('若A是一个正交矩阵，则A的行列式为1。', 'F'),
    Question('若A和B均为p阶方阵，则|AB|=|A||B|。', 'T'),
    Question('关于 Python 语言的特点，以下选项中描述错误的是', 'A.Python 语言是非开源语言'),
    Question('使用pandas时需要导入下面哪个？', 'A.import pandas as pd'),
    Question('Numpy中矩阵转换为向量用下面哪个函数？', 'B.resize'),
    Question('numpy中向量转成矩阵使用下面哪个函数？', 'A.reshape'),
    Question('下列变量中，属于负相关的是', 'D.价格下降，消费增加'),
    Question('如果正态随机向量X的各分量是相互独立的随机变量,那么随机变量X的协方差阵是下面哪个？', 'B.对角阵'),
    Question('多元正态分布是以下哪项的推广。', 'A.一元正态分布'),
    Question('Numpy的ndarray(数组)中，使用下面哪个来表示数组的维度尺寸。', 'C.shape'),
    Question('有数组 n = np.arange(24).reshape(2,-1,2,2)，n.shape的返回结果是什么？', 'A.(2,3,2,2)'),
    Question('常用统计函数中，mean计算下面的哪个？', 'C.数组的均值'),
    Question('多变量的图表示法不包括', 'C.箱线图'),
    Question('将所有样本点都点在一个半圆里面，根据样本点的位置可以直观地对样本点之间的相关性进行分析的多变量表示图是',
             'A.星座图'),
    Question('利用其可以很方便的研究个样本点之间的关系并对样本进行分类的是', 'C.雷达图和脸谱图'),
    Question(
        '在脸谱图中，脸谱的绘制顺序是脸庞高度、脸庞宽度、脸庞轮廓、嘴唇高度、嘴唇宽度、笑容曲线、眼睛高度、眼睛宽度、头发高度、头发宽度、头发造型、鼻子高度、鼻子宽度、耳朵宽度、耳朵高度共计15项，输入的数据变量依次为X1~X10共计10个变量，则X1表示的脸部特征是',
        'B.脸庞高度和头发造型'),
    Question(
        '将圆平等分并由圆心连接各分点，将所得的p条线段作为坐标轴，根据各变量的取值对各坐标轴做适当刻度，对任意样本点可分别在p轴上确定其坐标，在各坐标轴上点出其坐标并依次连接p个点。这样做出的图是',
        'B.雷达图'),
    Question('设X~N (μ,Σ)，则X离μ越近（远）密度越大（小），度量这里远近的距离应是', 'B.马氏距离'),
    Question('设随机变量X和Y都服从正态分布, 且它们不相关, 则', 'D.X与Y未必独立'),
    Question('用样本的信息推断总体，样本应该是', 'C.总体中随机抽取的一部分'),
    Question('抽样调查的目的是', 'D.样本推断总体特征'),
    Question('设A,B,C均为常数矩阵，随机向量X和Y的均值特征不包括', 'A.E(AX)=AE(X)A\''),
    Question('设A,B,C均为常数矩阵，随机向量X和Y的协差阵D[X]和D[Y]性质包括', 'A.D(AX)=AD(X)A\''),
    Question('就大部分统计问题而言，欧氏距离存在缺点不包括', 'D.与变量的分布特征有关'),
    Question('T分布的均值是', 'A.0'),
    Question('假设检验的一般步骤中不包括', 'C.对总体参数的置信区间作出估计'),
    Question('假设检验是基于何种情况提出来的？', 'A.H0成立'),
    Question('比较两组均值向量，检验一般采用哪种方法', 'A.t检验'),
    Question('进行多元均值检验时，假设H0:μ=μ_0,H1: μ≠μ_0,协方差阵Σ已知且α显著性水平下的分位点为c，拒绝域为：',
             'B.统计量＞c'),
    Question('进行多元均值检验时，假设H0:μ=μ_0,H1: μ≠μ_0,协方差阵Σ未知且α显著性水平下的分位点为c，拒绝域为：',
             'D.统计量＞c'),
    Question('在进行两总体的均值比较时，假设H0:μ_1=μ_2,H1: μ_1≠μ_2,协方差阵Σ相等时，且α显著性水平下的分位点为c，拒绝域为：',
             'D.统计量＞c'),
    Question(
        '在进行两总体的均值比较时，假设H0:μ_1=μ_2,H1: μ_1≠μ_2,协方差阵Σ不相等时，且α显著性水平下的分位点为c，拒绝域为：',
        'B.统计量＞c'),
    Question(
        '在进行两总体的均值比较时，假设H0:μ_1=μ_2,H1: μ_1≠μ_2,协方差阵Σ不相等时，且α显著性水平下的分位点为T_(p,n1+n2-2)^2 (α)，拒绝域为：',
        'A.统计量T^2＞T_(p,n1+n2-2)^2 (α)'),
    Question('在假设检验中，如果p值大于显著性水平α，就认为总体均值与检验值之间？', 'D.无显著差异'),
    Question('设A是3阶方阵，且|A|=-2，则|A^(-1) |=（ ）。', 'D.-1/2'),
    Question('对于任意n阶方阵A,B，总有（ ）。', 'B.|AB|=|BA|'),
    Question('设A=diag(a_11,a_22,⋯,a_pp )且a_ii≠0(i=1,2,⋯p)，以下说法错误的是（ ）。', 'B.矩阵A有小于p个特征向量'),
    Question('设α1，α2，…，αm均为n维向量，那么，下面关于向量的说法正确的是（ ）。',
             'C.若α1，α2，…，αm线性相关，则对任意一组不全为零的数k1，k2，…，km，都有k1α1+k2α2+…+kmαm=0'),
    Question('设a=(2,-4,1)\'，b=(3,5,-1)\'，ab\'的非零特征值为（ ）。', 'B.-15'),
    Question('设有样本X（0,3），Y（1,2），求XY的欧式距离', 'A.根號2'),

    Question('因子分析中，将每个原始变量分解为两个部分，一个部分由所有变量共同具有的少数几个', '公共因子 特殊因子'),
    Question('设X=(x_1,x_2,x_3)为标准化后的随机变量，将其协方差矩阵通过因子分析分解为：',
             'x_1的共同度=0.872,x_1的剩余方差=0.128,公因子F_1与x_1的协方差=0.934'),
    Question(
        '对多元数据X（x1,x2,x3,x4,x5）进行了主成分分析, 样本的特征值λ_1=2.857，λ_2=0.809，λ_3=0.609，λ_4=0.521，λ_5=0.203对应特征向量p1=(0.464,0.457,0.470,0.421,0.421), p1= (0.240,0.509,0.260,-0.526,-0.582)，则第一主成分Y1的计算公式是',
        'Y1=0.464x1+0.457x2+0.470x3+0.421x4+0.421x5'),
    Question('进行K-均值聚类时，碎石图如图所示，则最优的分类数为', '2|3'),
    Question('主成分分析通常把转化生成的综合指标称之为主成分，其中每个主成分都是原始变量的', '线性组合'),
    Question(
        '主成分分析中我们所说的保留原始变量尽可能多的信息，也就是指的生成的较少的综合变量的方差和尽可能接近于原始变量',
        '方差'),
    Question('主成分分析中可以利用', '协方差矩阵|相关矩阵'),
    Question(
        '对多元数据X（x1,x2,x3,x4）进行了主成分分析, 样本的特征值λ_1=2.857，λ_2=0.809，λ_3=0.702，λ_4=0.025，则第一主成分的方差贡献率是',
        '65 %'),
    Question('在进行主成分分析得出协方差阵或是相关阵发现最小特征根接近于零时，意味着中心化以后的原始变量之间存在',
             '多重共线性'),
    Question('主成分的协方差矩阵为', '对角矩阵|对角阵'),
    Question('因子分析中因子载荷系数aij的统计意义是第i个变量与第j个公因子的', '相关系数'),
    Question('多元分析中常用的统计量有', '样本均值向量 (2分)样本协差阵 (2分)样本离差阵 (2分)样本相关系数矩阵  (2分)'),
    Question('在损失很少的信息前提下，把多个指标转化为几个综合指标的多元统计方法。', '主成分分析是利用降维的思想，'),
    Question('判别分析是判别样品',
             '所属类型(1分)的一种统计方法，常用的判别方法有距离判别|距离判别法(1分)、Fisher判别|费歇判别|Fisher判别法|费歇判别法(1分)、Bayes判别|贝叶斯判别|贝叶斯判别法|Bayes判别法(1分)、逐步判别法。'),
    Question('聚类分析就是分析如何对样品(或变量)进行量化分类的问题。通常聚类分析分为',
             'Q型|样本|R型|变量(1分) 聚类和R型|变量|Q型|样本(1分)聚类。'),
    Question('常用的Minkowski距离公式为，当q=2时，它表示', '欧氏距离|欧式距离'),
    Question('学习回归分析的目的是对实际问题进行', '预测和控制'),
    Question('判别分析适用于被解释变量是', '非度量|分类|属性(1分) 变量的情形。'),
    Question('与其他多元线性统计模型类似，判别分析的假设之一是每一个判别变量（解释变量）不能是其他判别变量的',
             '线性(1分) 组合，假设之二是各组变量的协方差矩阵|协差阵(1分)相等，假设之三是各判别变量遵从多元正态(1分)分布。'),
    Question('贝叶斯统计的思想是：假定对研究对象已有一定的认识，常用',
             '先验概率(1分)后验概率(1分)分布，各种统计推断就都可以通过这个分布来进行。'),
    Question('按经典假设，线性回归模型中的解释变量应是非随机变量，且与随机误差项', '不相关'),
    Question('回归分析中定义的解释变量和被解释变量都是', '随机(1分)变量'),
    Question('聚类和分类的区别是，', '分类(1分) 分析是一种有监督学习方法，而聚类(1分)分析是一种无监督学习方法。'),
    Question('是将分类对象分成若干类，相似的归为同一类，不相似的归为不同的类。', '聚类分析'),
    Question('进行系统聚类分析时，计算初始6个样本（X1…X6）的距离矩阵为：若类之间连接应用最大距离方法，最先聚类的是',
             'X5和X6|X5，X6|X5 X6|X5,X6|X5X6'),
    Question(
        '进行系统聚类分析时，计算初始6个样本（X1…X6）的距离矩阵为：若类之间连接应用最小距离方法，假设将X5和X6聚为一类定义为X7，则X7与X1的距离d(7,1)=',
        '6'),
    Question('Q型聚类法是按样品进行聚类，R型聚类法是按变量进行聚类,9. Q型聚类相似度统计量是',
             '距离而R型聚类统计量通常采用相似系数'),
    Question('常用的Minkowski距离公式为，当q=1时，它表示', '绝对距离|曼哈顿距离|曼氏距离|街区距离'),
    Question('回归分析中从研究对象上可分为', '一元和多元'),
    Question('聚类分析中，方法的基本思想是通过优化目标函数得到每个样本点对所有类中心的隶属度，从而对样本进行自动分类。',
             '模糊聚类'),
    Question('回归分析中，被预测或被解释的变量称为', '因变量'),
    Question('Numpy中创建全为0的矩阵使用', 'zeros|zeros()|zeros()'),
    Question('pandas中，用来读取csv文件。', 'read_csv|read_csv()|read_csv()'),
    Question('多元分析研究的是', '多指标问题'),
    Question('协方差和相关系数仅仅是变量间  的一种度量，并不能刻画变量间可能存在的', '离散程度 关联程度关系'),
    Question('设随机向量X=(x1，x2, x3, x4)\'的相关阵R为1 0.2 -0.5 0.4', '则x1和x3的相关系数为 -0.5'),
    Question('设a=(2,-4,1)\'，b=(4,1,-4)\'，则a和b的夹角为', '90'),
    Question('若A为4阶非退化矩阵，若2为矩阵A的一个特征值，对应的特征向量为（1，0，3，4），则A逆矩阵的一个特征值为',
             '1/2|0.5，对应特征向)量为（1，0，3，4)'),
    Question('设矩阵A=1 1 11 2 12 3 λ+1的秩为2，', '则λ= 1'),
    Question('设X=(X_1,X_2,…,X_p)\'有为p个分量，μ为X的均值向量，则μ是', 'p'),
    Question('几何平面上的点p=(x1,x2)到原点O=(0,0)的欧氏距离是',
             '(x1^2+x2^2)^(1⁄2)|（x1^2+x2^2）^(1/2)|(x1^2+x2^2)^(1/2)'),
    Question('设X、Y从均值向量为μ，协方差阵为∑的总体G中抽取的两个样品，定义X、Y两点之间的马氏距离为',
             '(X-Y)\'Σ^(-1) (X-Y)|(X-Y)\'∑^(-1)(X-μ)'),
    Question('如果正态随机向量X的协方差阵∑是对角阵，则X的各分量是', '相互独立 的随机变量。'),
    Question('在实际问题中,通常可以假定被研究的对象是',
             '多元正态分布 , 但分布中的参数μ和Σ是未知的,一般的做法是通过样本来估计。'),
    Question('数理统计中常用的抽样分布卡方分布，在多元统计中,与之对应的分布为', 'Wishart分布'),
    Question(
        '多元统计研究的是多指标问题,为了了解总体的特征,通过对总体抽样得到代表总体的样本但因为信息是分散在每个样本上的,就需要对样本进行加工,把样本的信息浓缩到不包含未知量的样本函数中,这个函数称为',
        '统计量'),
    Question('S的平方=1/n-1.。。   是', '样本方差 的计算公式'),
    Question('X拔=1/NΣXi是', '样本均值|均值 的计算公式。'),
    Question('假设（X,Y）是二元随机变量，则cov是', '总体协方差 的计算公式'),
    Question('多元数据的协方差阵检验中，需分析当前的波动幅度与过去的波动情形有无显著差异，此时要检验的假设H0为',
             '协方差矩阵等于规定协方差矩阵'),
    Question('多元数据协方差阵检验中，需要了解这多个总体之间的波动幅度有无明显的差异，此时要检验的假设的备择假设H1为',
             '∑i不完全相等'),
    Question('多总体的均值向量检验中，假设r个总体的方差相等，要检验的假设H0是μ_1=μ_2=⋯=μ_r,备择假设H1是', 'μ_i不全相等'),
    Question(
        '是借助两变量散点图的作图方法，它可以看作是一个大的图形方阵，其每一个非主对角元素的位置上是对应行的变量与对应列的变量的散点图。',
        '散点图矩阵'),
    Question('进行单指标检验时，假设H0: H0:μ=μ_0,H1: μ≠μ_0,计算得到统计量的数值为1.833，临界值t为0.45，此时应',
             '拒绝 原假设'),
    Question('针对连续变量的统计推断方法中，最常用的有T检验和', '方差分析'),
    Question('常用的Minkowski距离公式为..，当q=1时，它表示', '绝对距离'),
    Question('常用的Minkowski距离公式为..，当q=2时，它表示', '欧氏距离'),
    Question('常用的Minkowski距离公式为..，当q趋于正无穷时，它表示', '切比雪夫距离'),
    Question('如果X和Y在统计上独立，则相关系数等于', '0'),
    Question('相关系数r的取值范围是', '-1≤r≤1'),
    Question('代码求随机矩阵的特征值和特征向量', '''
import numpy as np

a = input().split(' ')
try:
    b = [int(i) for i in a]
    X = np.array(b).reshape(5, 5)
    w, v = np.linalg.eig(X)
    print(w, "\\n", v)
except ValueError:
    print("输入有错！")
'''),

    Question('代码求相关系数矩阵', '''
import numpy as np

a = input().split(' ')
c = input().split(' ')
t = [int(m) for m in c]
b = [float(i) for i in a]
X = np.array(b).reshape(t[0], t[1])
print(np.corrcoef(X))
'''),

    Question('代码线性回归', '''
import numpy as np
from sklearn.linear_model import LinearRegression

a = input().split(' ')
b = input().split(' ')
c = int(input())
a1 = [int(m) for m in a]
b1 = [float(i) for i in b]
X = np.array(a1).reshape(5, 1)
y = np.array(b1).reshape(5, 1)
model = LinearRegression()
model.fit(X, y)
results = model.predict(np.array([c]).reshape(1, 1))
print("Predict 12 inch cost:{:.2f}".format(results[0, 0]))
'''),

    Question('代码分类判别', '''
from numpy import *

# Fisher代码实现

# 计算样本均值
# 参数samples为nxm维矩阵，其中n表示维数，m表示样本个数
def compute_mean(samples):
    mean_mat = mean(samples, axis=1)  # axis=1按照行方向计算
    return mean_mat
# end of compute_mean

# 计算样本类内离散度
# 参数samples表示样本向量矩阵，大小为nxm，其中n表示维数，m表示样本个数
# 参数mean表示均值向量，大小为d*1，d表示维数，大小与样本维数相同，即d=m
def compute_Si(samples, mean):
    # 获取样本维数，样本个数
    dimens, nums = samples.shape[:2]
    # 将所有样本向量减去均值向量
    samples_mean = samples - mean
    # 初始化类内离散度矩阵
    s_in = 0
    for i in range(nums):
        x = samples_mean[:, i]
        s_in += dot(x, x.T)
    # endfor
    return s_in
# end of compute_Si

if __name__ == '__main__':
    x1 = array([float(i) for i in input().split(',')])
    y1 = array([float(i) for i in input().split(',')])
    w1 = mat(vstack((x1, y1)))
    x2 = array([float(i) for i in input().split(',')])
    y2 = array([float(i) for i in input().split(',')])
    w2 = mat(vstack((x2, y2)))

    mean1 = compute_mean(w1)

    mean2 = compute_mean(w2)

    s_in1 = compute_Si(w1, mean1)

    s_in2 = compute_Si(w2, mean2)

    # 求总类内离散度矩阵
    s = s_in1 + s_in2

    # 求s的逆矩阵
    s_t = s.I

    # 求解权向量，最佳投影方向
    w = dot(s_t, mean1 - mean2)

    # 求解阈值w0，基于先验概率
    w_new = w.T  # 最佳投影方向的转置
    m1_new = dot(w_new, mean1)
    m2_new = dot(w_new, mean2)
    pw1 = 0.6
    pw2 = 0.4
    w0 = m1_new * pw1 + m2_new * pw2

    # 对测试数据进行分类判别
    x = mat(array([float(i) for i in input().split(',')]).reshape(2, 1))
    y_i = w_new * x[:, 0]
    if y_i > w0:
        print('该点属于第一类')
    else:
        print('该点属于第二类')
'''),

    Question('代码K均值聚类的实现', '''
import numpy as np
from sklearn.cluster import KMeans

temp = np.array([float(i) for i in input().split(' ')])
n_samples, n_features = np.array([int(i) for i in input().split(' ')])
n_clusters = int(input())
X = []
for i in range(n_samples):
    y = []
    for j in range(n_features):
        y.append(temp[n_features * i + j])
    X.append(y)
X1 = np.array(X)

kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X1)
m = kmeans.labels_[0]
print('A公司所在类的中心为：{:.2f},{:.2f}。'.format(kmeans.cluster_centers_[m, 0], kmeans.cluster_centers_[m, 1]))
'''),

    Question('代码针对变量的系统聚类实现', '''
import numpy as np
from sklearn.cluster import AgglomerativeClustering

temp = np.array([float(i) for i in input().split(' ')])
n_samples, n_features = np.array([int(i) for i in input().split(' ')])
n_clusters = int(input())
X = []
for i in range(n_samples):
    y = []
    for j in range(n_features):
        y.append(temp[n_features * i + j])
    X.append(y)
X1 = np.array(X)

hc = AgglomerativeClustering(n_clusters=n_clusters, affinity='correlation', \
                             linkage='complete')
hc.fit(X1.T)
hcl = hc.labels_
if hcl[0] == hcl[2]:
    print("香气和酸质属于一类。")
else:
    print("香气和酸质不属于一类。")
'''),

    Question('代码写出贡献率最大的主成分线性方程', '''
import numpy as np
from decimal import *

# mean of each feature
temp = np.array([float(i) for i in input().split(',')])
n_samples, n_features = np.array([int(i) for i in input().split(',')])
X = []
for i in range(n_samples):
    y = []
    for j in range(n_features):
        y.append(temp[n_features * i + j])
    X.append(y)
X1 = np.array(X)

mean = np.array([np.mean(X1[:, i]) for i in range(n_features)])

# normalization
norm_X = X - mean
# scatter matrix
scatter_matrix = np.dot(np.transpose(norm_X), norm_X)

# Calculate the eigenvectors and eigenvalues
eig_val, eig_vec = np.linalg.eig(scatter_matrix)
eig_pairs = [(np.abs(eig_val[i]), eig_vec[:, i]) for i in range(n_features)]
# sort eig_vec based on eig_val from highest to lowest
eig_pairs.sort(reverse=True)
# select the top k eig_vec
feature = [ele[1] for ele in eig_pairs[:1]]
i = 1
value = ''
for ele in feature[0]:
    if(ele >= 0):
        value = value + '+' + str(Decimal(ele).quantize(Decimal('0.00000'))) + \
                '*(x' + str(i) + '-' + str(Decimal(mean[i-1]).quantize(Decimal('0.00'))) + ')'
    else:
        value = value + str(Decimal(ele).quantize(Decimal('0.00000'))) + \
                '*(x' + str(i) + '-' + str(Decimal(mean[i-1]).quantize(Decimal('0.00'))) + ')'
    i = i + 1
if(value[0] == '+'):
    value = value[1:]
print('第1主成分=' + value)
''')

]


class numpy:
    all_question = question

    @classmethod
    def array(cls, question):
        ret = []
        for i in cls.all_question:
            if question in i.question_text:
                ret.append(i)

        if len(ret) == 0:
            print('没有题目')
        else:
            for i in ret:
                print(f'题目:{i.question_text}\n答案:{i.answer}',
                      end='\n--------------------------------------------------\n')

# 《智能系统设计与应用》课程设计 
docker仓库见：[https://hub.docker.com/r/professornuo/intelligent_algebraic_systems](https://hub.docker.com/r/professornuo/intelligent_algebraic_systems)
##  零、使用方法
安装docker后，在shell中执行以下指令
``` shell
docker pull professornuo/intelligent_algebraic_systems
docker run -it -p 8501:8501 professornuo/intelligent_algebraic_systems
```
随后在浏览器中打开URL [http://127.0.0.1:8501](http://127.0.0.1:8501) 即可使用

## 一、课程设计目的 
通过设计并实现一个小型智能系统培养学生软件系统开发的基本能力，包括加深面向对象程序设计的理解、提高学生编程动手能力、软件系统的设计与实现能力、基本算法的设计、编程与调试能力、智能系统的分析与实现能力。

## 二、课程设计报告（文档）要求： 
书写课程设计报告，报告中应该包含如下内容：
1. 课程设计题目及内容。
2. 每个功能模块的设计分析及算法描述。
3. 程序中使用的数据及主要符号说明。
4. 带有详细注释的自己编写的源程序。
5. 程序运行时的效果图。
6. 实验结果分析，实验收获和体会。
7. 自评成绩。

## 三、题目要求：
智能代数运算系统：用户输入任意表达式，系统能正确计算出结
果，表达式支持常用数学函数以及变量。
设计要求及提示如下：
1. 用户通过输入任意表达式，计算出结果，如：`a*sin(b*x+c) + x^2 + sqrt(a)`;
2. 表达式中若出现未申明变量，则给该变量初始化一个随机值，如：`a = random(0,10)`;
3. 支持常用数学函数，包括（不限于）如下函数：`sin, cos, tan, floor, random, abs, sqrt, ^....`
4. 可以修改变量的值，表达式根据变量的变化自动更新计算结果；
5. 允许用户自定义函数，如定义 `f(x) = (x+2)^2` 后，用户可以在表达式中使用该函数：`f(sin(a))+f(a)+sin(f(a))`
6. 下图为程序效果参考：
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/ba8a68ec-2278-4ce4-ad0b-4e7a8a0c4b0f)
[几何画板的demo](https://www.netpad.net.cn/resource_web/course/#/575887 "几何画板的demo")

## 四、测试用例：
`a*sin(b*x+c^log(2,sin(a)))+abs(3+x)*cos(cos(b)+(b-4*ac))/(2*floor(x))-log(a,x)`

`𝑎 sin(𝑏 ∗ 𝑥 + 𝑐^2) + abs(3 + x) ∗ sec(𝑏 + (b − 4𝑎𝑐))/(2 ∗ 𝑓𝑙𝑜𝑜𝑟(𝑥)) − log(𝑎, 𝑥) ∗ ln(𝑥)`

`log(log(log(𝑎, 𝑥), 𝑚), 𝑛) + sin(cos(sin(cos(x) + a ∗ b/(c ∗ d)) + b) + c)`

## 五、俺的作品
### 解析式计算&Latex输出&绘图测试
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/555dc74b-3dfd-4c21-9be6-a7ce30f89b06)
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/dc840cc6-6faa-42e0-8c82-0999a052e407)
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/235405a3-f4fd-4e11-92d1-44afb67db562)
### 自定义函数测试
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/7e7d45fb-3efb-4e41-870a-d7ea1952c057)
![image](https://github.com/Tangent-90C/Intelligent-System-Design-and-Application-course-design-/assets/28804414/936f32e2-e7e3-465c-be27-a8801d849544)

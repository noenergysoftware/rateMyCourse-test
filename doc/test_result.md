# Alpha阶段测试结果
具体哪些bug这里就不列出了。都可以在[github的issue](https://github.com/noenergysoftware/rateMyCourse/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aclosed+)中找到。测试人员发现的bug都有打上相应的标签。
## 前测试点
commit: 666cc6afa8556d0618d630e9118f1df88518e994

共47个测试样例，全部通过。

* bug数：4
* invalid数：2

JS代码覆盖率：
因为较晚才弄明白到底该怎么配合使用JSCover和Selenium，所以覆盖率还没有刷高。
![](alpha_front_coverage.png)

## 后测试点
commit: 55890581df5543ce2e34768306f72bf01e62c867

共31个测试样例，全部通过。

* bug数：4
* invalid数：8

Python代码覆盖率：
![](alpha_back_coverage.png)


# Beta阶段测试结果
因为大量使用了python的subTest，很多测试样例被转变成了一组子测试样例的线性执行序列，所以统计测试样例数目已经变成一件没啥意义的事情了，以后也都不将统计。

## 前测试点
commit: 5c6e26850dd8f74f423433f78d60535647bd90ef

Bug:
* 切页功能：[1](https://github.com/noenergysoftware/rateMyCourse/issues/55), [2](https://github.com/noenergysoftware/rateMyCourse/issues/109), [3](https://github.com/noenergysoftware/rateMyCourse/issues/112)
* 赞踩功能：[1](https://github.com/noenergysoftware/rateMyCourse/issues/119)
* Edge的兼容性问题：[1](https://github.com/noenergysoftware/rateMyCourse/issues/117), [2](https://github.com/noenergysoftware/rateMyCourse/issues/118)
* 其他：[1](https://github.com/noenergysoftware/rateMyCourse/issues/116)

Invalid:
* 切页功能：[1](https://github.com/noenergysoftware/rateMyCourse/issues/56)

js覆盖率：
![beta_front_coverage.png](beta_front_coverage.png)

## 后测试点
commit: ff51f9ec21efb90cce08e5585c90cb7235cd7da1

Bug:
* 评分功能：[1](https://github.com/noenergysoftware/rateMyCourse/issues/106)
* 评分计算：[1](https://github.com/noenergysoftware/rateMyCourse/issues/104)

Invalid:
* 评分计算：[1](https://github.com/noenergysoftware/rateMyCourse/issues/105)

python覆盖率：
![beta_back_coverage.png](beta_back_coverage.png)

## 安全性检查
* [分析书](https://github.com/noenergysoftware/rateMyCourse/blob/master/document/safe/safe_analyze_report.md)
* [解决报告书](https://github.com/noenergysoftware/rateMyCourse/blob/master/document/safe/security_report.md)

主要解决的问题：
* Django的秘钥的存放
* CSRF攻击
* XSS攻击
* Clickjacking攻击
* 启用HSTS

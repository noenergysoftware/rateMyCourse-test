# 基本流程
0. 我们接下来会要启用local-storage，但在这个模式下生成的jscoverage.js文件是存在bug的。我们需要先用jscover在非local-storage模式下生成一个jscoverage.js，然后复制，找个地方保存下它，再继续操作。
    * 之所以需要启用local-storage，是为了让jscover的覆盖率变量在网页之间能够被共享，否则当我们切换页面的时候，旧页面的覆盖率变量就会丢失。
1. jscover加工前端代码：使用filesystem模式，生成加入插桩代码后的前端代码，注意要启用local-storage模式。
2. 将之前保存下来的非local-storage模式下的jscoverage.js拿出来，覆盖掉生成的local-storage模式下的jscoverage.js。
3. 修改nginx的conf文件，使代理插桩后的前端代码（需要杀光nginx进程才能使得更改conf文件有效）
4. 修改测试代码，使得在每个webdriver要被销毁之前，调用jscoverage_serializeCoverageToJSON函数生成jscoverage.json文件。
    * 因为每个Testcase都有一个webdriver，所以我们为每一个testcase准备一个文件夹，然后在该文件夹下生成jscoverage.json文件。
4. 运行测试样例。
5. 使用jscover的merge指令合并上一步产生的jscoverage.json们，将合并的jscoverage.json放在和jscoverage.html同目录下。
6. 修改jscoverage.js文件，将jscoverage_isReport改为true

    var jscoverage_isReport = true;
7. 使用edge打开jscoverage.html
    * 不能使用chrome，因为chrome禁止本地的文件访问。当然好像存在选项改，但还是直接Edge方便。

# 封装后的详细流程
1. 使用jscover插桩前端代码，示例命令：
    `java -Dfile.encoding=UTF-8 -jar test/JSCover-all.jar -fs --local-storage --no-branch --no-function --include-unloaded-js --no-instrument=/front_end/lib D:/code_concerned/ruangong/rateMyCourse_front D:/code_concerned/ruangong/rateMyCourse_front_coverage`
    * `Dfile.encoding=UTF-8`：这是为了避免插桩后的代码中的中文变成乱码
    * `-jar test/JSCOVER-all.jar`：指定jscover的jar包位置，可以从JSCOVER官网下载，这里我已经放了一个在这了。
    * `-fs`：指定为文件模式，也就是会生成插桩后的代码文件，其他模式见官网。
    * `--local-storage`：指定使用HTML5的local-storage功能来跨页面保存覆盖率变量。
    * `--no-branch --no-function`：禁止检查分支覆盖率和函数覆盖率。这是为了效率考虑，不然太慢了。
    * `--include-unloaded-js`：使得初始的jscoverage.json中包含未加载的js文件的覆盖率信息。但因为我们之后肯定会用merge后的jscoverage.json文件覆盖它，所以是没啥用的一句话，不用管，但最好别删。
    * `--no-instrument=/front_end/lib`：指定哪些js文件不应被进行插桩。这里我是指定的第三方代码全都不插桩。
    * `D:/code_concerned/ruangong/rateMyCourse_front`：原代码
    * `D:/code_concerned/ruangong/rateMyCourse_front_coverage`：插桩后的代码的目录

2. 运行测试样例
3. 合并插桩记录，示例命令：
    `java -cp test/JSCover-all.jar jscover.report.Main --merge test/coverage/front/* D:/code_concerned/ruangong/rateMyCourse_front_coverage/`
    * `-cp test/JSCover-all.jar jscover.report.Main`：我也不知道啥意思，反正就是指定要使用的java类吧。
    * `--merge`：指明是要对插桩记录进行合并
    * `test/coverage/front/*`：未合并的插桩记录文件的所在目录，应于front_config中的COVERAGE_DIR一致
    * `D:/code_concerned/ruangong/rateMyCourse_front_coverage/`：插桩后的代码的目录，也是合并后的插桩记录文件的存放位置。我们需要放到代码目录里去，以从源代码级别查看哪些行被覆盖到了。

4. 使用edge打开插桩后的代码的目录下的jscoverage.html，查看结果。

# 不使用Proxy的原因
因为Proxy模式需要修改浏览器代理。而我们目前的本地测试环境使用了Fiddler作为浏览器代理，这两个代理也就冲突了。
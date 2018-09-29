# find-all-the-new-words

- 找出文章中的生词（配合anki使用）
- 示例 [先背生词，再看文章 FAIDK v1.0.0](https://zhuanlan.zhihu.com/p/25003457)

## 依赖

- Python3.6

## 已知bug

- ~~部分以 s 为结尾的单词词形还原不正确，比如 yes->ye, less->les 等。这是我使用的词形还原工具 pattern.en.lemma 那边的bug，已去提bug。不是非常影响使用，暂时不打算更换词形还原工具。如果有更多的错误影响使用的话，请告诉我。~~
- 实践证明上面那bug影响使用，所以我弃用了，等下个版本换一个上来，但是可能要暑假了，太忙了。我自己也在将就着用，万一有那么一两个用户的话，你们也先将就一下吧。
- ~~exe 尚不支持词形还原。复杂的包打exe会有各种奇奇怪怪的问题，我再想想办法~~
- exe 等测试一段时间没什么问题就打包

## 最近一次更新 2018年09月28日 2.0.1

- 重构代码，我也不知道是重构好了还是重构差了。。。
- 鸽了一个暑假，接下来更新可能稳定一点
- 这个版本我只做了简单测试，所以记得备份自己的old.txt，其他应该不会造成什么损失
- 维护一个QQ群，万一有人用呢，也满足一下我的虚荣心，更新可能快点。737389550 
<div align=center>
<img src="https://i.loli.net/2018/09/29/5baedf2a2bd6d.jpg" width = "100"/>
</div>

## ~~即将到来的~~新 Feature 预告

- 中断恢复
- 自定义按键
- 词形还原
- 文章含有过多生词自动切割
- 自定义 config 路径
- 多 config 选择

## 更新

### 2018年09月28日 2.0.1

- 重构代码，我也不知道是重构好了还是重构差了。。。
- 鸽了一个暑假，接下来更新可能稳定一点
- 这个版本我只做了简单测试，所以记得备份自己的old.txt，其他应该不会造成什么损失
- 维护一个QQ群，万一有人用呢，也满足一下我的虚荣心，更新可能快点。737389550 
<div align=center>
<img src="https://i.loli.net/2018/09/29/5baedf2a2bd6d.jpg" width = "100"/>
</div>


### 2018年05月16日 1.0.1

- 删除了pattern 的词形还原
- 修复了一个文件命名错误导致把old.txt覆盖了的bug，它把我的词库弄没了。我希望没有给你们带来什么损失，毕竟并没有人来报bug。

### 2018年03月14日 1.0.0

- 添加 v1.0.0 release
- 添加 json indent

### 2018年03月14日 0.2.3

- 增加 FAIDN.config, 支持自定义目录

### 2018年02月27日 0.2.2

- 从 python 2.7 更新到 python 3.6
- 增加词形还原功能

### 2017年04月08日 0.2.1

- 修复old.txt文件没有单词的bug
- 修复build 模式输入2会报错的bug

### 2017年03月07日 0.2.0

- 省略回车，节省时间
- 按照pylint规范化代码
- 添加0.2.0的exe程序
- 修复.py与exe不同的路径情况（用于生成exe的Python文件已放入压缩包）

## 使用

- 把文章放在 ./article 文件夹中
- build 模式用来建立自己的词汇库，即 old.txt，同时也可以将新单词列出来，建议建立的时候挑选较短的文章，一篇一篇来
- 词库建立好了就可以使用 find 模式批量查找生词

## exe文件

- exe文件 release 里面
- 解压后 ，快捷方式需要你自己重新创建
- 如果还需要帮助，你可以参考上面给的示例

## 关于anki

- [Anki——近乎完美的神器](https://zhuanlan.zhihu.com/-anki)

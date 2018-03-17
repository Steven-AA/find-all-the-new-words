# find-all-the-new-words

- 找出文章中的生词（配合anki使用）
- 示例 [先背生词，再看文章 FAIDK v1.0.0](https://zhuanlan.zhihu.com/p/25003457)

## 依赖

- Python3.6

## 已知bug

- 部分以 s 为结尾的单词词形还原不正确，比如 yes->ye, less->les 等。这是我使用的词形还原工具 pattern.en.lemma 那边的bug，已去提bug。不是非常影响使用，暂时不打算更换词形还原工具。如果有更多的错误影响使用的话，请告诉我。
- exe 尚不支持词形还原。复杂的包打exe会有各种奇奇怪怪的问题，我再想想办法

## 更新

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
- build.py 用来建立自己的词汇库，即old.txt，同时也可以将新单词列出来，建议建立的时候挑选较短的文章，一篇一篇来
- 词库建立好了就可以使用 find.py 批量查找生词

## exe文件

- exe文件 release 里面
- 解压后 ，快捷方式需要你自己重新创建
- 如果还需要帮助，你可以参考上面给的示例

## 关于anki

- [Anki——近乎完美的神器](https://zhuanlan.zhihu.com/-anki)

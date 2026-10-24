# 来源与许可范围

本项目仅包含 **rag-design-review（RAG 设计审核）**。主体任务指南由 AI 辅助整理，按用户任务需求编写并经审阅；离线示例和合成资料为本次发布准备自建。

本项已确认采用 **MIT License**，版权署名为 **xiaojin5222-ui**。许可适用于本仓库自身的任务指南、配置、文档、示例代码与合成数据，具体条款见 `LICENSE`。

## 来源检查

已对照原始指南、前序技术审阅及相关素材，未发现需要另行取得第三方许可的具体复制段落、图片或源码。指南吸收的是检索、版本、权限、引用核对和边界测试等方法，并重新组织为可执行的审核步骤；没有把第三方案例结果写成自己的实测成绩。

示例使用虚构的工作室通行证和会议室政策，明确标记为合成数据。示例代码仅使用 Python 标准库，没有打包第三方库或上游实现。

## 公共参考

以下资料仅以书目信息和链接提供，没有转载论文、网页、图片或代码：

- **Patrick Lewis 等12位作者**：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)，2020年。作为 RAG 概念的论文出处。
- **Elastic 官方文档维护者**：[Approximate kNN query examples](https://www.elastic.co/docs/solutions/search/vector/knn/approximate-knn-query-examples)。用于了解混合检索及分数尺度问题。
- **scikit-learn 文档维护者**：[Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)。用于区分模型分数与经验证、校准的概率。

链接及题名于2026-10-24核对。在线文档可能更新；引用不表示其作者认可本项目。本项目的 MIT 许可不授予对这些第三方原文的权利。

## 不包含的材料

本仓库不分发第三方原图、识别文本、逐图摘录、内部任务记录、私人数据或历史运行目录；也不分发参考资料的全文、图表或源码。后续若引入实际第三方复制内容，应按具体来源保留其许可与声明。


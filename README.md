### 緣由
- 想要學習如何用 python 開發 firebase functions
- 想要學習如何在 functions framework + flask 環境下初始化 injector 並在後續的 request 中使用

### 選型
- 依賴注入容器: [injector](https://pypi.org/project/injector/)
- 分層方式: presentation -> application -> domain (除了 domain models 還包括 adapters 及 infrastructure services 的抽象)
- 先採用貧血模型
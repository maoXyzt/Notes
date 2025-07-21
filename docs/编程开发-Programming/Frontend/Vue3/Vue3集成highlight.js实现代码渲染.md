# Vue3 集成 highlight.js 实现代码渲染

## 安装依赖

```bash
pnpm install highlight.js
pnpm install @highlightjs/vue-plugin
```

`highlightjs/vue-plugin` 插件提供了一个组件 `<highlightjs>`，可以在 Vue 中使用

## 使用

在 `main.js` 中引入并注册插件：

```javascript
//引入依赖和语言
import 'highlight.js/styles/stackoverflow-light.css'
import hljs from "highlight.js/lib/core";
import hljsVuePlugin from "@highlightjs/vue-plugin";
//import "highlight.js/lib/common"; //单一加载
//按需引入语言
import javascript from "highlight.js/lib/languages/javascript";
import java from "highlight.js/lib/languages/java";
import sql from "highlight.js/lib/languages/sql";
import xml from "highlight.js/lib/languages/xml";
import html from "highlight.js/lib/languages/vbscript-html";
import json from "highlight.js/lib/languages/json";
import yaml from "highlight.js/lib/languages/json";
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("java", java);
hljs.registerLanguage("yaml", yaml);
hljs.registerLanguage("json", json);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("xml", xml);
hljs.registerLanguage("html", html);
```

高亮显示代码:

```vue
<template>
  语言：
  <el-select v-model="language" @change="languageChange" placeholder="Select" style="width: 240px">
    <el-option
        v-for="item in languageOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
        :disabled="item.disabled"
    />
  </el-select>
  <div style="height: 100vh;width: 100vh;line-height: 30px;padding: 5px;">
    <!--
          <highlightjs language="sql" :code="code"></highlightjs>
    -->
    <highlightjs :language="language" :code="code"></highlightjs>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {js, json, java, sql, yaml,xml} from './CodeHighlightData.ts'

//默认高亮JS代码
let code = ref(js)
let language = ref('javascript')
//语言选项
const languageOptions = [
  {
    value: 'javascript',
    label: 'js',
  },
  {
    value: 'java',
    label: 'Java'
  },
  {
    value: 'yaml',
    label: 'yaml',
  },
  {
    value: 'sql',
    label: 'sql',
  },
  {
    value: 'json',
    label: 'json',
  },
  {
    value: 'xml',
    label: 'xml',
    disabled: false,
  },
  {
    value: 'html',
    label: 'html',
    disabled: false,
  },
]

/**
 * 语言改变事件处理函数
 * @param language
 */
const languageChange = (language: string) => {
  if ('java' === language) {
    code.value = java
  } else if ('json' === language) {
    code.value = json
  } else if ('yaml' === language) {
    code.value = yaml
  } else if ('sql' === language) {
    code.value = sql
  } else if ('xml' === language) {
    code.value = xml
  } else {
    code.value = js
  }
}
</script>
```

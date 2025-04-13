<template>
  <div class="mian_container">
    <div class="about">
      <h2>课时教案</h2>
      <h4>助教场景：AI辅助自动生成教案</h4>
    </div>
    <div class="editor-preview-container">
      <Editor class="editor" @update-preview="updatePreview" />
      <Preview class="preview" :content="previewContent" />
    </div>
  </div>
</template>

<script>
import Editor from "./Func1_page/PageEditor.vue";
import Preview from "./Func1_page/PagePreview.vue";

export default {
  name: 'FunctionOne',
  components: {
    Editor,
    Preview,
  },
  data() {
    return {
      previewContent: JSON.stringify({  // 初始化为空结构
        plan: '',
        content: '',
        schedule: []
      })
    };
  },
  methods: {
    updatePreview(newData) {
      this.previewContent = JSON.stringify(newData);  // 直接更新预览内容
    },
  },
};
</script>

<style scoped>
.mian_container {
  margin: 40px 80px;
}

.about {
  margin-bottom: 20px;
}

.editor-preview-container {
  display: flex;
  gap: 20px;
}

.editor,
.preview {
  flex: 1;
  border: 1px solid #ccc;
  padding: 10px;
  box-sizing: border-box;
  min-height: 400px;
}

.preview >>> .content {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
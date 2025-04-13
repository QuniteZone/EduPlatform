<template>
  <section class="preview">
    <div v-if="formattedContent" class="content">
      <h3>{{ formattedContent.plan }}</h3>
      <p>{{ formattedContent.content }}</p>
      <div v-if="formattedContent.schedule">
        <h4>学习计划安排：</h4>
        <ul>
          <li v-for="(item, index) in formattedContent.schedule" :key="index">
            {{ item }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      请先生成内容
    </div>
  </section>
</template>

<script>
export default {
  props: {
    content: {
      type: String,
      required: true
    }
  },
  computed: {
    formattedContent() {
      try {
        return JSON.parse(this.content)
      } catch (error) {
        return null
      }
    }
  }
};
</script>

<style scoped>
.preview {
  width: 100%;
  border: 1px solid #ccc;
  padding: 10px;
  box-sizing: border-box;
  color: #333;
  min-height: 400px;
}

.content {
  line-height: 1.6;
}

h3 {
  color: #1a73e8;
  margin-bottom: 15px;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
}
</style>
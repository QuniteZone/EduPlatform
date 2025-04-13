<template>
  <section class="editor">
    <textarea v-model="content" placeholder="请输入内容..."></textarea>
    <div class="select_box">
      <div class="grade_select">
        <p>选择年级</p>
        <el-select v-model="grade" placeholder="Select" style="width: 180px">
          <el-option
            v-for="item in gradeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div class="course_select">
        <p>选择课程</p>
        <el-select v-model="subject" placeholder="Select" style="width: 180px">
          <el-option
            v-for="item in subjectOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <el-button
        type="primary"
        @click="generateContent"
        style="width: 180px"
      >
        生成内容
      </el-button>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const emit = defineEmits(['update-preview'])

const grade = ref('未选择')
const subject = ref('未选择')

const gradeOptions = [
  { value: '高一', label: '高一' },
  { value: '高二', label: '高二' },
  { value: '高三', label: '高三' },
]

const subjectOptions = [
  { value: '数学', label: '数学' },
  { value: '语文', label: '语文' },
  { value: '英语', label: '英语' },
]

const generateContent = async () => {
  try {
    const response = await axios.post('/api/plan/lesson_plan', {
      grade: grade.value,
      subject: subject.value,
      knowledge:""
    });

    emit('update-preview', response.data)  // 发送数据给父组件

  } catch (error) {
    alert('生成失败');
    console.error('请求失败:', error);
  }
};
</script>

<style scoped>
.editor {
  width: 100%;
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

textarea {
  width: 100%;
  height: 200px;
  resize: none;
  margin-bottom: 10px;
}

.select_box {
  display: flex;
  gap: 40px;
  flex: 1;
}

.grade_select,
.course_select {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.grade_select p,
.course_select p {
  margin-bottom: 5px;
}

.el-button {
  margin-left: 40px;
  align-self: flex-end;
}
</style>
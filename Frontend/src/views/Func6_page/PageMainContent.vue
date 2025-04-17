<template>
  <div class="main-content">
    <!-- Header -->
    <div class="header">
      <el-button type="primary">第2组</el-button>
      <span>简答题</span>
      <span>当前学生：2023031011</span>
      <el-button type="primary" style="float: right;">提交阅卷结果</el-button>
    </div>

    <!-- 题目内容 -->
    <div class="question-content">
      <h3>第1题</h3>
      <p>需要占用一片连续的存储空间，D. 数中元素的个数不变。</p>
      <p>当输入序列为 1, 2, 3，则下列序列中不可能是栈的输出序列的是 (C)</p>
    </div>

    <!-- 评分和评语区域 -->
    <div class="grading-section">
      <el-row :gutter="20">
        <!-- AI 打分和评语 -->
        <el-col :span="8">
          <div class="ai-section">
            <div class="ai-score">
              <label>AI 给出的分数</label>
              <el-input v-model="aiScore" placeholder="AI 打分" disabled></el-input>
              <el-button type="primary" @click="handleAiReview">AI 评阅</el-button>
            </div>
            <div class="ai-comment">
              <label>AI 评语</label>
              <el-input
                type="textarea"
                :rows="5"
                placeholder="AI 评语将在此显示"
                v-model="aiComment"
                readonly
              ></el-input>
            </div>
          </div>
        </el-col>

        <!-- 教师打分 -->
        <el-col :span="8">
          <div class="teacher-scoring">
            <div class="teacher-score">
              <label>教师打分：</label>
              <el-input v-model="teacherScore" placeholder="请输入教师打分"></el-input>
            </div>
            <div class="score-buttons">
              <el-button
                v-for="score in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
                :key="score"
                type="primary"
                @click="setTeacherScore(score)"
              >
                {{ score }}
              </el-button>
              <el-button type="info" @click="setTeacherScore(0)">0分</el-button>
              <el-button type="success" @click="setTeacherScore(10)">满分</el-button>
            </div>
          </div>
        </el-col>

        <!-- 教师评语 -->
        <el-col :span="8">
          <div class="teacher-comment">
            <label>教师评语：</label>
            <el-input
              type="textarea"
              :rows="5"
              placeholder="请输入教师评语"
              v-model="teacherComment"
            ></el-input>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 按钮 -->
    <div class="buttons">
      <el-button type="primary" @click="handleSubmit">批改完成</el-button>
      <el-button type="danger" @click="handleNext">下一份</el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      aiScore: '', // AI 打分
      aiComment: '', // AI 评语
      teacherScore: '', // 教师打分
      teacherComment: '' // 教师评语
    };
  },
  methods: {
    handleAiReview() {
      this.aiComment = 'AI 评语：这是一条示例评语。';
    },
    setTeacherScore(score) {
      this.teacherScore = score;
    },
    handleSubmit() {
      alert('批改完成');
    },
    handleNext() {
      alert('跳转到下一份');
    }
  }
};
</script>

<style scoped>
.main-content {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-content {
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
}

.grading-section {
  border: 1px solid #ccc;
  padding: 20px;
}

.ai-section,
.teacher-scoring,
.teacher-comment {
  margin-top: 20px;
}

.ai-score,
.ai-comment,
.teacher-score,
.score-buttons,
.teacher-comment {
  margin-bottom: 10px;
}

.buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
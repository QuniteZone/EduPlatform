<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="/function1">功能1</el-menu-item>
    <el-menu-item index="/function2">功能2</el-menu-item>

    <el-sub-menu index="-1">
      <template #title>测试1</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="-2" disabled>测试2</el-menu-item>
  </el-menu>
  <router-view />
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const activeIndex = ref(route.path)
// const activeIndex = ref("Home.vue")

const handleSelect = (key: string, keyPath: string[]) => {
  router.push(key)
  console.log(key, keyPath)
}

</script>
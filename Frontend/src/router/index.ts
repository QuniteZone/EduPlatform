import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Func1 from '../views/Func1.vue'
import Func2 from '../views/Func2.vue'
import Home from '../views/Home.vue'
import PageEditor from '../views/Func1_page/PageEditor.vue'
import PagePreview from '../views/Func1_page/PagePreview.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/function1',
    name: 'Function1',
    component: Func1
  },
  {
    path: '/function2',
    name: 'Function2',
    component: Func2
  },
  {
    path: '/editor',
    name: 'PageEditor',
    component: PageEditor,
  },
  {
    path: '/preview',
    name: 'PagePreview',
    component: PagePreview,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
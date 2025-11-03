import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Editor from '@/views/Editor.vue';
import NotFound from '@/views/NotFound.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/edit',
      name: 'Editor',
      component: Editor,
      meta: { defaultViewMode: false }
    },
    {
      path: '/view',
      name: 'View',
      component: Editor,
      meta: { defaultViewMode: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    }
  ]
});

export default router;


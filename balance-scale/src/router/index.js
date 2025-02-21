import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("../pages/Home.vue") },
    { path: "/SignUp", component: () => import("../pages/SignUp.vue") },
    { path: "/SignIn", component: () => import("../pages/SignIn.vue") },
  ],
});

export default router;

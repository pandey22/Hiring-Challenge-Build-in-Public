import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import SignIn from '../pages/SignIn.vue';
import SignUp from '../pages/SignUp.vue';
import StudentDashboard from '../pages/StudentDashboard.vue';
import TeacherDashboard from '../pages/TeacherDashboard.vue';

const routes = [
  { path: "/", component: Home },
  { path: "/SignIn", component: SignIn },
  { path: "/SignUp", component: SignUp },
  { path: "/StudentDashboard", component: StudentDashboard },
  { path: "/TeacherDashboard", component: TeacherDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

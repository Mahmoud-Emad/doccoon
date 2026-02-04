import { createRouter, createWebHistory } from "vue-router";

const Home = () => import("@/views/Home.vue");
const Editor = () => import("@/views/Editor.vue");
const Docs = () => import("@/views/Docs.vue");
const Privacy = () => import("@/views/Privacy.vue");
const Terms = () => import("@/views/Terms.vue");
const Login = () => import("@/views/Login.vue");
const Register = () => import("@/views/Register.vue");
const ForgotPassword = () => import("@/views/ForgotPassword.vue");
const ResetPassword = () => import("@/views/ResetPassword.vue");
const OAuthCallback = () => import("@/views/OAuthCallback.vue");
const Profile = () => import("@/views/Profile.vue");
const SharedPage = () => import("@/views/SharedPage.vue");
const SharedBook = () => import("@/views/SharedBook.vue");
const NotFound = () => import("@/views/NotFound.vue");
const ServerError = () => import("@/views/ServerError.vue");

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    // If using browser back/forward, restore saved position
    if (savedPosition) {
      return savedPosition;
    }
    // Otherwise scroll to top
    return { top: 0 };
  },
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/register",
      name: "Register",
      component: Register,
    },
    {
      path: "/forgot-password",
      name: "ForgotPassword",
      component: ForgotPassword,
    },
    {
      path: "/reset-password",
      name: "ResetPassword",
      component: ResetPassword,
    },
    {
      path: "/auth/google/callback",
      name: "GoogleCallback",
      component: OAuthCallback,
    },
    {
      path: "/auth/github/callback",
      name: "GitHubCallback",
      component: OAuthCallback,
    },
    {
      path: "/edit",
      name: "Editor",
      component: Editor,
      meta: { defaultViewMode: false },
    },
    {
      path: "/view",
      name: "View",
      component: Editor,
      meta: { defaultViewMode: true },
    },
    {
      path: "/docs",
      name: "Docs",
      component: Docs,
    },
    {
      path: "/privacy",
      name: "Privacy",
      component: Privacy,
    },
    {
      path: "/terms",
      name: "Terms",
      component: Terms,
    },
    {
      path: "/profile",
      name: "Profile",
      component: Profile,
    },
    {
      path: "/shared/page/:token",
      name: "SharedPage",
      component: SharedPage,
    },
    {
      path: "/shared/book/:token",
      name: "SharedBook",
      component: SharedBook,
    },
    {
      path: "/error",
      name: "ServerError",
      component: ServerError,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: NotFound,
    },
  ],
});

export default router;

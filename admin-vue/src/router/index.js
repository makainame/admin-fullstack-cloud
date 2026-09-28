import { createRouter, createWebHashHistory } from 'vue-router'
const routes = [
  {path:'/',redirect:'/login'},
  {path:'/login',component:()=>import('../views/Login.vue')},
  {
    path:'/admin',
    component:()=>import('../views/Layout.vue'),
    children:[
      {path:'user',component:()=>import('../views/User.vue')},
      {path:'upload',component:()=>import('../views/Upload.vue')}
    ]
  }
]
const router = createRouter({history:createWebHashHistory(),routes})
router.beforeEach((to,from,next)=>{
  const token = localStorage.getItem('token')
  if(to.path!=='/login' && !token) return next('/login')
  next()
})
export default router

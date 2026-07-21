<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" style="background-color: #2e3440;">
      <el-menu router active-text-color="#ffd04b" background-color="#2e3440" text-color="#fff">
        <el-menu-item index="/admin/user">用户管理</el-menu-item>
        <el-menu-item index="/admin/upload">文件上传</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="text-align: right; font-size: 14px; line-height: 60px;">
        <el-button @click="logout" type="text">退出登录</el-button>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const logout = ()=>{
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

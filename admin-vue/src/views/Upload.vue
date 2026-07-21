<template>
  <div style="width: 80%; margin: 20px auto;">
    <h3>文件上传管理</h3>
    <el-upload
      action="/api/upload"
      :headers="headerObj"
      list-type="text"
      :on-success="successHandle"
    >
      <el-button type="primary">点击上传文件</el-button>
    </el-upload>
    <el-table :data="fileList" border style="margin-top:20px">
      <el-table-column label="文件名" prop="file_name"></el-table-column>
      <el-table-column label="上传时间" prop="upload_time"></el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="size"
      :total="total"
      @change="getFileList"
      style="margin-top:10px;text-align:right"
    ></el-pagination>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
const headerObj = {
  Authorization: `Bearer ${localStorage.getItem('token')}`
}
const fileList = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)
const getFileList = async () => {
  const res = await request.get(`/upload/list?page=${page.value}&size=${size.value}`)
  fileList.value = res.data.data
  total.value = res.data.total
}
const successHandle = () => {
  getFileList()
}
onMounted(() => {
  getFileList()
})
</script>

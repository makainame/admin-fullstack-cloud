<template>
  <div class="user-container">
    <div class="btn-box" style="margin: 10px 0;">
      <el-button type="primary" @click="openAddDialog">新增用户</el-button>
      <el-button type="success" @click="exportExcel">导出Excel</el-button>
      <el-button type="warning" @click="uploadExcel">导入Excel</el-button>
      <input ref="excelFileRef" type="file" accept=".xlsx,.xls" style="display: none" @change="handleImport">
    </div>
    <el-table :data="userList" border stripe style="width: 100%">
      <el-table-column prop="id" label="用户ID" width="80"></el-table-column>
      <el-table-column label="头像" width="80">
        <template #default="scope">
          <el-avatar v-if="scope.row.avatar" :src="avatarUrl(scope.row.avatar)" size="small" />
          <el-avatar v-else icon="UserFilled" size="small" />
        </template>
      </el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="nickname" label="用户昵称"></el-table-column>
      <el-table-column prop="create_time" label="创建时间"></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="openEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="delUser(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="size"
      :total="total"
      layout="total, sizes, prev, pager, next, jumper"
      @change="getUserList"
      style="margin-top: 10px; text-align: right;"
    ></el-pagination>
    <el-dialog v-model="dialogVisible" :title="isAdd ? '新增用户' : '编辑用户'">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" :disabled="!isAdd"></el-input>
        </el-form-item>
        <el-form-item label="密码" v-if="isAdd">
          <el-input v-model="form.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname"></el-input>
        </el-form-item>
        <el-form-item label="头像">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              accept="image/*"
              class="avatar-uploader"
            >
              <div class="avatar-preview">
                <img v-if="previewUrl" :src="previewUrl" class="avatar-img" />
                <img v-else-if="form.avatar" :src="avatarUrl(form.avatar)" class="avatar-img" />
                <div v-else class="avatar-placeholder">
                  <el-icon :size="32"><UserFilled /></el-icon>
                </div>
                <div class="avatar-overlay">
                  <el-icon :size="20"><Camera /></el-icon>
                  <span>更换头像</span>
                </div>
              </div>
            </el-upload>
            <div style="font-size: 12px; color: #909399; line-height: 1.5;">
              <p style="margin: 0;">支持 JPG/PNG/GIF</p>
              <p style="margin: 4px 0 0 0;">点击头像区域上传</p>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUser">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script setup>
import {ref,onMounted} from 'vue'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'
import { UserFilled, Camera } from '@element-plus/icons-vue'

const userList = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const isAdd = ref(true)
const form = ref({username:'',password:'',nickname:'',id:0,avatar:''})
const excelFileRef = ref(null)
const uploadRef = ref(null)
const selectedFile = ref(null)
const previewUrl = ref('')

const avatarUrl = (name) => `${import.meta.env.VITE_AVATAR_URL || '/upload/avatars'}/${name}`

const getUserList = async ()=>{
  const res = await request.get(`/user/list?page=${page.value}&size=${size.value}`)
  userList.value = res.data.data
  total.value = res.data.total
}
const openAddDialog = ()=>{
  dialogVisible.value = true
  isAdd.value = true
  form.value = {username:'',password:'',nickname:'',id:0,avatar:''}
  selectedFile.value = null
  previewUrl.value = ''
}
const openEditDialog = (row)=>{
  dialogVisible.value = true
  isAdd.value = false
  form.value = {...row}
  selectedFile.value = null
  previewUrl.value = ''
}
const handleFileChange = (file)=>{
  selectedFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
}
const submitUser = async ()=>{
  const fd = new FormData()
  if(isAdd.value){
    fd.append('username', form.value.username)
    fd.append('password', form.value.password)
    fd.append('nickname', form.value.nickname)
    if(selectedFile.value) fd.append('file', selectedFile.value)
    await request.post('/user/add', fd)
  } else {
    fd.append('uid', form.value.id)
    fd.append('nickname', form.value.nickname)
    if(selectedFile.value) fd.append('file', selectedFile.value)
    await request.post('/user/update', fd)
  }
  dialogVisible.value = false
  ElMessage.success(isAdd.value ? '新增成功' : '修改成功')
  getUserList()
}
const delUser = async (uid)=>{
  await request.delete(`/user/del?uid=${uid}`)
  ElMessage.success('删除成功')
  getUserList()
}
const exportExcel = async ()=>{
  const res = await request.get('/excel/export/user',{responseType:'blob'})
  const blob = new Blob([res.data],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = '用户数据.xlsx'
  a.click()
}
const uploadExcel = ()=>excelFileRef.value.click()
const handleImport = async (e)=>{
  const file = e.target.files[0]
  const fd = new FormData()
  fd.append('file',file)
  await request.post('/excel/import/user',fd)
  ElMessage.success('导入成功')
  getUserList()
}
onMounted(getUserList)
</script>

<style scoped>
.avatar-preview {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 2px dashed #dcdfe6;
  transition: border-color 0.3s;
}
.avatar-preview:hover {
  border-color: #409eff;
}
.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #c0c4cc;
}
.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
  gap: 4px;
}
.avatar-preview:hover .avatar-overlay {
  opacity: 1;
}
</style>

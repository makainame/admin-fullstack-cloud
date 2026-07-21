import axios from 'axios'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api'
})

service.interceptors.request.use(config=>{
  const token = localStorage.getItem('token')
  if(token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default service

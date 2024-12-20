<template>
    <div class="profile-container">
      <div class="profile-box">
        <h2 class="profile-title">用户信息</h2>
        <el-form :model="userInfo" label-position="top">
          <el-form-item label="头像" class="avatar-item">
            <el-avatar :size="120" :src="userInfo.avatar">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png" />
            </el-avatar>
            <el-button class="avatar-upload-btn" type="primary" plain @click="uploadAvatar">
              <Camera class="icon" />
              更换头像
            </el-button>
          </el-form-item>
  
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" disabled>
              <template #prefix>
                <User class="icon" />
              </template>
            </el-input>
          </el-form-item>
  
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email" disabled>
              <template #prefix>
                <Mail class="icon" />
              </template>
            </el-input>
          </el-form-item>
  
          <el-form-item label="注册时间">
            <el-input v-model="userInfo.registrationDate" disabled>
              <template #prefix>
                <Calendar class="icon" />
              </template>
            </el-input>
          </el-form-item>
  
          <el-form-item label="上次登录">
            <el-input v-model="userInfo.lastLogin" disabled>
              <template #prefix>
                <Clock class="icon" />
              </template>
            </el-input>
          </el-form-item>
  
          <el-form-item label="账户状态">
            <el-tag :type="userInfo.status === '正常' ? 'success' : 'danger'" effect="dark">
              {{ userInfo.status }}
            </el-tag>
          </el-form-item>
  
          <el-form-item class="action-buttons">
            <el-button type="primary" @click="editProfile">
              <Edit class="icon" />
              编辑资料
            </el-button>
            <el-button @click="changePassword">
              <Key class="icon" />
              修改密码
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { ElMessage } from 'element-plus';
  import { User, Mail, Calendar, Clock, Camera, Edit, Key } from 'lucide-vue-next';
  
  const userInfo = ref({
    username: 'johndoe',
    email: 'johndoe@example.com',
    avatar: '',
    registrationDate: '2023-05-15',
    lastLogin: '2023-06-01 14:30',
    status: '正常'
  });
  
  const uploadAvatar = () => {
    ElMessage.info('头像上传功能待实现');
  };
  
  const editProfile = () => {
    ElMessage.info('编辑资料功能待实现');
  };
  
  const changePassword = () => {
    ElMessage.info('修改密码功能待实现');
  };
  </script>
  
  <style scoped>
  .profile-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f6f9fc 0%, #e9f1f7 100%);
    padding: 20px;
  }
  
  .profile-box {
    width: 100%;
    max-width: 480px;
    padding: 40px;
    background-color: #ffffff;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    border-radius: 24px;
    transition: all 0.3s ease;
  }
  
  .profile-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.12);
  }
  
  .profile-title {
    text-align: center;
    margin-bottom: 35px;
    font-size: 32px;
    color: #2c3e50;
    font-weight: 700;
  }
  
  .el-form-item {
    margin-bottom: 28px;
  }
  
  .avatar-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .el-avatar {
    margin-bottom: 15px;
    border: 4px solid #fff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }
  
  .el-avatar:hover {
    transform: scale(1.05);
  }
  
  .avatar-upload-btn {
    margin-top: 10px;
  }
  
  .el-input :deep(.el-input__wrapper) {
    border-radius: 12px;
    border: 1px solid #e0e6ed;
    transition: all 0.3s ease;
    box-shadow: none;
  }
  
  .el-input :deep(.el-input__wrapper:hover),
  .el-input :deep(.el-input__wrapper.is-focus) {
    border-color: #409eff;
    box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
  }
  
  .el-button {
    border-radius: 12px;
    font-size: 16px;
    height: 48px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .el-button--primary {
    background-color: #409eff;
    border-color: #409eff;
  }
  
  .el-button--primary:hover,
  .el-button--primary:focus {
    background-color: #66b1ff;
    border-color: #66b1ff;
  }
  
  .action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .action-buttons .el-button {
    flex: 1;
    margin: 0 10px;
  }
  
  .icon {
    width: 18px;
    height: 18px;
    margin-right: 8px;
  }
  
  .el-tag {
    font-size: 14px;
    padding: 6px 12px;
    border-radius: 8px;
  }
  
  @media (max-width: 480px) {
    .profile-box {
      padding: 30px 20px;
    }
  
    .action-buttons {
      flex-direction: column;
    }
  
    .action-buttons .el-button {
      margin: 10px 0;
    }
  }
  </style>
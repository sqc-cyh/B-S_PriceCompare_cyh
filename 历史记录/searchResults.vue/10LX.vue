<template>
    <div class="profile-container">
      <div class="profile-box">
        <h2 class="profile-title">用户信息</h2>
        <el-form :model="userInfo" label-position="top">
          <el-form-item label="头像">
            <el-avatar :size="100" :src="userInfo.avatar">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png" />
            </el-avatar>
            <el-button class="avatar-upload-btn" size="small" @click="uploadAvatar">更换头像</el-button>
          </el-form-item>
  
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" disabled prefix-icon="el-icon-user"></el-input>
          </el-form-item>
  
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email" disabled prefix-icon="el-icon-message"></el-input>
          </el-form-item>
  
          <el-form-item label="注册时间">
            <el-input v-model="userInfo.registrationDate" disabled prefix-icon="el-icon-date"></el-input>
          </el-form-item>
  
          <el-form-item label="上次登录">
            <el-input v-model="userInfo.lastLogin" disabled prefix-icon="el-icon-time"></el-input>
          </el-form-item>
  
          <el-form-item label="账户状态">
            <el-tag :type="userInfo.status === '正常' ? 'success' : 'danger'">
              {{ userInfo.status }}
            </el-tag>
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" @click="editProfile">编辑资料</el-button>
            <el-button @click="changePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { ElMessage } from 'element-plus';
  
  export default {
    name: 'UserPage', // 组件名称
    setup() {
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
  
      return {
        userInfo,
        uploadAvatar,
        editProfile,
        changePassword
      };
    }
  };
  </script>
  
  <style scoped>
  .profile-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
  }
  
  .profile-box {
    width: 100%;
    max-width: 450px;
    padding: 40px;
    background-color: #ffffff;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    transition: all 0.3s ease;
  }
  
  .profile-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  }
  
  .profile-title {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px;
    color: #333;
    font-weight: 600;
  }
  
  .el-form-item {
    margin-bottom: 25px;
  }
  
  .el-input__inner {
    border-radius: 8px;
    border: 1px solid #d4d4d4;
    transition: all 0.3s ease;
  }
  
  .el-input__inner:focus {
    border-color: #909399;
    box-shadow: 0 0 0 2px rgba(144, 147, 153, 0.2);
  }
  
  .el-button {
    border-radius: 8px;
    font-size: 16px;
    height: 44px;
    transition: all 0.3s ease;
  }
  
  .el-button--primary {
    background-color: #606266;
    border-color: #606266;
  }
  
  .el-button--primary:hover, .el-button--primary:focus {
    background-color: #909399;
    border-color: #909399;
  }
  
  .avatar-upload-btn {
    margin-left: 15px;
  }
  
  @media (max-width: 480px) {
    .profile-box {
      padding: 30px 20px;
    }
  }
  </style>
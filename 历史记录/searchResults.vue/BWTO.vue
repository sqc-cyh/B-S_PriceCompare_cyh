<template>
    <div class="profile-container">
      <div class="profile-box">
        <h2 class="profile-title">用户信息</h2>
        <el-form :model="userInfo" label-position="top" class="profile-form">
          
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" disabled prefix-icon="el-icon-user"></el-input>
          </el-form-item>
  
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email" disabled prefix-icon="el-icon-message"></el-input>
          </el-form-item>
  
          <el-form-item label="账户状态">
            <el-tag :type="userInfo.status === '正常' ? 'success' : 'danger'">
              {{ userInfo.status }}
            </el-tag>
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
        status: '正常'
      });
  
      const changePassword = () => {
        ElMessage.info('修改密码功能待实现');
      };
  
      return {
        userInfo,
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
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
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
    border: 1px solid #e0e0e0;
  }
  
  .profile-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  }
  
  .profile-title {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px;
    color: #333;
    font-weight: 600;
  }
  
  .profile-form {
    font-size: 16px; /* 全局字体大小 */
  }
  
  .el-form-item {
    margin-bottom: 20px; /* 增加表单项之间的间距 */
  }
  
  .el-input__inner {
    border-radius: 8px;
    border: 1px solid #d4d4d4;
    transition: all 0.3s ease;
  }
  
  .el-input__inner:focus {
    border-color: #409EFF; /* 聚焦时的边框颜色 */
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  }
  
  .el-button {
    border-radius: 8px;
    font-size: 16px;
    height: 44px;
    transition: all 0.3s ease;
  }
  
  .el-button--primary {
    background-color: #409EFF; /* 主按钮颜色 */
    border-color: #409EFF;
  }
  
  .el-button--primary:hover,
  .el-button--primary:focus {
    background-color: #66b1ff; /* 悬停状态 */
    border-color: #66b1ff;
  }
  
  @media (max-width: 480px) {
    .profile-box {
      padding: 30px 20px;
    }
  }
  </style>
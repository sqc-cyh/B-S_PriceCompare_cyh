vue

复制
<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">欢迎回来</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            clearable
          ></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            clearable
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">登录</el-button>
        </el-form-item>

        <el-form-item class="footer-links">
          <span>还没有账号？</span>
          <el-link type="primary" @click="goToRegister">注册新账户</el-link>
          <el-link type="primary" @click="goToResetPassword" style="margin-left: 10px;">忘记密码？</el-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter();
    const formRef = ref(null);
    const form = reactive({
      username: '',
      password: ''
    });

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    };

    const loading = ref(false);

    const submitForm = async () => {
      formRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true;
          try {
            const response = await axios.post('http://127.0.0.1:8000/users/login/', {
              username: form.username,
              password: form.password,
            });
            ElMessage.success(response.data.message);
            // 保存用户名到 localStorage
            localStorage.setItem('username', form.username);
            setTimeout(() => {
              loading.value = false;
              router.push('/compare');
            }, 2000);
          } catch (error) {
            loading.value = false;
            ElMessage.error(error.response?.data?.message || '登录失败');
          }
        } else {
          ElMessage.error('请正确填写所有必填项');
        }
      });
    };

    const goToRegister = () => {
      router.push('/register');
    };
    const goToResetPassword = () => {
      router.push('/forget');
    };
    
    return {
      form,
      rules,
      formRef,
      loading,
      submitForm,
      goToRegister,
      goToResetPassword
    };
  }
};
</script>



<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  background-color: #ffffff;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.login-title {
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
  width: 100%;
  border-radius: 8px;
  font-size: 16px;
  height: 44px;
  transition: all 0.3s ease;
}

.el-button--primary {
  background-color: #606266;
  border-color: #606266;
}

.el-button--primary:hover,
.el-button--primary:focus {
  background-color: #909399;
  border-color: #909399;
}

.footer-links {
  text-align: center;
  margin-top: 15px;
}

.el-link {
  margin-left: 5px;
}

@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }
}
</style>
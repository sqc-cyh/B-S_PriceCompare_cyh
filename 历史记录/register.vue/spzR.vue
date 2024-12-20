<template>
    <div class="register-container">
      <div class="register-box">
        <h2 class="register-title">创建新账户</h2>
        <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="6-20个字符，字母开头"
              prefix-icon="el-icon-user"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="至少6个字符，包含字母和数字"
              prefix-icon="el-icon-lock"
              clearable
              @input="checkPasswordStrength"
            ></el-input>
            <div class="password-strength">
              <div class="strength-bar" :style="{ width: passwordStrength + '%' }"></div>
            </div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
          </el-form-item>
  
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请确认密码"
              prefix-icon="el-icon-lock"
              clearable
            ></el-input>
            <p v-if="passwordMismatch" class="error-message">
              两次输入的密码不一致
            </p>
          </el-form-item>
  
          <!-- 其他表单项省略 -->
  
          <el-form-item>
            <el-button type="primary" @click="submitForm" :loading="loading">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed } from 'vue';
  import { ElMessage } from 'element-plus';
  
  export default {
    name: 'GrayRegistrationPage',
    setup() {
      const formRef = ref(null);
      const form = reactive({
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        phone: '',
        captcha: '',
        agree: false
      });
  
      const passwordMismatch = computed(() => {
        return form.password !== form.confirmPassword;
      });
  
      const passwordStrength = ref(0);
      const passwordStrengthText = ref('');
  
      const checkPasswordStrength = () => {
        const password = form.password;
        let strength = 0;
        if (password.length >= 6) strength += 20;
        if (password.match(/[A-Z]/)) strength += 20;
        if (password.match(/[a-z]/)) strength += 20;
        if (password.match(/[0-9]/)) strength += 20;
        if (password.match(/[^A-Za-z0-9]/)) strength += 20;
        passwordStrength.value = strength;
  
        if (strength < 40) passwordStrengthText.value = '弱';
        else if (strength < 80) passwordStrengthText.value = '中';
        else passwordStrengthText.value = '强';
      };
  
      const submitForm = () => {
        if (passwordMismatch.value) {
          ElMessage.error('两次输入的密码不一致');
          return;
        }
        // 表单验证和提交逻辑省略
      };
  
      return {
        form,
        formRef,
        passwordMismatch,
        passwordStrength,
        passwordStrengthText,
        checkPasswordStrength,
        submitForm,
      };
    },
  };
  </script>
  
<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.register-box {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  background-color: #ffffff;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.register-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.register-title {
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

.el-button--primary:hover, .el-button--primary:focus {
  background-color: #909399;
  border-color: #909399;
}

.el-checkbox {
  margin-top: 10px;
  color: #606266;
}

.password-strength {
  height: 4px;
  background-color: #e0e0e0;
  margin-top: 5px;
  border-radius: 2px;
  overflow: hidden;
}

.strength-bar {
  height: 100%;
  transition: width 0.3s ease;
  background-color: #909399;
}

.strength-text {
  font-size: 12px;
  color: #606266;
  margin-top: 5px;
  display: inline-block;
}

.el-link {
  font-weight: 400;
  color: #606266;
}

.el-link:hover {
  color: #909399;
}

@media (max-width: 480px) {
  .register-box {
    padding: 30px 20px;
  }
}
</style>
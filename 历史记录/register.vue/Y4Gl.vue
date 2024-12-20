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
              @input="debouncedCheckPasswordStrength"
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
          </el-form-item>
  
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱"
              prefix-icon="el-icon-message"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="手机号码" prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号码"
              prefix-icon="el-icon-mobile-phone"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="验证码" prop="captcha">
            <el-row :gutter="10">
              <el-col :span="16">
                <el-input
                  v-model="form.captcha"
                  placeholder="请输入验证码"
                ></el-input>
              </el-col>
              <el-col :span="8">
                <el-button type="primary" @click="sendCaptcha" :disabled="captchaDisabled">
                  {{ captchaText }}
                </el-button>
              </el-col>
            </el-row>
          </el-form-item>
  
          <el-form-item>
            <el-checkbox v-model="form.agree">
              我已阅读并同意
              <el-link type="primary" @click="showAgreement">《用户协议》</el-link>
              和
              <el-link type="primary" @click="showPrivacy">《隐私政策》</el-link>
            </el-checkbox>
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" @click="submitForm" :loading="loading">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  import debounce from 'lodash/debounce';
  
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
  
      const rules = {
        // 省略规则定义以节省空间
      };
  
      const loading = ref(false);
      const captchaDisabled = ref(false);
      const captchaText = ref('发送验证码');
      const passwordStrength = ref(0);
      const passwordStrengthText = ref('');
  
      const debouncedCheckPasswordStrength = debounce(function() {
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
      }, 300);
  
      const sendCaptcha = () => {
        // 发送验证码逻辑
        ElMessage.success('验证码已发送');
      };
  
      const submitForm = () => {
        formRef.value.validate((valid) => {
          if (valid) {
            loading.value = true;
            setTimeout(() => {
              loading.value = false;
              ElMessage.success('注册成功');
            }, 2000);
          } else {
            ElMessage.error('请正确填写所有必填项');
          }
        });
      };
  
      const showAgreement = () => {
        ElMessage('这里显示用户协议内容');
      };
  
      const showPrivacy = () => {
        ElMessage('这里显示隐私政策内容');
      };
  
      return {
        form,
        rules,
        formRef,
        loading,
        captchaDisabled,
        captchaText,
        passwordStrength,
        passwordStrengthText,
        debouncedCheckPasswordStrength,
        sendCaptcha,
        submitForm,
        showAgreement,
        showPrivacy,
      };
    },
  };
  </script>
  
  <style scoped>
  /* 样式与原代码相同，确保使用灰色调 */
  </style>
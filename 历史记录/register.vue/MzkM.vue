<template>
    <div class="register-container">
      <div class="register-box">
        <h2 class="register-title">加入我们</h2>
        <el-form :model="form" :rules="rules" ref="formRef">
          <el-form-item prop="username">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-user"></i> 选择您的用户名
              </span>
            </template>
            <el-input
              v-model="form.username"
              placeholder="6-20个字符，字母开头"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item prop="password">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-lock"></i> 创建安全密码
              </span>
            </template>
            <el-input
              v-model.lazy="form.password"
              type="password"
              placeholder="至少6个字符，包含字母和数字"
              clearable
              @input="checkPasswordStrength"
            ></el-input>
            <div class="password-strength">
              <div class="strength-bar" :style="{ width: passwordStrength + '%' }"></div>
            </div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
          </el-form-item>
  
          <el-form-item prop="confirmPassword">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-check"></i> 确认您的密码
              </span>
            </template>
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item prop="email">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-message"></i> 您的电子邮箱
              </span>
            </template>
            <el-input
              v-model="form.email"
              placeholder="example@domain.com"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item prop="phone">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-mobile-phone"></i> 手机号码
              </span>
            </template>
            <el-input
              v-model="form.phone"
              placeholder="请输入11位手机号"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item prop="captcha">
            <template #label>
              <span class="custom-label">
                <i class="el-icon-key"></i> 验证码
              </span>
            </template>
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
            <el-button type="primary" @click="submitForm" :loading="loading">完成注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted, watch } from 'vue';
  import { ElMessage } from 'element-plus';
  import debounce from 'lodash/debounce';
  
  export default {
    name: 'CompleteGrayRegistrationPage',
    setup() {
      const formRef = ref(null);
      const form = reactive({
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        phone: '',
        captcha: '',
        agree: false,
      });
  
      const loading = ref(false);
      const captchaDisabled = ref(false);
      const captchaText = ref('发送验证码');
      const passwordStrength = ref(0);
      const passwordStrengthText = ref('');
  
      const rules = {
        username: [
          { required: true, message: '请输入用户名', trigger: 'change' },
          { min: 6, max: 20, message: '用户名长度在6-20个字符之间', trigger: 'change' },
          { pattern: /^[a-zA-Z]/, message: '用户名必须以字母开头', trigger: 'change' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'change' },
          { min: 6, message: '密码至少6个字符', trigger: 'change' },
          {
            pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/,
            message: '密码必须包含字母和数字',
            trigger: 'change',
          },
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== form.password) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'change' },
          { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] },
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'change' },
          {
            pattern: /^[1][3-9][0-9]{9}$/,
            message: '手机号码格式不正确',
            trigger: 'change',
          },
        ],
        captcha: [
          { required: true, message: '请输入验证码', trigger: 'change' },
        ],
        agree: [
          {
            validator: (rule, value, callback) => {
              if (!value) {
                callback(new Error('请阅读并同意用户协议和隐私政策'));
              } else {
                callback();
              }
            },
            trigger: 'change',
          },
        ],
      };
  
      const checkPasswordStrength = debounce(() => {
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
        if (!form.phone) {
          ElMessage.warning('请先输入手机号码');
          return;
        }
        captchaDisabled.value = true;
        let count = 60;
        const timer = setInterval(() => {
          if (count > 0) {
            captchaText.value = `${count}秒后重试`;
            count--;
          } else {
            clearInterval(timer);
            captchaDisabled.value = false;
            captchaText.value = '发送验证码';
          }
        }, 1000);
        ElMessage.success('验证码已发送');
      };
  
      const submitForm = () => {
        if (!formRef.value) return;
        formRef.value.validate((valid) => {
          if (valid) {
            loading.value = true;
            setTimeout(() => {
              loading.value = false;
              ElMessage.success('注册成功');
            }, 2000);
          } else {
            ElMessage.error('请正确填写所有必填项');
            return false;
          }
        });
      };
  
      const showAgreement = () => {
        ElMessage('这里显示用户协议内容');
      };
  
      const showPrivacy = () => {
        ElMessage('这里显示隐私政策内容');
      };
  
      watch(
        () => form.password,
        () => {
          checkPasswordStrength();
        },
        { immediate: true, flush: 'post' }
      );
  
      return {
        form,
        rules,
        formRef,
        loading,
        captchaDisabled,
        captchaText,
        passwordStrength,
        passwordStrengthText,
        checkPasswordStrength,
        sendCaptcha,
        submitForm,
        showAgreement,
        showPrivacy,
      };
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height;
  }